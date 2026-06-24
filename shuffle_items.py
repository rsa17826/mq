"""
Coupled item-rando shuffle over json/progression.json with distinct
finite and infinite item pool isolation and progression-safe placement logic.
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
      print(f"ERROR: json/progression.json required but not found at {path}")
      sys.exit(1)
    raw = json.load(open(path))

    locations = []
    for i, loc in enumerate(raw.get("locations", [])):
      # Assign a unique location ID if not present
      loc_id = loc.get("id", f"loc_{i}_{loc['room']['north']}_{loc['room']['east']}")
      locations.append(
        {
          "id": loc_id,
          "room": (loc["room"]["north"], loc["room"]["east"]),
          "original_receive": loc.get("receive", []),
          "requires": parse_requires(loc.get("requires")),
          "raw": loc,
        }
      )
    return locations

  locations = load_progression()
  rng = random.Random(SEED)

  # --- Pool Splitting Logic ---
  finite_item_pool = []
  infinite_item_pool = []

  finite_locations = []
  infinite_locations = []

  for loc in locations:
    # Determine if this location yields infinite items based on its default contents
    is_infinite_loc = False
    for item_str in loc["original_receive"]:
      parsed = parse_requirement_token(item_str)
      if parsed.get("is_infinite"):
        is_infinite_loc = True
        break

    if is_infinite_loc:
      infinite_locations.append(loc)
      infinite_item_pool.extend(loc["original_receive"])
    else:
      finite_locations.append(loc)
      finite_item_pool.extend(loc["original_receive"])

  print(f"Loaded {len(locations)} total item locations:")
  print(f"  -> Finite Pool: {len(finite_locations)} locations, {len(finite_item_pool)} items")
  print(f"  -> Infinite Pool: {len(infinite_locations)} locations, {len(infinite_item_pool)} items")

  # --- Helper functions for logic evaluation ---
  def token_satisfied(tok, have):
    if tok.get("placeholder"):
      return True
    key = (tok["type"], tok.get("name"))
    needed = tok.get("count") or tok.get("tier") or 1
    return have.get(key, 0) >= needed

  def group_satisfied(group, have):
    return all(token_satisfied(tok, have) for tok in group)

  def requires_satisfied(requires_groups, have):
    if not requires_groups:
      return True
    return any(group_satisfied(g, have) for g in requires_groups)

  def apply_gives(items_list, have):
    for item_str in items_list:
      tok = parse_requirement_token(item_str)
      key = (tok["type"], tok.get("name"))
      amount = tok.get("count") or tok.get("tier") or 1
      if amount > have.get(key, 0):
        have[key] = amount

  # --- Shuffling & Placement Engine ---
  placements = {}

  if NO_SHUFFLE:
    print("Vanilla mode requested: keeping items in original locations.")
    for loc in locations:
      placements[loc["id"]] = loc["original_receive"]
  else:
    # 1. Shuffle Infinite Pool (Purely randomized, typically contains no gating items)
    rng.shuffle(infinite_item_pool)
    for loc in infinite_locations:
      # Pull items matching original quantity count
      count = len(loc["original_receive"])
      pulled_items = [infinite_item_pool.pop(0) for _ in range(count)]
      placements[loc["id"]] = pulled_items

    # 2. Shuffle Finite Pool using Assumed Fill progression-safety checks
    rng.shuffle(finite_item_pool)
    remaining_items = list(finite_item_pool)
    remaining_locations = list(finite_locations)

    while remaining_items:
      item_to_place = remaining_items.pop(0)

      # Step asset check: Can the game still be completed if this item is assumed
      # to be accessible, or do we have available open slots that don't trigger lockouts?
      # For a strict fill, we find locations whose current logic is satisfied.
      available_locs = []

      # Fast state verification: assume player has all remaining items to find reachable spots
      assumed_inventory = {}
      apply_gives(remaining_items, assumed_inventory)

      for loc in remaining_locations:
        if requires_satisfied(loc["requires"], assumed_inventory):
          available_locs.append(loc)

      if not available_locs:
        # Fallback to avoid complete deadlocks if progression definitions are tightly coiled
        available_locs = remaining_locations

      chosen_loc = rng.choice(available_locs)
      remaining_locations.remove(chosen_loc)

      placements.setdefault(chosen_loc["id"], []).append(item_to_place)

      # Handle cases where locations held multiple items originally
      while len(placements[chosen_loc["id"]]) < len(chosen_loc["original_receive"]) and remaining_items:
        placements[chosen_loc["id"]].append(remaining_items.pop(0))

  # --- Export formatting ---
  output_placements = []
  for loc in locations:
    output_placements.append({
      "locationId": loc["id"],
      "roomNorth": loc["room"][0],
      "roomEast": loc["room"][1],
      "originalItems": loc["original_receive"],
      "shuffledItems": placements.get(loc["id"], [])
    })

  out = {
    "seed": SEED if not NO_SHUFFLE else "vanilla",
    "placements": output_placements,
  }

  with open(f"{OUT_DIR}/json/item_placements.json", "w") as f:
    json.dump(out, f, indent=2)
  print("Wrote json/item_placements.json")

  # --- Hint Data Generation ---
  item_to_loc_index = {}
  for p in output_placements:
    room_str = f"{p['roomNorth']}_{p['roomEast']}"
    for item in p["shuffledItems"]:
      tok = parse_requirement_token(item)
      key_str = f"{tok['type']}:{tok.get('name')}"
      item_to_loc_index.setdefault(key_str, []).append({
        "locationId": p["locationId"],
        "room": room_str
      })

  hint_data = {
    "seed": SEED if not NO_SHUFFLE else "vanilla",
    "itemToLocationIndex": item_to_loc_index,
  }

  with open(f"{OUT_DIR}/json/item_hint_data.json", "w") as f:
    json.dump(hint_data, f, indent=2)
  print("Wrote json/item_hint_data.json")

if __name__ == "__main__":
  init()