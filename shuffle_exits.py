"""
Coupled entrance-rando shuffle over exits.json with multi-gap support.
"""

import json
import random
import sys, os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 12345

OPPOSITE = {"north": "south", "south": "north", "east": "west", "west": "east"}

# Grid layout pixel conversions
BLOCK_W = 710 / 14 # 14 blocks horizontally (0-13)
BLOCK_H = 560 / 11 # 11 blocks vertically (0-10)


def load_room_geometry():
  path = os.path.join(OUT_DIR, "room_geometry.json")
  if not os.path.exists(path):
    print(f"NOTE: no room_geometry.json found at {path} -- using fallback behavior.")
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
  return geo


exits_data = json.load(open(f"{OUT_DIR}/exits.json"))
geometry = load_room_geometry()

# Group vanilla edges by room and direction
edges_by_room_dir = {}
for e in exits_data["edges"]:
  if e.get("gated") or e.get("needs_review"):
    continue
  org = (e["origin"]["north"], e["origin"]["east"])
  edges_by_room_dir.setdefault((org, e["direction"]), []).append(e)

all_exits_raw = []
geometry_dropped = 0

# Parse edge gaps using array expansion
for (org, direction), edge_list in edges_by_room_dir.items():
  geo_room = geometry.get(org)
  if geo_room is not None:
    gaps = geo_room.get(direction, [])
    if gaps is None:
      gaps = []
    elif isinstance(gaps, dict):
      gaps = [gaps] # Backward compatibility for non-array objects

    if not gaps:
      geometry_dropped += len(edge_list)
      continue

    # Create a separate shufflable warp for each gap item listed
    for i, gap in enumerate(gaps):
      base_edge = edge_list[i] if i < len(edge_list) else edge_list[0]
      new_e = dict(base_edge)
      if i >= len(edge_list):
        new_e["id"] = f"{base_edge['id']}_gap_{i}"

      # Calculate precise block centers and convert to pixel coordinates
      if direction == "north":
        mid_block_x = (gap["left"] + gap["right"]) / 2
        new_e["src_coord"] = mid_block_x * BLOCK_W
        new_e["dest_x"] = mid_block_x * BLOCK_W
        new_e["dest_y"] = 0.5 * BLOCK_H # Centered on top block row 0
      elif direction == "south":
        mid_block_x = (gap["left"] + gap["right"]) / 2
        new_e["src_coord"] = mid_block_x * BLOCK_W
        new_e["dest_x"] = mid_block_x * BLOCK_W
        new_e["dest_y"] = 10.5 * BLOCK_H # Centered on bottom block row 10
      elif direction == "west":
        mid_block_y = (gap["top"] + gap["bottom"]) / 2
        new_e["src_coord"] = mid_block_y * BLOCK_H
        new_e["dest_x"] = 0.5 * BLOCK_W # Centered on leftmost block column 0
        new_e["dest_y"] = mid_block_y * BLOCK_H
      elif direction == "east":
        mid_block_y = (gap["top"] + gap["bottom"]) / 2
        new_e["src_coord"] = mid_block_y * BLOCK_H
        new_e["dest_x"] = 13.5 * BLOCK_W # Centered on rightmost block column 13
        new_e["dest_y"] = mid_block_y * BLOCK_H

      all_exits_raw.append(new_e)
  else:
    for e in edge_list:
      all_exits_raw.append(e)

for d in exits_data["doors"]:
  if d.get("gated") or d.get("needs_review"):
    continue
  all_exits_raw.append(d)

if geometry:
  print(f"Geometry filtering: dropped {geometry_dropped} missing openings.")

# Use explicit exit IDs to keep separate gap definitions from being merged
seen = {}
for e in all_exits_raw:
  seen[e["id"]] = e
all_exits = list(seen.values())

print(f"Total shufflable exits: {len(all_exits)}")

# Index exits per origin room
rooms = set()
exits_by_room = {}
for e in all_exits:
  org = (e["origin"]["north"], e["origin"]["east"])
  rooms.add(org)
  exits_by_room.setdefault(org, []).append(e)

rng = random.Random(SEED)
edge_exits = [e for e in all_exits if e["mechanism"] == "edge"]
door_exits = [e for e in all_exits if e["mechanism"] != "edge"]


def build_spanning_tree(pool, partner_finder, label, seed_reached=None):
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

  return spanning_pairs + extra_pairs, still_unpaired, reached


def edge_partner_finder(a, candidates):
  want = OPPOSITE[a["direction"]]
  return [c for c in candidates if c["direction"] == want]


def door_partner_finder(a, candidates):
  return candidates


edge_pairs, edge_unpaired, edge_reached = build_spanning_tree(
    edge_exits, edge_partner_finder, "edges"
)
door_pairs, door_unpaired, door_reached = build_spanning_tree(
    door_exits, door_partner_finder, "doors", seed_reached=edge_reached
)

all_pairs = edge_pairs + door_pairs
all_unpaired = edge_unpaired + door_unpaired

connections = []


def vanilla_dest_key(e):
  d = e["dest"]
  return (d["north"], d["east"])


def make_connection(from_exit, to_exit):
  origin = from_exit["origin"]
  vdest = vanilla_dest_key(from_exit)
  return {
      "originNorth": origin["north"],
      "originEast": origin["east"],
      "vanillaDestNorth": vdest[0],
      "vanillaDestEast": vdest[1],
      "newDestNorth": to_exit["origin"]["north"],
      "newDestEast": to_exit["origin"]["east"],
      "newX": to_exit.get("dest_x", 330),
      "newY": to_exit.get("dest_y", 260),
      "srcCoord": from_exit.get("src_coord"),
      "direction": from_exit.get("direction"),
      "fromExitId": from_exit["id"],
      "toExitId": to_exit["id"],
  }


for a, b in all_pairs:
  connections.append(make_connection(a, b))
  connections.append(make_connection(b, a))

for a in all_unpaired:
  connections.append(make_connection(a, a))

out = {
    "seed": SEED,
    "connections": connections,
}
with open(f"{OUT_DIR}/connections.json", "w") as f:
  json.dump(out, f, indent=2)

print(f"Wrote connections.json with seed={SEED}")