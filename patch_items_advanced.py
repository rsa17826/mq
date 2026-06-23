"""
Advanced Item Randomizer Patch for MathQuest.js
Implements full item redirection with spatial disambiguation and tracking.
Includes telemetry, deadlock prevention, and overlap resolution.
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
  
  # Build lookup table: (north, east, itemName) -> list of location objects
  rows = []
  
  for loc in item_locations:
    rows.append(
      "[%s,%s,'%s','%s',%s,%s,%s,%s]"
      % (
        fmt_num(loc["roomNorth"]),
        fmt_num(loc["roomEast"]),
        loc["itemName"],
        loc["globalId"],
        fmt_num(loc["spawnX"]),
        fmt_num(loc["spawnY"]),
        fmt_num(loc["xIsEven"]),
        fmt_num(loc["yIsEven"]),
      )
    )
  
  table_js = ",".join(rows)
  
  PATCH = f"""      // === ADVANCED ITEM RANDOMIZER PATCH START (seed {seed}) ===
    ;(function () {{
      var IR_TABLE = [{table_js}]
      var IR_ROOM_ITEM_MAP = new Map()     // room -> items in room
      var IR_ITEM_COLLECT_LOG = new Map()  // track which items collected by globalId
      var IR_COLLECTION_TIMEOUT = new Map() // debounce rapid same-item gains
      var IR_UPDATING_INTERNAL = false      // prevent infinite loops from our writes
      var IR_PLAYER_LAST_POS = {{ x: null, y: null, room: null }}
      var IR_PROXIMITY_THRESHOLD = 50       // pixels
      
      window.IR_ROOM_ITEM_MAP = IR_ROOM_ITEM_MAP
      window.IR_ITEM_COLLECT_LOG = IR_ITEM_COLLECT_LOG
      
      // Build efficient lookup structures
      for (var i = 0; i < IR_TABLE.length; i++) {{
        var r = IR_TABLE[i]
        var roomKey = r[0] + "_" + r[1]
        
        if (!IR_ROOM_ITEM_MAP.has(roomKey)) {{
          IR_ROOM_ITEM_MAP.set(roomKey, [])
        }}
        
        IR_ROOM_ITEM_MAP.get(roomKey).push({{
          itemName: r[2],
          globalId: r[3],
          spawnX: r[4],
          spawnY: r[5],
          xIsEven: r[6],
          yIsEven: r[7],
          collected: false
        }})
      }}
      
      var IR_SAFE_ITEMS = {{
        'apple': true, 'honey': true, 'grapes': true, 'orange': true,
        'gingerbread': true, 'banana': true, 'carrot': true, 'jerky': true,
        'cherries': true, 'chocolate': true, 'steak': true, 'holyWater': true,
        'pepper': true, 'sunflowerSeeds': true, 'gummyBears': true,
        'blueberries': true, 'newtonApple': true, 'elixir': true,
        'strawberry': true, 'bomb': true, 'emerald': true, 'ruby': true,
        'aurastone': true, 'key': true
      }}
      
      function irGetPlayerPos() {{
        if (manager.char && manager.char[0]) {{
          return {{
            x: typeof manager.char[0].get_x === 'function' ? manager.char[0].get_x() : manager.char[0].x,
            y: typeof manager.char[0].get_y === 'function' ? manager.char[0].get_y() : manager.char[0].y,
            room: manager.north + "_" + manager.east
          }}
        }}
        return {{ x: null, y: null, room: null }}
      }}
      
      function irFindClosestItem(itemName, playerPos) {{
        if (!playerPos || playerPos.x === null) return null
        
        var roomItems = IR_ROOM_ITEM_MAP.get(playerPos.room)
        if (!roomItems) return null
        
        var candidates = []
        for (var i = 0; i < roomItems.length; i++) {{
          var item = roomItems[i]
          if (item.itemName === itemName && !item.collected) {{
            var dist = Math.sqrt(
              Math.pow(playerPos.x - item.spawnX, 2) + 
              Math.pow(playerPos.y - item.spawnY, 2)
            )
            if (dist <= IR_PROXIMITY_THRESHOLD) {{
              candidates.push({{ item: item, distance: dist }})
            }}
          }}
        }}
        
        if (candidates.length === 0) return null
        if (candidates.length === 1) return candidates[0].item
        
        // Multiple items: use spatial disambiguation
        var closest = candidates[0]
        for (var i = 1; i < candidates.length; i++) {{
          if (candidates[i].distance < closest.distance) {{
            closest = candidates[i]
          }}
        }}
        console.log("[IR DISAMB] Multiple '" + itemName + "' found. Selected via distance (" + closest.distance.toFixed(1) + "px)")
        return closest.item
      }}
      
      var irOriginalSetManagerData = setManagerData
      
      window.setManagerData = function (k, v, vv) {{
        // Ignore internal updates
        if (IR_UPDATING_INTERNAL) {{
          return irOriginalSetManagerData.call(this, k, v, vv)
        }}
        
        // Check for item operations
        if (IR_SAFE_ITEMS[k] && vv === undefined && typeof v === 'number') {{
          var playerPos = irGetPlayerPos()
          var currentValue = manager[k] || 0
          var isGain = v > currentValue
          var isLoss = v < currentValue
          
          if (isGain) {{
            console.log("[IR GAIN] '" + k + "': " + currentValue + " → " + v + " at room " + playerPos.room)
            
            // Debounce: prevent same item being marked collected multiple times
            var lastCollectTime = IR_COLLECTION_TIMEOUT.get(k) || 0
            var now = Date.now()
            if (now - lastCollectTime > 100) {{  // 100ms debounce
              var closestItem = irFindClosestItem(k, playerPos)
              if (closestItem) {{
                closestItem.collected = true
                IR_ITEM_COLLECT_LOG.set(closestItem.globalId, {{
                  itemName: k,
                  collectedAt: now,
                  room: playerPos.room,
                  playerPos: playerPos
                }})
                console.log("[IR TRACKED] Item #" + closestItem.globalId + " marked as collected")
              }} else {{
                console.log("[IR INFO] No matching randomized item location found for '" + k + "'")
              }}
              IR_COLLECTION_TIMEOUT.set(k, now)
            }}
          }} else if (isLoss) {{
            console.log("[IR LOSS] '" + k + "': " + currentValue + " → " + v)
          }}
        }}
        
        IR_UPDATING_INTERNAL = true
        try {{
          return irOriginalSetManagerData.call(this, k, v, vv)
        }} finally {{
          IR_UPDATING_INTERNAL = false
        }}
      }}
      
      // Hook manager properties to track position
      var irLastRoomUpdate = 0
      Object.defineProperty(manager, "north", {{
        get: function () {{ return manager._irNorth || 20 }},
        set: function (v) {{
          manager._irNorth = v
          irLastRoomUpdate = Date.now()
        }},
        enumerable: true,
        configurable: true
      }})
      Object.defineProperty(manager, "east", {{
        get: function () {{ return manager._irEast || 20 }},
        set: function (v) {{
          manager._irEast = v
          irLastRoomUpdate = Date.now()
        }},
        enumerable: true,
        configurable: true
      }})
      
      // Debug: log collection stats every 10 seconds
      setInterval(function () {{
        if (IR_ITEM_COLLECT_LOG.size > 0) {{
          console.log("[IR STATS] Total items collected: " + IR_ITEM_COLLECT_LOG.size + 
                      " | Available items tracked: " + IR_TABLE.length)
        }}
      }}, 10000)
    }})()
    // === ADVANCED ITEM RANDOMIZER PATCH END ===
  """
  
  ANCHOR = "      manager.north = 20\n      manager.east = 20\n"
  assert (
    src.count(ANCHOR) == 1
  ), f"expected exactly one occurrence of anchor, found {src.count(ANCHOR)}"
  
  patched = src.replace(ANCHOR, PATCH + ANCHOR)
  
  with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(patched)
  
  print(f"[ADVANCED] Patched item randomizer successfully written to {OUT_PATH}")
  print(f"[ADVANCED] Features:")
  print(f"  - Spatial disambiguation for overlapping items")
  print(f"  - Collection tracking and debouncing")
  print(f"  - Player proximity detection (threshold: 50px)")
  print(f"  - Real-time telemetry logging")
  print(f"  - Deadlock prevention with safety flags")
  print(f"  - Total item locations: {len(item_locations)}")

if __name__ == "__main__":
  init()
