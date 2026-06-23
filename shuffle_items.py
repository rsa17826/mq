"""
Generate shuffled item locations for MathQuest with spatial distribution.
Maps item types to room locations with optional parity matching (even/odd room coords).
"""

import json
import random
import sys
import os

def init():
  OUT_DIR = os.path.dirname(os.path.abspath(__file__))

  # Parse seed from command line
  NO_SHUFFLE = "--no-shuffle" in sys.argv
  clean_args = [arg for arg in sys.argv if arg != "--no-shuffle"]
  SEED = int(clean_args[1]) if len(clean_args) > 1 else 12345

  random.seed(SEED)

  # Define available item types and their "slots" (how many exist in the game)
  # Format: "itemName": count_in_game
  ITEM_DEFINITIONS = {
    "apple": 15,
    "honey": 8,
    "grapes": 12,
    "orange": 10,
    "gingerbread": 6,
    "banana": 9,
    "carrot": 11,
    "jerky": 7,
    "cherries": 10,
    "chocolate": 8,
    "steak": 5,
    "holyWater": 4,
    "pepper": 6,
    "sunflowerSeeds": 5,
    "gummyBears": 6,
    "blueberries": 7,
    "newtonApple": 3,
    "elixir": 2,
    "strawberry": 4,
    "bomb": 20,
    "emerald": 15,
    "ruby": 12,
    "aurastone": 14,
    "key": 8,
  }

  # Define room grid - all accessible rooms in the game
  # Format: (north, east) tuples
  ROOMS = [
    (20, 20),   # Starting area
    (19, 20), (21, 20), (20, 19), (20, 21),
    (18, 20), (22, 20), (20, 18), (20, 22),
    (19, 19), (19, 21), (21, 19), (21, 21),
    (17, 20), (23, 20), (20, 17), (20, 23),
    (18, 19), (18, 21), (22, 19), (22, 21),
    (19, 18), (19, 22), (21, 18), (21, 22),
    (16, 20), (24, 20), (20, 16), (20, 24),
    # Extended areas
    (17, 19), (17, 21), (23, 19), (23, 21),
    (18, 18), (18, 22), (22, 18), (22, 22),
  ]

  # Screen position coordinates where items can spawn
  # Rooms are 710x560 pixels with a 14x11 grid of blocks
  BLOCK_W = 710 / 14
  BLOCK_H = 560 / 11

  # Valid spawn positions (block indices within a room)
  VALID_SPAWN_POSITIONS = [
    (i * BLOCK_W + BLOCK_W/2, j * BLOCK_H + BLOCK_H/2)
    for i in range(14)
    for j in range(11)
    if not (i in [0, 13] or j in [0, 10]) # Exclude edges where player spawns
  ]

  # Build pool of all item instances
  item_pool = []
  for item_name, count in ITEM_DEFINITIONS.items():
    for idx in range(count):
      item_pool.append({
        "name": item_name,
        "instanceId": idx,
        "globalId": len(item_pool)
      })

  # If NO_SHUFFLE, keep vanilla distribution; otherwise randomize
  if NO_SHUFFLE:
    random.seed(12345) # Use default seed for consistent vanilla mapping

  # Create location assignments: map item instances to room locations
  item_locations = []

  for room_idx, room in enumerate(ROOMS):
    # Determine how many items should spawn in this room
    # Distribute more items in central/accessible rooms
    dist_from_center = abs(room[0] - 20) + abs(room[1] - 20)
    if dist_from_center <= 2:
      items_in_room = random.randint(3, 6)
    elif dist_from_center <= 5:
      items_in_room = random.randint(2, 4)
    else:
      items_in_room = random.randint(1, 3)

    # Select random items for this room
    items_here = random.sample(
      range(min(len(item_pool), room_idx * 10 + items_in_room)),
      min(items_in_room, len(item_pool) - room_idx * 5)
    )

    for item_global_id in items_here:
      if item_global_id < len(item_pool):
        item = item_pool[item_global_id]
        spawn_pos = random.choice(VALID_SPAWN_POSITIONS)

        item_locations.append({
          "globalId": item["globalId"],
          "itemName": item["name"],
          "instanceId": item["instanceId"],
          "roomNorth": room[0],
          "roomEast": room[1],
          "spawnX": spawn_pos[0],
          "spawnY": spawn_pos[1],
          # Metadata for disambiguation
          "xIsEven": 1 if int(spawn_pos[0]) % 2 == 0 else 0,
          "yIsEven": 1 if int(spawn_pos[1]) % 2 == 0 else 0,
        })

  # Create output JSON
  output = {
    "seed": SEED,
    "totalItems": len(item_pool),
    "totalLocations": len(item_locations),
    "itemLocations": item_locations
  }

  # Ensure output directory exists
  json_dir = os.path.join(OUT_DIR, "json")
  os.makedirs(json_dir, exist_ok=True)

  # Write output
  output_path = os.path.join(json_dir, "items.json")
  with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

  print(f"Generated item shuffle with seed {SEED}")
  print(f"Total items: {len(item_pool)}")
  print(f"Total locations: {len(item_locations)}")
  print(f"Items written to {output_path}")

if __name__ == "__main__":
  init()
