import re
from functools import partial as bind

"""
Coupled entrance-rando shuffle over json/exits.json with multi-gap support.
Includes dead-end protection and safer inner-screen padding offsets.
"""

import json
import os
import sys


def init():
  OUT_DIR = os.path.dirname(os.path.abspath(__file__))

  # Check for the --no-shuffle flag and strip it out to avoid breaking seed parsing

  OPPOSITE = {"north": "south", "south": "north", "east": "west", "west": "east"}

  # Updated Grid layout pixel dimensions
  BLOCK_W = 710 / 14 # 14 blocks horizontally (0-13)
  BLOCK_H = 560 / 11 # 11 blocks vertically (0-10)

  def load_room_geometry():
    """Returns (geo, room_areas):
    geo[(north,east)] = {"west": [...], "south": [...], "east": [...], "north": [...]}
      (the per-side gap arrays, as before)
    room_areas[(north,east)] = [{"requires": parsed_reqs, "groups": [[(side,idx),...],...]}, ...]
      (room-internal connectivity scenarios -- a room with no entry here
      has no internal gating data, treated as a single open floor plan)
    """
    from _room_geometry import GEOM

    geo = {}
    room_areas = {}
    for rec in GEOM:
      room = (float(rec["north"]), float(rec["east"]))
      geo[room] = rec["exits"]
      if rec.get("areas"):
        scenarios = []
        for sc in rec["areas"]:
          groups = [[(g["side"], g["idx"]) for g in group] for group in sc["areas"]]
          scenarios.append(
            {
              "groups": groups,
            }
          )
        room_areas[room] = scenarios
    return geo, room_areas

  from _exits import EXITS

  geometry, room_areas = load_room_geometry()

  edges_by_room_dir = {}
  for e in EXITS["edges"]:
    if e.get("gated") or e.get("needs_review"):
      continue
    org = (e["origin"]["north"], e["origin"]["east"])
    edges_by_room_dir.setdefault((org, e["direction"]), []).append(e)

  all_exits_raw = []
  geometry_dropped = 0

  for (org, direction), edge_list in edges_by_room_dir.items():
    geo_room = geometry.get(org)
    if geo_room is not None:
      gaps = geo_room.get(direction, [])

      if not gaps:
        geometry_dropped += len(edge_list)
        continue

      for i, gap in enumerate(gaps):
        base_edge = edge_list[i] if i < len(edge_list) else edge_list[0]
        new_e = dict(base_edge)
        new_e["gap_index"] = i
        if i >= len(edge_list):
          new_e["id"] = f"{base_edge['id']}_gap_{i}"

        if direction == "north":
          mid_block_x = (gap["left"] + gap["right"]) / 2
          new_e["src_coord"] = mid_block_x * BLOCK_W
          new_e["dest_x"] = mid_block_x * BLOCK_W
          new_e["dest_y"] = 0 * BLOCK_H
          if (gap["left"] + gap["right"]) % 2 == 1:
            new_e["xIsEven"] = BLOCK_W / 2
        elif direction == "south":
          mid_block_x = (gap["left"] + gap["right"]) / 2
          new_e["src_coord"] = mid_block_x * BLOCK_W
          new_e["dest_x"] = mid_block_x * BLOCK_W
          new_e["dest_y"] = 10 * BLOCK_H
          if (gap["left"] + gap["right"]) % 2 == 1:
            new_e["xIsEven"] = BLOCK_W / 2
        elif direction == "west":
          mid_block_y = (gap["top"] + gap["bottom"]) / 2
          new_e["src_coord"] = mid_block_y * BLOCK_H
          new_e["dest_x"] = 0 * BLOCK_W
          new_e["dest_y"] = mid_block_y * BLOCK_H
          if (gap["top"] + gap["bottom"]) % 2 == 1:
            new_e["yIsEven"] = BLOCK_H / 2
        elif direction == "east":
          mid_block_y = (gap["top"] + gap["bottom"]) / 2
          new_e["src_coord"] = mid_block_y * BLOCK_H
          new_e["dest_x"] = 13 * BLOCK_W
          new_e["dest_y"] = mid_block_y * BLOCK_H
          if (gap["top"] + gap["bottom"]) % 2 == 1:
            new_e["yIsEven"] = BLOCK_H / 2
        if "newY" in gap:
          new_e["dest_y"] = gap.get("newY")
        if "newX" in gap:
          new_e["dest_x"] = gap.get("newX")
        new_e["idx"] = i
        all_exits_raw.append(new_e)
    else:
      for e in edge_list:
        e = dict(e)
        all_exits_raw.append(e)

  # for w in progression["warps"]:
  #   rooms = w["rooms"]
  #   sides = rooms if w["bidirectional"] else rooms[:1]
  #   for i, room in enumerate(sides):
  #     other = rooms[1] if room == rooms[0] else rooms[0]
  #     all_exits_raw.append(
  #       {
  #         "id": f"door:{w['id']}:{room[0]}_{room[1]}_{other[0]}_{other[1]}",
  #         "mechanism": "warp",
  #         "origin": {"north": room[0], "east": room[1]},
  #         "dest": {"north": other[0], "east": other[1]},
  #         "dest_x": WARP_FALLBACK_X,
  #         "dest_y": WARP_FALLBACK_Y,
  #         "requires": w["requires"],
  #       }
  #     )

  seen = {}
  for e in all_exits_raw:
    seen[e["id"]] = e
  all_exits = list(seen.values())

  total_exits_per_room = {}
  for e in all_exits:
    org = (e["origin"]["north"], e["origin"]["east"])
    total_exits_per_room[org] = total_exits_per_room.get(org, 0) + 1

  edge_exits = [e for e in all_exits if e["mechanism"] == "edge"]

  def fmt_coord(n):
    return str(int(n)) if n == int(n) else str(n)

  def entrance_key(room, entrance_value):
    return f"{fmt_coord(room[0])}.{fmt_coord(room[1])}.entrance.{entrance_value}"

  known_room_exits = {}
  for room, sides in geometry.items():
    pairs = set()
    for side in ("north", "south", "east", "west"):
      for idx in range(len(sides.get(side, []))):
        pairs.add((side, idx))
    known_room_exits[room] = pairs

  def room_group_of(room, side, idx, have):
    scenarios = room_areas.get(room)
    target = (side, idx)
    if not scenarios:
      return room
    parent = {p: p for p in known_room_exits.get(room, {target})}
    parent.setdefault(target, target)

    def find(p):
      while parent[p] != p:
        p = parent[p]
      return p

    def union(p, q):
      rp, rq = find(p), find(q)
      if rp != rq:
        parent[rp] = rq

    return find(target)

  def room_reachable_internally(exit_obj, have):
    if exit_obj["mechanism"] != "edge":
      return True
    room = (exit_obj["origin"]["north"], exit_obj["origin"]["east"])
    if room not in room_areas:
      return True
    side, idx = exit_obj["direction"], exit_obj.get("gap_index", 0)
    marked = [(s, i) for (s, i) in known_room_exits.get(room, set()) if have.get(entrance_key(room, f"{s}{i}"), 0) >= 1]
    if not marked:
      return True
    my_group = room_group_of(room, side, idx, have)
    return any(room_group_of(room, s, i, have) == my_group for (s, i) in marked)

  playercouldhave = {}

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
      for r in pre_reached:
        mark_reached(r, reached, playercouldhave)
      frontier = [e for room in pre_reached for e in by_room.get(room, [])]
    else:
      rooms_list = list(hubs) if hubs else list(pool_rooms)
      rng.shuffle(rooms_list)
      start = rooms_list[0]
      reached = {start}
      mark_reached(start, reached, playercouldhave)
      frontier = list(by_room.get(start, []))
    rng.shuffle(frontier)

    spanning_pairs = []
    remaining = set(hubs if hubs else pool_rooms) - reached
    attempts = 0
    max_attempts = len(pool) * 10

    while remaining and attempts < max_attempts:
      attempts += 1
      if not frontier:
        frontier = [e for room in reached for e in by_room.get(room, []) if e["id"] in unused]
        rng.shuffle(frontier)
        if not frontier:
          break
      a = frontier.pop()
      if a["id"] not in unused:
        continue
      a_room = (a["origin"]["north"], a["origin"]["east"])
      if not requires_satisfied(a.get("requires"), playercouldhave, a_room) or not room_reachable_internally(
        a, playercouldhave
      ):
        continue

      candidates = [e for room in remaining for e in by_room.get(room, []) if e["id"] in unused and e["id"] != a["id"]]
      candidates = partner_finder(a, candidates)
      if not candidates:
        continue

      b = rng.choice(candidates)
      del unused[a["id"]]
      del unused[b["id"]]
      spanning_pairs.append((a, b))
      mark_entrance_used(a, playercouldhave)
      mark_entrance_used(b, playercouldhave)
      b_room = (b["origin"]["north"], b["origin"]["east"])
      mark_reached(b_room, reached, playercouldhave)
      remaining.discard(b_room)
      for e in by_room.get(b_room, []):
        if e["id"] in unused:
          frontier.append(e)
      rng.shuffle(frontier)

    return spanning_pairs, list(unused.values()), reached

  def edge_partner_finder(a, candidates):
    want = OPPOSITE[a["direction"]]
    return [c for c in candidates if c["direction"] == want]

  def door_partner_finder(a, candidates):
    return candidates

  connections = []

  def vanilla_dest_key(e):
    d = e["dest"]
    return (d["north"], d["east"])

  def make_connection(from_exit, to_exit):
    origin = from_exit["origin"]
    print(f'"north": {origin["north"]},\\n.*"east": {origin["east"]},[\\s\\S]*?"exits":[\\s\\S]*?{from_exit.get("direction")}')
    print(from_exit.get("idx"), from_exit.get("direction"))
    print(
      {
        "newX": int(to_exit.get("dest_x", 330)),
        "newY": int(to_exit.get("dest_y", 255)),
      }
    )

  # --- Connection Logic Split ---
  all_rooms = {(e["origin"]["north"], e["origin"]["east"]) for e in all_exits}

  for a in all_exits:
    partner = None
    candidates = []
    for b in all_exits:
      if b["id"] == a["id"]:
        continue
      if b["origin"]["north"] == a["dest"]["north"] and b["origin"]["east"] == a["dest"]["east"]:
        if a["mechanism"] == "edge" and b["mechanism"] == "edge":
          if b["direction"] == OPPOSITE[a["direction"]]:
            candidates.append(b)
        elif a["mechanism"] != "edge" and b["mechanism"] != "edge":
          if b["dest"]["north"] == a["origin"]["north"] and b["dest"]["east"] == a["origin"]["east"]:
            candidates.append(b)

    if candidates:
      if a["mechanism"] == "edge":
        # Match by the closest physical coordinate along the room border to prevent side-exit mixups
        # lastcandidates = [*candidates]
        candidates.sort(key=lambda x: abs(x.get("src_coord", 0) - a.get("src_coord", 0)))
        # if lastcandidates!=candidates:
        partner = candidates[0]
      else:
        # For doors/warps, default to the matching target candidate
        partner = candidates[0]

    if partner:
      connections.append(make_connection(a, partner))
    else:
      # TODO
      connections.append(make_connection(a, {**a}))

  all_rooms = {(e["origin"]["north"], e["origin"]["east"]) for e in all_exits}

  with open(f"{OUT_DIR}/json/connections.json", "w") as f:
    json.dump(connections, f, indent=2)

  def room_key_str(room):
    return f"{fmt_coord(room[0])}_{fmt_coord(room[1])}"

  def have_key_str(k):
    return f"{k[0]}:{k[1]}" if isinstance(k, tuple) else k

  entrance_index = {}
  for e in edge_exits:
    room = (e["origin"]["north"], e["origin"]["east"])
    ent_value = f"{e['direction']}{e.get('gap_index', 0)}"
    key = entrance_key(room, ent_value)

    entrance_index[key] = {
      "exitId": f'"north": {e["id"].split("_")[0]},\n.*"east": {e["id"].split("_")[1]},',
      "room": room_key_str(room),
      "direction": e["direction"],
      "gapIndex": e.get("gap_index", 0),
    }

  return (playercouldhave, all_rooms)


if __name__ == "__main__":
  init()
