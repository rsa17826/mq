"""
Coupled entrance-rando shuffle over exits.json with multi-gap support.
Includes dead-end protection and safer inner-screen padding offsets.
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
        try:
          result["count"] = int(count_str)
        except ValueError:
          result["count"] = None
          if not placeholder:
            result["parse_warning"] = f"could not parse count from {tok!r}"
      elif "." in rest:
        name, tier_str = rest.rsplit(".", 1)
        result["name"] = name
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
        "gives": loc.get("gives", []),
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
geometry = load_room_geometry()
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
      print([*map(lambda x:x['id'],edge_list)])
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
    "newY": to_exit.get("dest_y", 255),
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