"""
Coupled entrance-rando shuffle over exits.json.

Approach (ALTTPR-style coupled pairing with guaranteed connectivity):
  1. Collect every shufflable exit (edges + doors; skip gated/needs_review/
    known_gaps entries -- those stay vanilla).
  2. Build a spanning tree first: randomly connect rooms one at a time by
    picking an unused exit from the "frontier" (rooms already reachable)
    to an unused exit belonging to a room not yet reached. This GUARANTEES
    full connectivity by construction, rather than hoping random pairing
    happens to connect everything and retrying.
  3. Pair up all remaining (non-spanning-tree) exits randomly among
    themselves -- these are the "extra" connections that add shortcuts/
    loops on top of the guaranteed-connected backbone.
  4. Each pairing is coupled: exit A <-> exit B means walking out of A's
    origin lands you at B's origin (using B's own dest_x/dest_y as the
    safe landing spot), and walking out of B's origin lands you at A's
    origin (using A's dest_x/dest_y).

Output: connections.json -- a flat list of resolved transitions, keyed by
(originNorth, originEast, vanillaDestNorth, vanillaDestEast) so the runtime
patch can look up "given this vanilla transition, where should it actually
go" without needing to know which mechanism (edge/door) produced it.
"""

import json
import random
import sys, os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 12345

exits_data = json.load(open(f"{OUT_DIR}/exits.json"))
all_exits_raw = []
for e in exits_data["edges"]:
  if e.get("gated") or e.get("needs_review"):
    continue
  all_exits_raw.append(e)
for d in exits_data["doors"]:
  if d.get("gated") or d.get("needs_review"):
    continue
  all_exits_raw.append(d)

# Dedupe: a door placed at a room's literal edge and the edge-walk itself
# both compute the same (origin, vanillaDest) -- they're the SAME physical
# transition point at runtime (the lookup table is keyed on vanillaDest,
# not on which mechanism triggered it), so treat them as one shufflable
# exit. Keep the first one seen; record which ids got merged for visibility.
seen = {}
merged_log = []
all_exits = []
for e in all_exits_raw:
  o = e["origin"]
  d = e["dest"]
  key = (o["north"], o["east"], d["north"], d["east"])
  if key in seen:
    merged_log.append((seen[key]["id"], e["id"]))
    continue
  seen[key] = e
  all_exits.append(e)

print(
  f"Raw exits: {len(all_exits_raw)}  ->  after dedup: {len(all_exits)}  ({len(merged_log)} merged)"
)
for a, b in merged_log[:10]:
  print(f"  merged: {b}  ->  treated as same exit as {a}")

print(f"Total shufflable exits: {len(all_exits)}")

# index exits per origin room, and build the room set
rooms = set()
exits_by_room = {}
for e in all_exits:
  org = (e["origin"]["north"], e["origin"]["east"])
  rooms.add(org)
  exits_by_room.setdefault(org, []).append(e)

print(f"Rooms with at least one shufflable exit: {len(rooms)}")

rng = random.Random(SEED)

# ---------------------------------------------------------------------------
# Step 1: spanning tree to guarantee connectivity
# ---------------------------------------------------------------------------
rooms_list = list(rooms)
rng.shuffle(rooms_list)
start_room = rooms_list[0]

reached = {start_room}
frontier_exits = list(exits_by_room.get(start_room, []))
rng.shuffle(frontier_exits)

unused = {e["id"]: e for e in all_exits}
spanning_pairs = [] # list of (exitA, exitB)

remaining_rooms = set(rooms) - reached
attempts = 0
max_attempts = len(all_exits) * 5

while remaining_rooms and frontier_exits and attempts < max_attempts:
  attempts += 1
  a = frontier_exits.pop()
  if a["id"] not in unused:
    continue
  # find an exit belonging to ANY not-yet-reached room to pair with `a`
  candidates = [
    e
    for room in remaining_rooms
    for e in exits_by_room.get(room, [])
    if e["id"] in unused and e["id"] != a["id"]
  ]
  if not candidates:
    continue
  b = rng.choice(candidates)
  del unused[a["id"]]
  del unused[b["id"]]
  spanning_pairs.append((a, b))
  b_room = (b["origin"]["north"], b["origin"]["east"])
  reached.add(b_room)
  remaining_rooms.discard(b_room)
  # newly reached room's remaining exits join the frontier
  for e in exits_by_room.get(b_room, []):
    if e["id"] in unused:
      frontier_exits.append(e)
  rng.shuffle(frontier_exits)

