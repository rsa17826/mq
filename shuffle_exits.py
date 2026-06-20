"""
Coupled entrance-rando shuffle over exits.json with multi-gap support.
Includes dead-end protection and safer inner-screen padding offsets.
With progression logic validation to prevent softlocks.
"""

import json
import random
import sys, os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 12345

OPPOSITE = {"north": "south", "south": "north", "east": "west", "west": "east"}

# Updated Grid layout pixel dimensions
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
      gaps = [gaps]

    if not gaps:
      geometry_dropped += len(edge_list)
      continue

    # Create a separate shufflable warp for each gap item listed
    for i, gap in enumerate(gaps):
      base_edge = edge_list[i] if i < len(edge_list) else edge_list[0]
      new_e = dict(base_edge)
      if i >= len(edge_list):
        new_e["id"] = f"{base_edge['id']}_gap_{i}"

      # Pushed inward slightly away from borders to avoid boundary re-triggers
      if direction == "north":
        mid_block_x = (gap["left"] + gap["right"]) / 2
        new_e["src_coord"] = mid_block_x * BLOCK_W
        new_e["dest_x"] = mid_block_x * BLOCK_W
        new_e["dest_y"] = 1.5 * BLOCK_H # Pushed down safely into row 1
      elif direction == "south":
        mid_block_x = (gap["left"] + gap["right"]) / 2
        new_e["src_coord"] = mid_block_x * BLOCK_W
        new_e["dest_x"] = mid_block_x * BLOCK_W
        new_e["dest_y"] = 9.5 * BLOCK_H # Pushed up safely into row 9
      elif direction == "west":
        mid_block_y = (gap["top"] + gap["bottom"]) / 2
        new_e["src_coord"] = mid_block_y * BLOCK_H
        new_e["dest_x"] = 1.5 * BLOCK_W # Pushed right safely into col 1
        new_e["dest_y"] = mid_block_y * BLOCK_H
      elif direction == "east":
        mid_block_y = (gap["top"] + gap["bottom"]) / 2
        new_e["src_coord"] = mid_block_y * BLOCK_H
        new_e["dest_x"] = 12.5 * BLOCK_W # Pushed left safely into col 12
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

seen = {}
for e in all_exits_raw:
  seen[e["id"]] = e
all_exits = list(seen.values())

print(f"Total shufflable exits: {len(all_exits)}")

total_exits_per_room = {}
for e in all_exits:
  org = (e["origin"]["north"], e["origin"]["east"])
  total_exits_per_room[org] = total_exits_per_room.get(org, 0) + 1

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

  dead_ends = {r for r in pool_rooms if total_exits_per_room.get(r, 0) <= 1}
  hubs = pool_rooms - dead_ends

  if pre_reached:
    reached = set(pre_reached)
    frontier = [e for room in pre_reached for e in by_room.get(room, [])]
  else:
    rooms_list = list(hubs) if hubs else list(pool_rooms)
    rng.shuffle(rooms_list)
    start = rooms_list[0]
    reached = {start}
    frontier = list(by_room.get(start, []))
  rng.shuffle(frontier)

  spanning_pairs = []
  remaining = set(hubs if hubs else pool_rooms) - reached
  attempts = 0
  max_attempts = len(pool) * 10

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

  remaining_dead_ends = dead_ends - reached
  if remaining_dead_ends:
    for r in list(remaining_dead_ends):
      r_exits = [e for e in by_room.get(r, []) if e["id"] in unused]
      if not r_exits:
        continue
      a = r_exits[0]
      candidates = [
          e
          for room in reached
          for e in by_room.get(room, [])
          if e["id"] in unused and e["id"] != a["id"]
      ]
      candidates = partner_finder(a, candidates)
      if candidates:
        b = rng.choice(candidates)
        del unused[a["id"]]
        del unused[b["id"]]
        spanning_pairs.append((a, b))
        reached.add(r)

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
      "newY": to_exit.get("dest_y", 255),
      "srcCoord": from_exit.get("src_coord"),
      "direction": from_exit.get("direction"),
      "fromExitId": from_exit["id"],
      "toExitId": to_exit["id"],
  }


