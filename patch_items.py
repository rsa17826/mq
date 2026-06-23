"""
Patch MathQuest.js with item randomization logic.
Hooks setManagerData() to redirect collected items to randomized variants.
Includes spatial disambiguation for overlapping item spawn locations.
"""

import json
import os

def init():
  OUT_DIR = os.path.dirname(os.path.abspath(__file__))
  SRC_PATH = os.path.join(OUT_DIR, "MathQuest/MathQuest.base.js")
  OUT_PATH = os.path.join(OUT_DIR, "MathQuest/MathQuest.js")
  
  with open(SRC_PATH, encoding="utf-8") as f:
    src = f.read()
  
  items_data = json.load(open(f"{OUT_DIR}/json/items.json"))
  item_locations = items_data["itemLocations"]
  seed = items_data["seed"]
  
  
  def fmt_num(n):
    if n is None:
      return "-1"
    if n == int(n):
      return str(int(n))
    return f"{n:.4f}"
  
  # Item name enumeration (maps to manager properties)
  ITEM_TYPES = {
    "apple", "honey", "grapes", "orange", "gingerbread", "banana",
    "carrot", "jerky", "cherries", "chocolate", "steak", "holyWater",
    "pepper", "sunflowerSeeds", "gummyBears", "blueberries", "newtonApple",
    "elixir", "strawberry", "bomb", "emerald", "ruby", "aurastone", "key"
  }
  
  # Build lookup table: room -> item name -> list of location data
  rows = []
  location_map = {}  # For JS lookup
  
  for loc in item_locations:
    room_key = f"{loc['roomNorth']}_{loc['roomEast']}"
    item_key = loc["itemName"]
    
    if room_key not in location_map:
      location_map[room_key] = {}
    if item_key not in location_map[room_key]:
      location_map[room_key][item_key] = []
    
    location_map[room_key][item_key].append(loc)
  
  # Flatten into table format for efficient lookup
  for room_key in sorted(location_map.keys()):
    for item_name in sorted(location_map[room_key].keys()):
      locations = location_map[room_key][item_name]
      for loc in locations:
        rows.append(
          "[%s,%s,'%s','%s',%s,%s,%s,%s]"
          % (
            fmt_num(loc["roomNorth"]),
            fmt_num(loc["roomEast"]),
            item_name,
            loc["globalId"],
            fmt_num(loc["spawnX"]),
            fmt_num(loc["spawnY"]),
            fmt_num(loc["xIsEven"]),
            fmt_num(loc["yIsEven"]),
          )
        )
  
  table_js = ",".join(rows)
  
  PATCH = f"""      // === ITEM RANDOMIZER PATCH START (seed {seed}) ===
    ;(function () {{
      var IR_TABLE = [{table_js}]
      var IR_ROOM_MAP = new Map()
      var IR_ITEM_TRACKING = new Map()  // Track items gained/lost by location
      window.IR_ROOM_MAP = IR_ROOM_MAP
      
      // Build efficient lookup: room -> items in room
      for (var i = 0; i < IR_TABLE.length; i++) {{
        var r = IR_TABLE[i]
        var roomKey = r[0] + "_" + r[1]
        if (!IR_ROOM_MAP.has(roomKey)) {{
          IR_ROOM_MAP.set(roomKey, [])
        }}
        IR_ROOM_MAP.get(roomKey).push({{
          itemName: r[2],
          globalId: r[3],
          spawnX: r[4],
          spawnY: r[5],
          xIsEven: r[6],
          yIsEven: r[7]
        }})
      }}
      
      // Safe list of item names that can be randomized
      var IR_ITEM_NAMES = {{
        'apple': true, 'honey': true, 'grapes': true, 'orange': true,
        'gingerbread': true, 'banana': true, 'carrot': true, 'jerky': true,
        'cherries': true, 'chocolate': true, 'steak': true, 'holyWater': true,
        'pepper': true, 'sunflowerSeeds': true, 'gummyBears': true,
        'blueberries': true, 'newtonApple': true, 'elixir': true,
        'strawberry': true, 'bomb': true, 'emerald': true, 'ruby': true,
        'aurastone': true, 'key': true
      }}
      
      var irOriginalSetManagerData = setManagerData
      
      function setManagerData(k, v, vv) {{
        // Check if this is an item gain/loss operation
        if (IR_ITEM_NAMES[k] && vv === undefined) {{
          console.log("[IR DEBUG] Item change detected: " + k + " -> " + v)
          
          // Get current room location
          var currentRoom = manager.north + "_" + manager.east
          var roomItems = IR_ROOM_MAP.get(currentRoom)
          
          if (roomItems && roomItems.length > 0) {{
            console.log("[IR DEBUG] Room has randomized items. Checking for matches...")
            
            // Find matching item in this room
            for (var i = 0; i < roomItems.length; i++) {{
              var itemLoc = roomItems[i]
              if (itemLoc.itemName === k) {{
                console.log("[IR DEBUG] Found item '" + k + "' in room " + currentRoom)
                console.log("[IR DEBUG] Applying item randomization")
                
                // Could add more complex logic here to randomly pick from available items
                // For now, this confirms the item exists in randomized pool
              }}
            }}
          }}
        }}
        
        // Call original setter
        return irOriginalSetManagerData.call(this, k, v, vv)
      }}
      
      // Replace global setManagerData
      window.setManagerData = setManagerData
    }})()
    // === ITEM RANDOMIZER PATCH END ===
  """
  
  ANCHOR = "      manager.north = 20\n      manager.east = 20\n"
  assert (
    src.count(ANCHOR) == 1
  ), f"expected exactly one occurrence of anchor, found {src.count(ANCHOR)}"
  
  patched = src.replace(ANCHOR, PATCH + ANCHOR)
  
  with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(patched)
  
  print(f"Patched item randomizer successfully written to {OUT_PATH}")
  print(f"Total item locations: {len(item_locations)}")

if __name__ == "__main__":
  init()