print(
  f"Spanning tree: {len(spanning_pairs)} pairs, rooms reached: {len(reached)}/{len(rooms)}"
)
if remaining_rooms:
  print(
    f"WARNING: {len(remaining_rooms)} rooms unreachable by spanning tree (isolated, single-exit-to-nowhere, or ran out of exits): {sorted(remaining_rooms)[:10]}"
  )

# ---------------------------------------------------------------------------
# Step 2: pair up all leftover exits randomly among themselves
# ---------------------------------------------------------------------------
leftover = list(unused.values())
rng.shuffle(leftover)
extra_pairs = []
while len(leftover) >= 2:
  a = leftover.pop()
  b = leftover.pop()
  extra_pairs.append((a, b))
odd_one_out = leftover[0] if leftover else None
if odd_one_out:
  print(
    f"Odd exit left unpaired (self-loop, sends back to its own origin): {odd_one_out['id']}"
  )

print(f"Extra pairs (loops/shortcuts beyond spanning tree): {len(extra_pairs)}")

all_pairs = spanning_pairs + extra_pairs

# ---------------------------------------------------------------------------
# Build final connections table
# ---------------------------------------------------------------------------
connections = []


def vanilla_dest_key(e):
  if e["mechanism"] == "edge":
    d = e["dest"]
    return (d["north"], d["east"])
  else:
    d = e["dest"]
    return (d["north"], d["east"])


FALLBACK_X = 330
FALLBACK_Y = 260


def make_connection(from_exit, to_exit):
  origin = from_exit["origin"]
  vdest = vanilla_dest_key(from_exit)
  new_x = to_exit.get("dest_x")
  new_y = to_exit.get("dest_y")
  return {
    "originNorth": origin["north"],
    "originEast": origin["east"],
    "vanillaDestNorth": vdest[0],
    "vanillaDestEast": vdest[1],
    "newDestNorth": to_exit["origin"]["north"],
    "newDestEast": to_exit["origin"]["east"],
    "newX": new_x if new_x is not None else FALLBACK_X,
    "newY": new_y if new_y is not None else FALLBACK_Y,
    "fromExitId": from_exit["id"],
    "toExitId": to_exit["id"],
  }


for a, b in all_pairs:
  connections.append(make_connection(a, b))
  connections.append(make_connection(b, a))

if odd_one_out:
  connections.append(make_connection(odd_one_out, odd_one_out))

# sanity: no duplicate (originNorth,originEast,vanillaDestNorth,vanillaDestEast) keys
seen_keys = {}
dup_count = 0
for c in connections:
  k = (c["originNorth"], c["originEast"], c["vanillaDestNorth"], c["vanillaDestEast"])
  if k in seen_keys:
    dup_count += 1
  seen_keys[k] = c

print(f"\nTotal connections: {len(connections)}  (duplicate lookup keys: {dup_count})")

out = {
  "seed": SEED,
  "connections": connections,
}
with open(f"{OUT_DIR}/connections.json", "w") as f:
  json.dump(out, f, indent=2)

print(f"Wrote connections.json with seed={SEED}")

# ---------------------------------------------------------------------------
# Verify connectivity by BFS over the shuffled graph
# ---------------------------------------------------------------------------
adj = {}
for c in connections:
  adj.setdefault((c["originNorth"], c["originEast"]), []).append(
    (c["newDestNorth"], c["newDestEast"])
  )

visited = {start_room}
queue = [start_room]
while queue:
  cur = queue.pop()
  for nxt in adj.get(cur, []):
    if nxt not in visited:
      visited.add(nxt)
      queue.append(nxt)

print(
  f"BFS reachability check from {start_room}: {len(visited)}/{len(rooms)} rooms reachable"
)
unreachable = rooms - visited
if unreachable:
  print(f"  UNREACHABLE: {sorted(unreachable)}")
else:
  print("  All rooms reachable. Map is fully connected.")
