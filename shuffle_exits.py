"""
Coupled entrance-rando shuffle over exits.json with multi-gap support.
Includes dead-end protection and safer inner-screen padding offsets.
"""

import json
import random
import sys, os
def init():
  OUT_DIR = os.path.dirname(os.path.abspath(__file__))
  SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 12345

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
    path = os.path.join(OUT_DIR, "room_geometry.json")
    if not os.path.exists(path):
      print(f"NOTE: no room_geometry.json found at {path} -- using fallback behavior.")
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
      raise ValueError("room_geometry.json must be a list or dict")
    return geo, room_areas


  REQUIREMENT_PREFIXES = {
    "entrance", "item", "skill", "permit", "quest", "weapon", "armor",
    "ring", "magic", "food", "drop", "misc",
  }


  def parse_requirement_token(tok):
    """Parse one requirement token into a structured dict. Token forms seen
    in progression.json:
      entrance.NAME            -- which exit was used to get here
      PREFIX:NAME#COUNT        -- need at least COUNT of an item-like thing
      PREFIX:NAME.TIER         -- need a tiered thing (skill/permit/quest/
        magic) at >= TIER (having a higher tier
        satisfies a lower-tier requirement)
      PREFIX:NAME              -- need the thing at all, count/tier unset
      NAME                     -- bare/unprefixed flag, taken as a literal
        opaque requirement (no known convention)
      ...with a trailing "?" on a tier/count, or a bare "???", meaning
      "real value not decided yet" -- parsed as a placeholder rather than
      a parse failure: the "?" is stripped and, if a number remains, it's
      used as a provisional value; either way the token is marked
      placeholder=True so callers can choose to ignore/flag it separately
      from genuine malformed data.
    Returns {"raw": tok, "type": ..., ...}. Never raises.
    """
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
            result["count"] = float("inf")
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
    # bare/unprefixed token -- opaque flag, no further structure assumed
    return {"raw": tok, "type": "flag", "name": tok}


  def parse_requires(requires):
    """requires is a list of AND-groups (lists of tokens); satisfying ANY
    one group is sufficient (OR between groups, AND within a group). None
    or [] both mean "no requirement" (always satisfiable)."""
    if not requires:
      return []
    return [[parse_requirement_token(t) for t in group] for group in requires]


  def load_progression():
    path = os.path.join(OUT_DIR, "progression.json")
    if not os.path.exists(path):
      print(f"NOTE: no progression.json found at {path} -- no item/skill gating loaded.")
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

    # visibility report: flag anything that didn't parse cleanly, and any
    # bare/unprefixed tokens so they can be reviewed/cleaned up upstream.
    # Placeholders ("?"-suffixed or bare "???") are pending-data markers,
    # not genuine issues -- reported separately, once, quietly.
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

    print(f"Loaded progression.json: {len(locations)} locations, {len(gates)} gates, {len(warps)} warps")
    with_req = sum(1 for l in locations if l["requires"])
    print(f"  locations with requirements: {with_req} / {len(locations)}")
    if placeholders_seen:
      print(f"  NOTE: {len(placeholders_seen)} placeholder token(s) (pending real data, ignored): "
        f"{sorted(placeholders_seen)}")
    if warnings:
      print(f"  WARNING: {len(warnings)} tokens failed to parse cleanly:")
      for room, raw, msg in warnings[:20]:
        print(f"    room {room}: {raw!r} -- {msg}")
    if flags_seen:
      print(f"  NOTE: {len(flags_seen)} bare/unprefixed tokens (no PREFIX: or "
        f"entrance. convention), passed through as opaque flags -- "
        f"review if these should use a real prefix:")
      for f in sorted(flags_seen)[:20]:
        print(f"    {f!r}")
      if len(flags_seen) > 20:
        print(f"    ... and {len(flags_seen) - 20} more")

    return {"locations": locations, "gates": gates, "warps": warps}



  exits_data = json.load(open(f"{OUT_DIR}/exits.json"))
  geometry, room_areas = load_room_geometry()
  progression = load_progression()

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
        new_e["gap_index"] = i
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
        e = dict(e)
        e.setdefault("gap_index", 0)
        all_exits_raw.append(e)

  for d in exits_data["doors"]:
    if d.get("gated") or d.get("needs_review"):
      continue
    all_exits_raw.append(d)

  # Warps (e.g. the magic water-warp spell): unlike doors, these aren't
  # extracted from game source -- they come straight from progression.json's
  # "warps" list, since some of these links (notably the room-(9,14) x-split
  # case) were never fully recoverable from the vanilla code at all. Each
  # warp produces one exit per room endpoint; requires travels WITH the
  # exit's origin (it's a property of casting the spell from that room, not
  # of whatever the vanilla/shuffled destination happens to be).
  WARP_FALLBACK_X = 710 / 2
  WARP_FALLBACK_Y = 560 / 2

  for w in progression["warps"]:
    rooms = w["rooms"]
    sides = rooms if w["bidirectional"] else rooms[:1]
    for i, room in enumerate(sides):
      other = rooms[1] if room == rooms[0] else rooms[0]
      all_exits_raw.append(
        {
          "id": f"{w['id']}:side{i}",
          "mechanism": "warp",
          "origin": {"north": room[0], "east": room[1]},
          "dest": {"north": other[0], "east": other[1]},
          "dest_x": WARP_FALLBACK_X,
          "dest_y": WARP_FALLBACK_Y,
          "requires": w["requires"],
        }
      )

  print(f"Warps: {len(progression['warps'])} defined -> {sum(len(w['rooms']) if w['bidirectional'] else 1 for w in progression['warps'])} exit endpoints")

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
  warp_exits = [e for e in all_exits if e["mechanism"] == "warp"]
  door_exits = [e for e in all_exits if e["mechanism"] not in ("edge", "warp")]


  # ---------------------------------------------------------------------------
  # Progression-aware reachability: the GAME already enforces requirements
  # (a gated warp/door simply won't work without the right items) -- nothing
  # for the runtime patch to do. What the shuffler needs to avoid is treating
  # a gated connection as part of the GUARANTEED-reachable backbone before
  # its requirement is actually satisfiable, which would create a shuffle-
  # introduced softlock that doesn't exist in vanilla.
  #
  # playercouldhave is a dict tracking what's currently obtainable:
  #   - (type, name) -> highest count/tier seen, for item/skill/permit/etc.
  #   - "N.E.entrance.directionI" -> 1, once that specific room+gap has been
  #     wired into the shuffle graph (so "entrance.south1" in a requirement
  #     attached to that same room resolves correctly -- see entrance_key()).
  #
  # Locations can depend on OTHER locations transitively (room A's pickup
  # needs an item that only comes from room B's pickup, which might itself
  # be gated). Rather than re-scan everything on every change, unresolved
  # locations get registered in `pending`, keyed by whichever (type,name)
  # token(s) are currently missing; satisfying a token re-checks only the
  # locations registered under it, and any newly-granted receive can itself
  # unblock further pending locations (a worklist, not a single pass).
  # ---------------------------------------------------------------------------

  locations_by_room = {}
  for loc in progression["locations"]:
    locations_by_room.setdefault(loc["room"], []).append(loc)


  def fmt_coord(n):
    return str(int(n)) if n == int(n) else str(n)


  def entrance_key(room, entrance_value):
    """room.entrance.directionN -- e.g. 19.17.entrance.south0. This is the
    key playercouldhave uses once THIS room's specific gap has been wired
    into the shuffle graph (paired with something, either direction)."""
    return f"{fmt_coord(room[0])}.{fmt_coord(room[1])}.entrance.{entrance_value}"


  def token_satisfied(tok, have, room):
    if tok.get("placeholder"):
      return True # pending real data -- never block progress on these
    if tok["type"] == "entrance":
      # entrance.south1 in a requirement attached to `room` means "you
      # entered THIS room via its south1 gap" -- qualify with room and
      # check the same key mark_entrance_used() sets when that gap gets
      # wired into the shuffle graph.
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
    """The key this token actually lives under in `have`/`pending` --
    entrance tokens use the room-qualified string key (entrance_key),
    everything else uses the plain (type, name) tuple."""
    if tok["type"] == "entrance":
      return entrance_key(room, tok["value"])
    return token_key(tok)


  def apply_gives(receive_raw, have):
    """Folds receive tokens into `have`, returning the list of (type,name)
    keys that actually changed (so callers can wake up anything pending on
    them). Doesn't handle entrance keys -- those are plain strings set
    directly by mark_entrance_used, never something a location "receives"."""
    updated = []
    for raw_tok in receive_raw:
      tok = parse_requirement_token(raw_tok)
      key = token_key(tok)
      amount = tok.get("count") or tok.get("tier") or 1
      if amount > have.get(key, 0):
        have[key] = amount
        updated.append(key)
    return updated


  pending = {}              # token_key -> [location, ...] currently blocked on it
  location_pending_keys = {} # id(location) -> set of token_keys it's registered under


  def missing_token_keys(requires_groups, have, room):
    """Union, across every OR-group, of the keys currently failing
    token_satisfied -- registering under all of them means this location
    gets re-checked no matter which one resolves first."""
    missing = set()
    for group in requires_groups:
      for tok in group:
        if not token_satisfied(tok, have, room):
          missing.add(resolved_key(tok, room))
    return missing


  def try_grant_location(loc, have):
    """Attempt to grant loc's receive now. Returns the list of (type,name)
    keys newly added to `have` if successful (possibly empty if it only
    grants entrance-style things, which doesn't happen via receive), or
    None if still blocked (and (re-)registers it in `pending`)."""
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
    """Worklist: a token just changed -> re-check whatever's pending on it
    -> granting those may change MORE tokens -> keep going until quiet."""
    worklist = list(updated_keys)
    while worklist:
      key = worklist.pop()
      for loc in list(pending.get(key, [])):
        result = try_grant_location(loc, have)
        if result:
          worklist.extend(result)


  def mark_reached(room, reached_set, have):
    """Add room to reached_set and, on first visit, attempt every one of
    its locations (granting + propagating, or registering as pending)."""
    is_new = room not in reached_set
    reached_set.add(room)
    if is_new:
      for loc in locations_by_room.get(room, []):
        result = try_grant_location(loc, have)
        if result:
          propagate(result, have)


  def mark_entrance_used(exit_obj, have):
    """Whenever an edge exit gets paired (either side -- pairing is always
    bidirectional), that specific room+direction+gap becomes a real,
    enterable entrance: anything waiting on "entrance.X" for that exact
    room+gap can now potentially proceed."""
    if exit_obj["mechanism"] != "edge":
      return # only edge exits have a direction+gap_index to qualify
    room = (exit_obj["origin"]["north"], exit_obj["origin"]["east"])
    key = entrance_key(room, f"{exit_obj['direction']}{exit_obj.get('gap_index', 0)}")
    if have.get(key, 0) < 1:
      have[key] = 1
      propagate([key], have)


  # ---------------------------------------------------------------------------
  # Room-internal connectivity (room_geometry.json's "areas" field): which of
  # a room's own exits are mutually walkable from each other isn't always a
  # given -- e.g. a bombable wall splits a room into two halves until you
  # have permit:bomb, at which point they merge into one. Each scenario lists
  # its own "reqs" (same OR-of-AND convention) and the resulting groups of
  # {side,idx} exits that are connected under it. A room's EFFECTIVE grouping
  # at any moment is the union of every CURRENTLY-satisfied scenario's groups
  # (scenarios don't replace each other, they layer on top -- the unconditional
  # scenario, reqs=[[]], is always active and acts as the baseline).
  #
  # Recomputed live (not cached) since which scenarios are active changes as
  # playercouldhave grows -- these are small per-room union-finds, cheap.
  # ---------------------------------------------------------------------------

  known_room_exits = {} # room -> set of (side, idx) pairs that exist per geometry
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
      return room # no internal gating data at all -- one open group
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
    """Is this exit usable right now FROM WITHIN its own room -- i.e. is it
    in the same live-computed connectivity group as some exit in that room
    that's already been entrance-marked? If NOTHING in the room has been
    marked yet, this exit would BE the first entrance, which is always
    allowed (nothing to be disconnected from yet) -- otherwise this check
    would permanently block a room's very first use of itself."""
    if exit_obj["mechanism"] != "edge":
      return True # area grouping only applies to geometry-based edges
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
      a_room = (a["origin"]["north"], a["origin"]["east"])
      if not requires_satisfied(a.get("requires"), playercouldhave, a_room) or not room_reachable_internally(a, playercouldhave):
        # not usable yet -- left in `unused` so it's retried once a
        # frontier refill picks it up again, by which point playercouldhave
        # may have grown enough to satisfy it
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
      mark_entrance_used(a, playercouldhave)
      mark_entrance_used(b, playercouldhave)
      b_room = (b["origin"]["north"], b["origin"]["east"])
      mark_reached(b_room, reached, playercouldhave)
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
        if not requires_satisfied(a.get("requires"), playercouldhave, r) or not room_reachable_internally(a, playercouldhave):
          continue # this dead-end's only exit is gated and not yet unlocked
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
          mark_entrance_used(a, playercouldhave)
          mark_entrance_used(b, playercouldhave)
          mark_reached(r, reached, playercouldhave)

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
      mark_entrance_used(a, playercouldhave)
      mark_entrance_used(b, playercouldhave)

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
  warp_pairs, warp_unpaired, warp_reached = build_spanning_tree(
    warp_exits, door_partner_finder, "warps", seed_reached=edge_reached
  )

  all_pairs = edge_pairs + door_pairs + warp_pairs
  all_unpaired = edge_unpaired + door_unpaired + warp_unpaired

  print(f"playercouldhave (final, accumulated across all pools): "
        f"{len(playercouldhave)} distinct items/skills/permits tracked")

  all_reached = edge_reached | door_reached | warp_reached
  all_rooms = set(edge_exits and {(e['origin']['north'], e['origin']['east']) for e in edge_exits} or set())
  all_rooms |= {(e['origin']['north'], e['origin']['east']) for e in door_exits}
  all_rooms |= {(e['origin']['north'], e['origin']['east']) for e in warp_exits}
  unreached_rooms = all_rooms - all_reached
  if unreached_rooms:
    print(f"  {len(unreached_rooms)} room(s) never reached (check above pool-specific "
          f"warnings for cause -- could be gating, could be exhausted exits): "
          f"{sorted(unreached_rooms)[:10]}")

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
      "srcCoord": from_exit.get("src_coord"),
      "direction": from_exit.get("direction"),
      "mechanism": from_exit["mechanism"],
      "requires": requires_raw,
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

  all_rooms = set()
  for e in edge_exits + door_exits + warp_exits:
      all_rooms.add((e['origin']['north'], e['origin']['east']))
  print('total distinct rooms across all exit pools:', len(all_rooms))

  print('playercouldhave:', playercouldhave)
  print('edge_reached:', len(edge_reached))
  print('door_reached:', len(door_reached))
  print('warp_reached:', len(warp_reached))
  all_reached = edge_reached | door_reached | warp_reached
  print('union reached:', len(all_reached))
  print('unreached:', len(all_rooms - all_reached))
  return (playercouldhave, edge_reached, door_reached, warp_reached, all_rooms)