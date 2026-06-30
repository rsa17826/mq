#!/usr/bin/env python3
import json
import os


def generate_js_client():
  # 1. Resolve paths
  CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
  output_path = os.path.join(CURRENT_DIR, "archipelago_manifest.js")

  # 2. Import the progression list directly from your game module
  try:
    from _progression import PROG
  except ImportError:
    print(
      "Error: Could not find _progression.py. Ensure this script is run from its directory."
    )
    return

  # 3. Mirror the ID counters exactly as they are configured in your AP world
  LOCATION_NAME_TO_ID = {}
  ITEM_NAME_TO_ID = {}

  loc_id_counter = 1
  item_id_counter = 1

  # --- Items: mirrors items.py exactly ---
  for thing in PROG:
    if "receive" in thing:
      for itemInfo in thing["receive"]:
        itemName = itemInfo.removesuffix("#1")
        if itemName not in ITEM_NAME_TO_ID:
          if itemInfo.startswith(
            (
              "magic:",
              "weapon:",
              # "flag:final boss dead",
              "permit:",
              "misc:fire crystal",
              "item:aurastones",
              # "entrance.",
              # "quest:",
              # "area:",
            )
          ):
            ITEM_NAME_TO_ID[itemName] = item_id_counter
          elif itemInfo.startswith(("skill:", "armor:", "item:ring")):
            ITEM_NAME_TO_ID[itemName] = item_id_counter
          elif itemInfo.startswith(
            (
              "item:key",
              "item:",
              "food:",
              "misc:",
            )
          ):
            ITEM_NAME_TO_ID[itemName] = item_id_counter
          elif itemInfo.startswith(("quest:", "area:")):
            continue
          else:
            print(itemName, "not used")
            continue
          item_id_counter += 1

  # --- Locations: mirrors locations.py exactly ---
  for thing in PROG:
    if "receive" in thing:
      for itemInfo in thing["receive"]:
        if itemInfo.startswith(
          (
            "item:",
            "weapon:",
            "armor:",
            "food:",
            "skill:",
            "magic:",
            "permit:",
            "misc:",
          )
        ):
          locName = f"{itemInfo.split('#')[0]}"
          if locName not in LOCATION_NAME_TO_ID:
            LOCATION_NAME_TO_ID[locName] = loc_id_counter
            loc_id_counter += 1

  # Invert the items dictionary so JavaScript can look up strings using integer IDs
  ITEM_ID_TO_NAME = {v: k for k, v in ITEM_NAME_TO_ID.items()}
  # TODO
  ITEM_ID_TO_NAME[99999] = "item:trap"
  # 4. Generate the final JavaScript code block
  js_content = f"""/**
* AUTO-GENERATED ARCHIPELAGO MANIFESTS
* Do not modify this file directly. Regenerate via your build script.
*/

const AP_LOCATION_IDS = {json.dumps(LOCATION_NAME_TO_ID, indent=2)};

const AP_ITEM_IDS = {json.dumps(ITEM_ID_TO_NAME, indent=2)};

console.log(`[Archipelago] Database ready: ${{Object.keys(AP_LOCATION_IDS).length}} locations, ${{Object.keys(AP_ITEM_IDS).length}} items.`);
"""

  # 5. Write out file
  with open(output_path, "w", encoding="utf-8") as f:
    f.write(js_content)

  print(f"Success! Generated Client database at: {output_path}")
  print(f"Registered {loc_id_counter} locations and {item_id_counter} items.")


if __name__ == "__main__":
  generate_js_client()
