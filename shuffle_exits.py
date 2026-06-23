"""
Coupled entrance-rando shuffle over json/exits.json with multi-gap support.
Includes dead-end protection and safer inner-screen padding offsets.
"""

import json
import random
import sys, os
def init():
  OUT_DIR = os.path.dirname(os.path.abspath(__file__))

  # Check for the --no-shuffle flag and strip it out to avoid breaking seed parsing
  NO_SHUFFLE = "--no-shuffle" in sys.argv
  clean_args = [arg for arg in sys.argv if arg != "--no-shuffle"]
  SEED = int(clean_args[1]) if len(clean_args) > 1 else 12345

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
    path = os.path.join(OUT_DIR, "json/room_geometry.json")
    if not os.path.exists(path):
      print(f"NOTE: no json/room_geometry.json found at {path} -- using fallback behavior.")
      return {}, {}
    raw = json.load(open(path))
    geo = {}
    room_areas = {}
    if isinstance(raw, list):
      for rec in raw:
        room = (float(rec["north"]), float(rec["east"]))
        geo[room] = rec["exits"]
        if rec.get("areas"):
          scenarios = []
          for sc in rec["areas"]:
            groups = [[(g["side"], g["idx"]) for g in group] for group in sc["areas"]]
            scenarios.append({"requires": parse_requires(sc.get("reqs")), "groups": groups})
          room_areas[room] = scenarios
    elif isinstance(raw, dict):
      for k, v in raw.items():
        n_str, e_str = k.split("_")
        room = (float(n_str), float(e_str))
        geo[room] = v.get("exits", v)
        if v.get("areas"):
          scenarios = []
          for sc in v["areas"]:
            groups = [[(g["side"], g["idx"]) for g in group] for group in sc["areas"]]
            scenarios.append({"requires": parse_requires(sc.get("reqs")), "groups": groups})
          room_areas[room] = scenarios
    else:
      raise ValueError("json/room_geometry.json must be a list or dict")
    return geo, room_areas


  REQUIREMENT_PREFIXES = {
    "entrance", "item", "skill", "permit", "quest", "weapon", "armor",
    "ring", "magic", "food", "drop", "misc",
  }


  def parse_requirement_token(tok):
    """Parse one requirement token into a structured dict."""
    if tok.strip("?") == "":
      return {"raw": tok, "type": "flag", "name": tok, "placeholder": True}

    if tok.startswith("entrance."):
      return {"raw": tok, "type": "entrance", "value": tok[len("entrance."):]}

    if ":" in tok:
      prefix, rest = tok.split(":", 1)
      if prefix in REQUIREMENT_PREFIXES:
        result = {"raw": tok, "type": prefix}
        placeholder = "?" in rest
        if placeholder:
          rest = rest[:-1]
          result["placeholder"] = True
        if "#" in rest:
          name, count_str = rest.rsplit("#", 1)
          result["name"] = name
          if count_str.lower() in ("inf", "infinite"):
            result["count"] = 999999999999
            result["is_infinite"] = True
          else:
            try:
              result["count"] = int(count_str)
            except ValueError:
              result["count"] = None
              if not placeholder:
                result["parse_warning"] = f"could not parse count from {tok!r}"
        elif "." in rest:
          name, tier_str = rest.rsplit(".", 1)
          result["name"] = name
          if tier_str.lower() in ("inf", "infinite"):
            result["tier"] = float("inf")
            result["is_infinite"] = True
          else:
            try:
              result["tier"] = int(tier_str)
            except ValueError:
              result["tier"] = None
              if not placeholder:
                result["parse_warning"] = f"could not parse tier from {tok!r}"
        else:
          result["name"] = rest
          result["count"] = 1
        return result
    if "?" in tok:
      return {"raw": tok, "type": "flag", "name": tok, "placeholder":True}
    return {"raw": tok, "type": "flag", "name": tok}


  def parse_requires(requires):
    if not requires:
      return []
    return [[parse_requirement_token(t) for t in group] for group in requires]


  def load_progression():
    path = os.path.join(OUT_DIR, "json/progression.json")
    if not os.path.exists(path):
      print(f"NOTE: no json/progression.json found at {path} -- no item/skill gating loaded.")
      return {"locations": [], "gates": [], "warps": []}
    raw = json.load(open(path))

    locations = []
    for loc in raw.get("locations", []):
      locations.append(
        {
          "room": (loc["room"]["north"], loc["room"]["east"]),
          "receive": loc.get("receive", []),
          "requires": parse_requires(loc.get("requires")),
          "raw": loc,
        }
      )

    gates = []
    for g in raw.get("gates", []):
      gates.append(
        {
          "room": (g["room"]["north"], g["room"]["east"]),
          "from": g["from"],
          "to": g["to"],
          "bidirectional": g.get("bidirectional", True),
          "requires": parse_requires(g.get("requires")),
          "raw": g,
        }
      )

    warps = []
    for w in raw.get("warps", []):
      rooms = [(r["north"], r["east"]) for r in w["rooms"]]
      warps.append(
        {
          "id": w.get("id", f"warp:{rooms[0][0]}_{rooms[0][1]}:{rooms[1][0]}_{rooms[1][1]}"),
          "rooms": rooms,
          "bidirectional": w.get("bidirectional", True),
          "requires": parse_requires(w.get("requires")),
          "raw": w,
        }
      )

    warnings = []
    flags_seen = set()
    placeholders_seen = set()
    for entry in locations + gates + warps:
      for group in entry["requires"]:
        for tok in group:
          if tok.get("placeholder"):
            placeholders_seen.add(tok["raw"])
            continue
          if "parse_warning" in tok:
            warnings.append((entry.get("room", entry.get("rooms")), tok["raw"], tok["parse_warning"]))
          if tok["type"] == "flag":
            flags_seen.add(tok["raw"])

    print(f"Loaded json/progression.json: {len(locations)} locations, {len(gates)} gates, {len(warps)} warps")
    with_req = sum(1 for l in locations if l["requires"])
    print(f"  locations with requirements: {with_req} / {len(locations)}")
    return {"locations": locations, "gates": gates, "warps": warps}


  exits_data = json.load(open(f"{OUT_DIR}/json/exits.json"))
  geometry, room_areas = load_room_geometry()
  progression = load_progression()

  edges_by_room_dir = {}
  for e in exits_data["edges"]:
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
      if gaps is None:
        gaps = []
      elif isinstance(gaps, dict):
        gaps = [gaps]

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
          if (gap["left"] + gap["right"])%2==1:
            new_e['xIsEven']=(BLOCK_W/2)
        elif direction == "south":
          mid_block_x = (gap["left"] + gap["right"]) / 2
          new_e["src_coord"] = mid_block_x * BLOCK_W
          new_e["dest_x"] = mid_block_x * BLOCK_W
          new_e["dest_y"] = 10 * BLOCK_H
          if (gap["left"] + gap["right"])%2==1:
            new_e['xIsEven']=(BLOCK_W/2)
        elif direction == "west":
          mid_block_y = (gap["top"] + gap["bottom"]) / 2
          new_e["src_coord"] = mid_block_y * BLOCK_H
          new_e["dest_x"] = 0 * BLOCK_W
          new_e["dest_y"] = mid_block_y * BLOCK_H
          if (gap["top"] + gap["bottom"])%2==1:
            new_e["yIsEven"]=(BLOCK_H/2)
        elif direction == "east":
          mid_block_y = ((gap["top"] + gap["bottom"]) / 2)
          new_e["src_coord"] = mid_block_y * BLOCK_H
          new_e["dest_x"] = 13 * BLOCK_W
          new_e["dest_y"] = mid_block_y * BLOCK_H
          if (gap["top"] + gap["bottom"])%2==1:
            new_e["yIsEven"]=(BLOCK_H/2)
        if 'newY' in gap:
          new_e['dest_y'] = gap.get("newY")
        if 'newX' in gap:
          new_e['dest_x'] = gap.get("newX")
        all_exits_raw.append(new_e)
    else:
      for e in edge_list:
        e = dict(e)
        e.setdefault("gap_index", 0)
        all_exits_raw.append(e)

  for d in exits_data["doors"]:
    if d.get("gated") or d.get("needs_review"):
      continue
    all_exits_raw.append(d)

  WARP_FALLBACK_X = 710 / 2
  WARP_FALLBACK_Y = 560 / 2

  for w in progression["warps"]:
    rooms = w["rooms"]
    sides = rooms if w["bidirectional"] else rooms[:1]
    for i, room in enumerate(sides):
      other = rooms[1] if room == rooms[0] else rooms[0]
      all_exits_raw.append(
        {
          "id": f"door:{w['id']}:{room[0]}_{room[1]}_{other[0]}_{other[1]}",
          "mechanism": "warp",
          "origin": {"north": room[0], "east": room[1]},
          "dest": {"north": other[0], "east": other[1]},
          "dest_x": WARP_FALLBACK_X,
          "dest_y": WARP_FALLBACK_Y,
          "requires": w["requires"],
        }
      )

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
  warp_exits = [e for e in all_exits if e["mechanism"] == "warp"]
  door_exits = [e for e in all_exits if e["mechanism"] not in ("edge", "warp")]

  locations_by_room = {}
  for loc in progression["locations"]:
    locations_by_room.setdefault(loc["room"], []).append(loc)

  def fmt_coord(n):
    return str(int(n)) if n == int(n) else str(n)

  def entrance_key(room, entrance_value):
    return f"{fmt_coord(room[0])}.{fmt_coord(room[1])}.entrance.{entrance_value}"

  def token_satisfied(tok, have, room):
    if tok.get("placeholder"):
      return True
    if tok["type"] == "entrance":
      return have.get(entrance_key(room, tok["value"]), 0) >= 1
    key = (tok["type"], tok.get("name"))
    needed = tok.get("count") or tok.get("tier") or 1
    return have.get(key, 0) >= needed

  def group_satisfied(group, have, room):
    return all(token_satisfied(tok, have, room) for tok in group)

  def requires_satisfied(requires_groups, have, room):
    if not requires_groups:
      return True
    return any(group_satisfied(g, have, room) for g in requires_groups)

  def token_key(tok):
    return (tok["type"], tok.get("name"))

  def resolved_key(tok, room):
    if tok["type"] == "entrance":
      return entrance_key(room, tok["value"])
    return token_key(tok)

  def apply_gives(receive_raw, have):
    updated = []
    for raw_tok in receive_raw:
      tok = parse_requirement_token(raw_tok)
      key = token_key(tok)
      amount = tok.get("count") or tok.get("tier") or 1
      if amount > have.get(key, 0):
        have[key] = amount
        updated.append(key)
    return updated

  pending = {}
  location_pending_keys = {}

  def missing_token_keys(requires_groups, have, room):
    missing = set()
    for group in requires_groups:
      for tok in group:
        if not token_satisfied(tok, have, room):
          missing.add(resolved_key(tok, room))
    return missing

  def try_grant_location(loc, have):
    room = loc["room"]
    if requires_satisfied(loc["requires"], have, room):
      updated = apply_gives(loc.get("receive", []), have)
      regs = location_pending_keys.pop(id(loc), None)
      if regs:
        for k in regs:
          lst = pending.get(k)
          if lst and loc in lst:
            lst.remove(loc)
            if not lst:
              del pending[k]
      return updated
    else:
      missing = missing_token_keys(loc["requires"], have, room)
      location_pending_keys[id(loc)] = missing
      for k in missing:
        bucket = pending.setdefault(k, [])
        if loc not in bucket:
          bucket.append(loc)
      return None

  def propagate(updated_keys, have):
    worklist = list(updated_keys)
    while worklist:
      key = worklist.pop()
      for loc in list(pending.get(key, [])):
        result = try_grant_location(loc, have)
        if result:
          worklist.extend(result)

  def mark_reached(room, reached_set, have):
    is_new = room not in reached_set
    reached_set.add(room)
    if is_new:
      for loc in locations_by_room.get(room, []):
        result = try_grant_location(loc, have)
        if result:
          propagate(result, have)

  def mark_entrance_used(exit_obj, have):
    if exit_obj["mechanism"] != "edge":
      return
    room = (exit_obj["origin"]["north"], exit_obj["origin"]["east"])
    key = entrance_key(room, f"{exit_obj['direction']}{exit_obj.get('gap_index', 0)}")
    if have.get(key, 0) < 1:
      have[key] = 1
      propagate([key], have)

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

    for sc in scenarios:
      if not requires_satisfied(sc["requires"], have, room):
        continue
      for group in sc["groups"]:
        for p in group:
          parent.setdefault(p, p)
        for p in group[1:]:
          union(group[0], p)
    return find(target)

  def room_reachable_internally(exit_obj, have):
    if exit_obj["mechanism"] != "edge":
      return True
    room = (exit_obj["origin"]["north"], exit_obj["origin"]["east"])
    if room not in room_areas:
      return True
    side, idx = exit_obj["direction"], exit_obj.get("gap_index", 0)
    marked = [
      (s, i) for (s, i) in known_room_exits.get(room, set())
      if have.get(entrance_key(room, f"{s}{i}"), 0) >= 1
    ]
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
      if not requires_satisfied(a.get("requires"), playercouldhave, a_room) or not room_reachable_internally(a, playercouldhave):
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
    vdest = vanilla_dest_key(from_exit)
    requires_groups = from_exit.get("requires") or []
    requires_raw = [[tok["raw"] for tok in group] for group in requires_groups]
    return {
      "originNorth": origin["north"],
      "originEast": origin["east"],
      "vanillaDestNorth": vdest[0],
      "vanillaDestEast": vdest[1],
      "newDestNorth": to_exit["origin"]["north"],
      "newDestEast": to_exit["origin"]["east"],
      "newX": to_exit.get("dest_x", 330),
      "newY": to_exit.get("dest_y", 255),
      "xIsEven": to_exit.get("xIsEven",0),
      "yIsEven": to_exit.get("yIsEven",0),
      "srcCoord": from_exit.get("src_coord"),
      "direction": from_exit.get("direction"),
      "mechanism": from_exit["mechanism"],
      "requires": requires_raw,
      "fromExitId": from_exit["id"],
      "toExitId": to_exit["id"],
    }

  # --- Connection Logic Split ---
  if NO_SHUFFLE:
    print("Vanilla mode requested: mapping exits directly to original layout targets.")
    all_rooms = {(e['origin']['north'], e['origin']['east']) for e in all_exits}
    edge_reached = all_rooms
    door_reached = all_rooms
    warp_reached = all_rooms

    # Pre-populate state for validation logs
    for e in all_exits:
      r = (e["origin"]["north"], e["origin"]["east"])
      mark_reached(r, edge_reached, playercouldhave)
      mark_entrance_used(e, playercouldhave)

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
          candidates.sort(key=lambda x: abs(x.get("src_coord", 0) - a.get("src_coord", 0)))
          partner = candidates[0]
        else:
          # For doors/warps, default to the matching target candidate
          partner = candidates[0]

      if partner:
        connections.append(make_connection(a, partner))
      else:
        connections.append(make_connection(a, a))
  else:
    edge_pairs, edge_unpaired, edge_reached = build_spanning_tree(
      edge_exits, edge_partner_finder, "edges"
    )
    door_pairs, door_unpaired, door_reached = build_spanning_tree(
      door_exits, door_partner_finder, "doors", seed_reached=edge_reached
    )
    warp_pairs, warp_unpaired, warp_reached = build_spanning_tree(
      warp_exits, door_partner_finder, "warps", seed_reached=edge_reached
    )

    all_pairs = edge_pairs + door_pairs + warp_pairs
    all_unpaired = edge_unpaired + door_unpaired + warp_unpaired

    for a, b in all_pairs:
      connections.append(make_connection(a, b))
      connections.append(make_connection(b, a))

    for a in all_unpaired:
      connections.append(make_connection(a, a))

  print(f"playercouldhave (final, accumulated across all pools): {len(playercouldhave)} distinct items/skills/permits tracked")

  all_reached = edge_reached | door_reached | warp_reached
  all_rooms = {(e['origin']['north'], e['origin']['east']) for e in all_exits}
  unreached_rooms = all_rooms - all_reached
  if unreached_rooms:
    print(f"  {len(unreached_rooms)} room(s) never reached: {sorted(unreached_rooms)[:10]}")

  out = {
    "seed": SEED if not NO_SHUFFLE else "vanilla",
    "connections": connections,
  }
  with open(f"{OUT_DIR}/json/connections.json", "w") as f:
    json.dump(out, f, indent=2)

  print(f"Wrote json/connections.json")

  def room_key_str(room):
    return f"{fmt_coord(room[0])}_{fmt_coord(room[1])}"

  def have_key_str(k):
    return f"{k[0]}:{k[1]}" if isinstance(k, tuple) else k

  graph = {}
  for c in connections:
    room_str = f"{fmt_coord(c['originNorth'])}_{fmt_coord(c['originEast'])}"
    graph.setdefault(room_str, []).append(
      {
        "toRoom": f"{fmt_coord(c['newDestNorth'])}_{fmt_coord(c['newDestEast'])}",
        "exitId": c["fromExitId"],
        "viaExitId": c["toExitId"],
        "mechanism": c["mechanism"],
        "direction": c.get("direction"),
        "requires": c["requires"],
      }
    )

  locations_out = []
  item_give_index = {}
  for loc in progression["locations"]:
    room_str = room_key_str(loc["room"])
    requires_raw = [[tok["raw"] for tok in group] for group in loc["requires"]]
    receive_raw = loc.get("receive", [])
    locations_out.append({"room": room_str, "requires": requires_raw, "receive": receive_raw})
    for raw_tok in receive_raw:
      tok = parse_requirement_token(raw_tok)
      key_str = have_key_str(token_key(tok))
      item_give_index.setdefault(key_str, []).append({"room": room_str, "raw": raw_tok})

  entrance_index = {}
  for e in edge_exits:
    room = (e["origin"]["north"], e["origin"]["east"])
    ent_value = f"{e['direction']}{e.get('gap_index', 0)}"
    key = entrance_key(room, ent_value)
    entrance_index[key] = {
      "exitId": e["id"],
      "room": room_key_str(room),
      "direction": e["direction"],
      "gapIndex": e.get("gap_index", 0),
    }

  final_have = {have_key_str(k): v for k, v in playercouldhave.items()}
  pending_out = {
    have_key_str(k): [room_key_str(loc["room"]) for loc in locs]
    for k, locs in pending.items()
  }

  hint_data = {
    "seed": SEED if not NO_SHUFFLE else "vanilla",
    "graph": graph,
    "locations": locations_out,
    "itemGiveIndex": item_give_index,
    "entranceIndex": entrance_index,
    "finalState": {
      "playercouldhave": final_have,
      "unresolvedPending": pending_out,
    },
  }
  with open(f"{OUT_DIR}/json/hint_data.json", "w") as f:
    json.dump(hint_data, f, indent=2)

  print('total distinct rooms across all exit pools:', len(all_rooms))
  filtered_keys = [k for k in playercouldhave.keys() if "entrance" not in k]
  sorted_keys = sorted(filtered_keys, key=lambda x: x[0])
  print('edge_reached:', len(edge_reached))
  print('door_reached:', len(door_reached))
  print('warp_reached:', len(warp_reached))
  return (playercouldhave, edge_reached, door_reached, warp_reached, all_rooms)

if __name__ == "__main__":
  init()