def validate_logic(connections_list, progression_data, shufflable_exits):
  # Build group aliases/item mapping
  item_groups = {}
  for item in progression_data.get("items", []):
    if "contains" in item:
      item_groups[item["id"]] = item["contains"]

  # Group progression components by room coordinates
  locations_by_room = {}
  for loc in progression_data.get("locations", []):
    if "room" in loc:
      r = (int(loc["room"]["north"]), int(loc["room"]["east"]))
      locations_by_room.setdefault(r, []).append(loc)

  trades_by_room = {}
  for trade in progression_data.get("trades", []):
    if "room" in trade:
      r = (int(trade["room"]["north"]), int(trade["room"]["east"]))
      trades_by_room.setdefault(r, []).append(trade)

  gates_by_room = {}
  for gate in progression_data.get("gates", []):
    if "room" in gate:
      r = (int(gate["room"]["north"]), int(gate["room"]["east"]))
      gates_by_room.setdefault(r, []).append(gate)

  # Build dictionary mapping an exit ID to its landing properties
  conn_map = {}
  for c in connections_list:
    conn_map[c["fromExitId"]] = (int(c["newDestNorth"]), int(c["newDestEast"]), c["toExitId"])

  # Group all shufflable exits by their room coordinates
  exits_by_room = {}
  for e in shufflable_exits:
    r = (int(e["origin"]["north"]), int(e["origin"]["east"]))
    exits_by_room.setdefault(r, []).append(e)

  def sub_item_list(val):
    if isinstance(val, list):
      return val
    return [val]

  # Check if DNF formula for item requirements is met
  def check_requires(requires, inventory):
    if not requires:
      return True
    for req_list in requires:
      all_satisfied = True
      for item_id in req_list:
        if item_id in inventory:
          continue
        if item_id in item_groups and any(g_item in inventory for g_item in item_groups[item_id]):
          continue
        all_satisfied = False
        break
      if all_satisfied:
        return True
    return False

  def exit_matches_gate_string(exit_obj, gate_str):
    if exit_obj["id"] == gate_str:
      return True
    if exit_obj["id"].startswith(gate_str + "_gap_"):
      return True
    if exit_obj.get("direction") == gate_str:
      return True
    if gate_str in exit_obj["id"]:
      return True
    return False

  # Establish default starting point from game initialization anchor
  start_room = (20, 20)
  if start_room not in exits_by_room:
    if exits_by_room:
      start_room = list(exits_by_room.keys())[0]
    else:
      return True

  reachable_exits = set()
  collected_items = set()
  used_trades = set()

  # Seed simulation with all entrances available from the starting room
  for e in exits_by_room.get(start_room, []):
    reachable_exits.add((start_room, e["id"]))

  # Fixed-point graph propagation loop
  changed = True
  while changed:
    changed = False
    reached_rooms = {room for (room, eid) in reachable_exits}

    # 1. Harvest items from reached locations and trades
    for r in reached_rooms:
      if r in locations_by_room:
        for loc in locations_by_room[r]:
          for item in loc.get("gives", []):
            if item not in collected_items:
              collected_items.add(item)
              changed = True

      if r in trades_by_room:
        for idx, trade in enumerate(trades_by_room[r]):
          trade_key = (r, idx)
          if trade_key not in used_trades:
            if all(item in collected_items for item in trade.get("give", [])):
              for item_entry in trade.get("receive", []):
                for sub in sub_item_list(item_entry):
                  if sub not in collected_items:
                    collected_items.add(sub)
                    changed = True
              used_trades.add(trade_key)
              changed = True

    # 2. Traverse randomized outer room boundaries/connections
    for (room, eid) in list(reachable_exits):
      if eid in conn_map:
        dest_n, dest_e, dest_eid = conn_map[eid]
        dest_room = (dest_n, dest_e)
        if (dest_room, dest_eid) not in reachable_exits:
          reachable_exits.add((dest_room, dest_eid))
          changed = True

    # 3. Propagate internally within each reached room through logic gates
    for room in reached_rooms:
      room_exits = exits_by_room.get(room, [])
      cur_reachable_in_room = [e for e in room_exits if (room, e["id"]) in reachable_exits]

      for src_exit in cur_reachable_in_room:
        for dest_exit in room_exits:
          if (room, dest_exit["id"]) in reachable_exits:
            continue

          blocked = False
          if room in gates_by_room:
            for gate in gates_by_room[room]:
              applies = False
              if exit_matches_gate_string(src_exit, gate["from"]) and exit_matches_gate_string(dest_exit, gate["to"]):
                applies = True
              elif gate.get("bidirectional", False) and exit_matches_gate_string(src_exit, gate["to"]) and exit_matches_gate_string(dest_exit, gate["from"]):
                applies = True

              if applies:
                if not check_requires(gate.get("requires", []), collected_items):
                  blocked = True
                  break

          if not blocked:
            reachable_exits.add((room, dest_exit["id"]))
            changed = True

  # Guarantee all locations can be completely reached/harvested
  for loc in progression_data.get("locations", []):
    for item in loc.get("gives", []):
      if item not in collected_items:
        return False
    if "room" in loc:
      r = (int(loc["room"]["north"]), int(loc["room"]["east"]))
      if r in exits_by_room:
        for e in exits_by_room[r]:
          if (r, e["id"]) not in reachable_exits:
            return False

  # Guarantee all trades can be completely completed and their rooms cleared
  for trade in progression_data.get("trades", []):
    for item_entry in trade.get("receive", []):
      for sub in sub_item_list(item_entry):
        if sub not in collected_items:
          return False
    if "room" in trade:
      r = (int(trade["room"]["north"]), int(trade["room"]["east"]))
      if r in exits_by_room:
        for e in exits_by_room[r]:
          if (r, e["id"]) not in reachable_exits:
            return False

  return True


