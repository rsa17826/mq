"""
Coupled entrance-rando shuffle over exits.json.

Approach (ALTTPR-style coupled pairing with guaranteed connectivity):
  1. Collect every shufflable exit (edges + doors; skip gated/needs_review/
    known_gaps entries -- those stay vanilla).
  2. Two SEPARATE pairing universes:
    - Edges (north/south/east/west) can ONLY pair with the opposite
      compass direction (north<->south, east<->west). This guarantees
      "walk west, walk east to come back" -- never "walk west, have
      to walk up to get back". Doors are never used as an edge's
      partner, since they carry no compass direction.
    - Doors (stairs, caves, wallCrack, etc.) pair freely among
      themselves, same as before -- no compass concept applies to an
      object-click teleport.
  Each universe gets its own spanning-tree-for-connectivity pass, then
  leftover exits in that universe get paired randomly among themselves.
  3. Real per-room exit geometry (optional, see load_room_geometry below):
    when available for a room, it tells us which of the 4 sides actually
    have an opening (replacing the old "assume all 4 directions, then
    flag invalid via destination lookup" heuristic) and the gap's pixel
    range, whose midpoint becomes the landing position for that exit
    (far more accurate than the flat 330/260 fallback).

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

OPPOSITE = {"north": "south", "south": "north", "east": "west", "west": "east"}


def load_room_geometry():
  """Optional per-room exit-gap geometry, e.g.:
    [{"north": 17, "east": 19, "exits": {
      "west": null, "south": null,
      "east": {"top": 20, "bottom": 40},
      "north": {"left": 20, "right": 90}
    }}, ...]
  Accepts either that list form, or a dict keyed "north_east" -> exits.
  Returns a dict keyed (north, east) -> {"west": gap_or_None, ...}, or
  {} if no geometry file is present (callers must degrade gracefully).
  """
  path = os.path.join(OUT_DIR, "room_geometry.json")
  if not os.path.exists(path):
    print(
      f"NOTE: no room_geometry.json found at {path} -- all rooms will "
      f"fall back to the old exits.json-derived behavior (no gap "
      f"filtering, flat fallback landing position)."
    )
    return {}
  raw = json.load(open(path))
  geo = {}
  if isinstance(raw, list):
    for rec in raw:
      geo[(float(rec["north"]), float(rec["east"]))] = rec["exits"]
  elif isinstance(raw, dict):
    for k, v in raw.items():
      n_str, e_str = k.split("_")
      geo[(float(n_str), float(e_str))] = v.get("exits", v)
  else:
    raise ValueError("room_geometry.json must be a list or dict")
  print(f"Loaded room geometry for {len(geo)} rooms from {path}")
  return geo


def gap_midpoint(direction, gap):
  """gap is the {"left","right"} or {"top","bottom"} dict for this
  direction; returns the coordinate to use as the entry x or y."""
  if gap is None:
    return None
  if direction in ("north", "south"):
    return (gap["left"] + gap["right"]) / 2
  else:
    return (gap["top"] + gap["bottom"]) / 2


exits_data = json.load(open(f"{OUT_DIR}/exits.json"))
geometry = load_room_geometry()

all_exits_raw = []
geometry_dropped = 0
for e in exits_data["edges"]:
  if e.get("gated") or e.get("needs_review"):
    continue
  org = (e["origin"]["north"], e["origin"]["east"])
  geo_room = geometry.get(org)
  if geo_room is not None:
    gap = geo_room.get(e["direction"])
    if gap is None:
      geometry_dropped += 1
      continue # geometry says this side has no opening -- not a real exit
    mid = gap_midpoint(e["direction"], gap)
    if mid is not None:
      # geometry's gap midpoint is more accurate than whatever exits.json
      # had (vanilla per-room fixup or the flat fallback); override it as
      # this exit's landing position when something else routes here.
      if e["direction"] in ("north", "south"):
        e = dict(e, dest_x=mid)
      else:
        e = dict(e, dest_y=mid)
  all_exits_raw.append(e)
for d in exits_data["doors"]:
  if d.get("gated") or d.get("needs_review"):
    continue
  all_exits_raw.append(d)

if geometry:
  print(
    f"Geometry filtering: dropped {geometry_dropped} edges with no opening on that side"
  )

# Dedupe: a door placed at a room's literal edge and the edge-walk itself
# both compute the same (origin, vanillaDest) -- they're the SAME physical
# transition point at runtime (the lookup table is keyed on vanillaDest,
# not on which mechanism triggered it), so treat them as one shufflable
# exit. Prefer keeping the EDGE record when one collides with a door:
# edges carry the compass direction needed for the opposite-pairing rule,
# doors don't, so dropping the door loses no information.
seen = {}
merged_log = []
for e in all_exits_raw:
  o = e["origin"]
  d = e["dest"]
  key = (o["north"], o["east"], d["north"], d["east"])
  if key not in seen:
    seen[key] = e
    continue
  existing = seen[key]
  if existing["mechanism"] == "edge" and e["mechanism"] != "edge":
    merged_log.append((existing["id"], e["id"])) # keep existing edge, drop e
    continue
  if e["mechanism"] == "edge" and existing["mechanism"] != "edge":
    merged_log.append((e["id"], existing["id"])) # new edge replaces old door
    seen[key] = e
    continue
  merged_log.append((existing["id"], e["id"])) # same mechanism type, keep first

all_exits = list(seen.values())

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

edge_exits = [e for e in all_exits if e["mechanism"] == "edge"]
door_exits = [e for e in all_exits if e["mechanism"] != "edge"]
print(
  f"Edge exits: {len(edge_exits)} (opposite-direction constrained)  |  "
  f"Door exits: {len(door_exits)} (freely paired)"
)


def build_spanning_tree(pool, partner_finder, label, seed_reached=None):
  """Generic spanning-tree-then-leftover-pairing over `pool` (a list of
  exits). `partner_finder(a, candidates)` returns the list of exits in
  `candidates` that are valid partners for `a` (e.g. opposite direction
  for edges, anything for doors). `seed_reached`, if given, is a set of
  rooms considered already-reachable from elsewhere (e.g. the edge
  backbone) -- any pool exit belonging to one of those rooms starts in
  the frontier immediately, so a sparse pool (like doors) connects INTO
  the existing component instead of risking an isolated sub-cluster."""
  pool_rooms = set()
  by_room = {}
  for e in pool:
    org = (e["origin"]["north"], e["origin"]["east"])
    pool_rooms.add(org)
    by_room.setdefault(org, []).append(e)

  if not pool_rooms:
    return [], [], set()

  unused = {e["id"]: e for e in pool}
  seed_reached = seed_reached or set()
  pre_reached = pool_rooms & seed_reached

  if pre_reached:
    reached = set(pre_reached)
    frontier = [e for room in pre_reached for e in by_room.get(room, [])]
  else:
    rooms_list = list(pool_rooms)
    rng.shuffle(rooms_list)
    start = rooms_list[0]
    reached = {start}
    frontier = list(by_room.get(start, []))
  rng.shuffle(frontier)

  spanning_pairs = []
  remaining = set(pool_rooms) - reached
  attempts = 0
  max_attempts = len(pool) * 5

  while remaining and attempts < max_attempts:
    attempts += 1
    if not frontier:
      # refill from ALL unused exits in already-reached rooms before
      # giving up -- a plain stack can dead-end early on sparse pools
      frontier = [
        e
        for room in reached
        for e in by_room.get(room, [])
        if e["id"] in unused
      ]
      rng.shuffle(frontier)
      if not frontier:
        break
    a = frontier.pop()
    if a["id"] not in unused:
      continue
    candidates = [
      e
      for room in remaining
      for e in by_room.get(room, [])
      if e["id"] in unused and e["id"] != a["id"]
    ]
    candidates = partner_finder(a, candidates)
    if not candidates:
      continue
    b = rng.choice(candidates)
    del unused[a["id"]]
    del unused[b["id"]]
    spanning_pairs.append((a, b))
    b_room = (b["origin"]["north"], b["origin"]["east"])
    reached.add(b_room)
    remaining.discard(b_room)
    for e in by_room.get(b_room, []):
      if e["id"] in unused:
        frontier.append(e)
    rng.shuffle(frontier)

  print(
    f"  [{label}] spanning tree: {len(spanning_pairs)} pairs, "
    f"rooms reached: {len(reached)}/{len(pool_rooms)}"
    + (f" ({len(pre_reached)} pre-seeded)" if pre_reached else "")
  )
  if remaining:
    print(
      f"  [{label}] WARNING: {len(remaining)} rooms unreachable within "
      f"this pool: {sorted(remaining)[:10]}"
    )

  # leftover pairing among whatever's left unused
  leftover = list(unused.values())
  rng.shuffle(leftover)
  extra_pairs = []
  still_unpaired = []
  while leftover:
    a = leftover.pop()
    candidates = partner_finder(a, leftover)
    if not candidates:
      still_unpaired.append(a)
      continue
    b = rng.choice(candidates)
    leftover.remove(b)
    extra_pairs.append((a, b))

  print(
    f"  [{label}] extra pairs: {len(extra_pairs)}, "
    f"unpaired leftovers (self-loop): {len(still_unpaired)}"
  )

  return spanning_pairs + extra_pairs, still_unpaired, reached


def edge_partner_finder(a, candidates):
  want = OPPOSITE[a["direction"]]
  return [c for c in candidates if c["direction"] == want]


def door_partner_finder(a, candidates):
  return candidates # no constraint


edge_pairs, edge_unpaired, edge_reached = build_spanning_tree(
  edge_exits, edge_partner_finder, "edges"
)
door_pairs, door_unpaired, door_reached = build_spanning_tree(
  door_exits, door_partner_finder, "doors", seed_reached=edge_reached
)

all_pairs = edge_pairs + door_pairs
all_unpaired = edge_unpaired + door_unpaired

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

for a in all_unpaired:
  connections.append(make_connection(a, a))
  if len(all_unpaired) <= 10:
    print(f"  self-loop (unpaired): {a['id']}")

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
# Verify connectivity by BFS over the shuffled graph (combined edges+doors)
# ---------------------------------------------------------------------------
adj = {}
for c in connections:
  adj.setdefault((c["originNorth"], c["originEast"]), []).append(
    (c["newDestNorth"], c["newDestEast"])
  )

start_room = next(iter(edge_reached)) if edge_reached else next(iter(rooms))
visited = {start_room}
queue = [start_room]
while queue:
  cur = queue.pop()
  for nxt in adj.get(cur, []):
    if nxt not in visited:
      visited.add(nxt)
      queue.append(nxt)

print(
  f"\nBFS reachability check from {start_room}: {len(visited)}/{len(rooms)} rooms reachable"
)
unreachable = rooms - visited
if unreachable:
  print(f"  UNREACHABLE: {sorted(unreachable)}")
else:
  print("  All rooms reachable. Map is fully connected.")