# Load progression data for logic simulation validation
progression_path = os.path.join(OUT_DIR, "progression.json")
if os.path.exists(progression_path):
  with open(progression_path, "r") as f:
    progression_data = json.load(f)
  print("[+] Loaded progression.json for logic validation.")
else:
  progression_data = None
  print("NOTE: no progression.json found -- skipping verification.")

MAX_ATTEMPTS = 5000
connections = []

# Loop until a valid layout that avoids softlocks is discovered
for attempt in range(MAX_ATTEMPTS):
  edge_pairs, edge_unpaired, edge_reached = build_spanning_tree(
      edge_exits, edge_partner_finder, "edges"
  )
  door_pairs, door_unpaired, door_reached = build_spanning_tree(
      door_exits, door_partner_finder, "doors", seed_reached=edge_reached
  )

  all_pairs = edge_pairs + door_pairs
  all_unpaired = edge_unpaired + door_unpaired

  test_connections = []
  for a, b in all_pairs:
    test_connections.append(make_connection(a, b))
    test_connections.append(make_connection(b, a))

  for a in all_unpaired:
    test_connections.append(make_connection(a, a))

  if not progression_data or validate_logic(test_connections, progression_data, all_exits):
    connections = test_connections
    if progression_data:
      print(f"[+] Found valid non-softlocking layout on attempt {attempt + 1}!")
    break
else:
  print(f"[-] Warning: Could not find a valid layout after {MAX_ATTEMPTS} attempts. Proceeding with last shuffle.")
  connections = test_connections

out = {
    "seed": SEED,
    "connections": connections,
}
with open(f"{OUT_DIR}/connections.json", "w") as f:
  json.dump(out, f, indent=2)

print(f"Wrote connections.json with seed={SEED}")