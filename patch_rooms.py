# @noregex
"""
Patch MathQuest.js with spatial disambiguation logic for multiple screen exits.
Includes detailed telemetry debug logs and setter recursion-lock fixes.
"""

import json
import os


def init(src):
  OUT_DIR = os.path.dirname(os.path.abspath(__file__))

  connections = json.load(open(f"{OUT_DIR}/json/connections.json"))
  seed = "asd"

  def fmt_num(n):
    if n is None:
      return "-1"
    if n == int(n):
      return str(int(n))
    return f"{n:.4f}"

  rows = []
  print(connections)
  for c in connections:
    print("")
    print("")
    print("")
    print(c)
    rows.append(
      "[%s,%s,%s,%s,%s,%s]"
      % (
        f'"{c["id"]}"',
        fmt_num(c["newX"]),
        fmt_num(c["newY"]),
        fmt_num(c["srcCoord"]),
        f'"{c["direction"]}"',
        fmt_num(c["idx"]),
      )
    )
  table_js = ",".join(rows)

  # Hardcoded layout specs matching your requirements
  PATCH = f"""      // === ENTRANCE RANDOMIZER PATCH START (seed {seed}) ===
    ;(function () {{
      var ROOM_WIDTH = 710.0;
      var ROOM_HEIGHT = 560.0;
      var BLOCKS_X = 14;
      var BLOCKS_Y = 11;
      var BLOCK_W = ROOM_WIDTH / BLOCKS_X;
      var BLOCK_H = ROOM_HEIGHT / BLOCKS_Y;

      var ER_TABLE = [{table_js}]
      var ER_MAP = new Map()
      window.ER_MAP=ER_MAP
      window.ER_TABLE=ER_TABLE
      for (var i = 0; i < ER_TABLE.length; i++) {{
        var r = ER_TABLE[i]
        if (!ER_MAP.has(r[0])) {{
          ER_MAP.set(r[0], [])
        }}
        ER_MAP.get(r[0]).push({{
          newX: r[1],
          newY: r[2],
          srcCoord: r[3],
          direction: r[4],
          idx: r[5]
        }})
      }}

      var erNorth = manager.north === undefined ? null : manager.north
      var erEast = manager.east === undefined ? null : manager.east
      var erInTransition = false
      var erUpdatingInternal = false 
      var erOrigin = {{ north: null, east: null, x: null, y: null }}

      function erBeginWriteIfNeeded() {{
        if (erUpdatingInternal) return; 
        if (!erInTransition) {{
          erOrigin.north = erNorth
          erOrigin.east = erEast
          if (manager.char && manager.char[0]) {{
            erOrigin.x = manager.char[0].get_x()
            erOrigin.y = manager.char[0].get_y()
          }} else {{
            erOrigin.x = null
            erOrigin.y = null
          }}
          erInTransition = true
          console.log("[ER DEBUG] Transition initiated. From room:", erOrigin.north + "," + erOrigin.east, "at position X/Y:", erOrigin.x + "," + erOrigin.y);
        }}
      }}

      Object.defineProperty(manager, "north", {{
        get: function () {{ return erNorth }},
        set: function (v) {{ erBeginWriteIfNeeded(); erNorth = v }},
        enumerable: true,
        configurable: true,
      }})
      Object.defineProperty(manager, "east", {{
        get: function () {{ return erEast }},
        set: function (v) {{ erEast = v }},
        enumerable: true,
        configurable: true,
      }})
      Object.defineProperty(manager, "realnorth", {{
        get: function () {{ return erNorth }},
        set: function (v) {{ erNorth = v }},
        enumerable: true,
        configurable: true,
      }})
      Object.defineProperty(manager, "realeast", {{
        get: function () {{ return erEast }},
        set: function (v) {{ erEast = v }},
        enumerable: true,
        configurable: true,
      }})

      var erOriginalLoca = __createObject.loca
      __createObject.loca = function () {{
        if (erInTransition) {{
          var key = erOrigin.north + "_" + erOrigin.east + "_" + erNorth + "_" + erEast
          if (key=="9_22_10.1_21"){{
            key = "9_22_9_21"
          }}
          if (erOrigin.north ==21 && erOrigin.east==21 && manager.char[0].get_x()==-1){{
            manager.char[0].set_x(50)
          }}
          console.log("[ER DEBUG] Checking redirection for vanilla move path key:", key);

          var conns = ER_MAP.get(key)
          if (conns && conns.length > 0) {{
            var conn = conns[0]

            // Spatial block evaluation handles multiple structural exit conflicts
            if (conns.length > 1 && erOrigin.x !== null && erOrigin.y !== null) {{
              console.log("[ER DEBUG] Multi-gap overlap discovered! Checking tile-block ranges. Choices:", conns.length);
              
              // Determine player block position
              var blockX = Math.floor(erOrigin.x / BLOCK_W);
              var blockY = Math.floor(erOrigin.y / BLOCK_H);
              
              // Clamp values to valid block bounds
              if (blockX < 0) blockX = 0;
              if (blockX >= BLOCKS_X) blockX = BLOCKS_X - 1;
              if (blockY < 0) blockY = 0;
              if (blockY >= BLOCKS_Y) blockY = BLOCKS_Y - 1;

              var roomData = AP_ENTRANCE_IDS[erOrigin.north + "_" + erOrigin.east];
              if (roomData) {{
                // Identify transition direction based on vanilla destination coordinates relative to origin
                var direction = null;
                if (erNorth < erOrigin.north) direction = "north";
                else if (erNorth > erOrigin.north) direction = "south";
                else if (erEast < erOrigin.east) direction = "west";
                else if (erEast > erOrigin.east) direction = "east";

                if (direction && roomData[direction]) {{
                  var spans = roomData[direction];
                  var matchedExitIndex = -1;

                  for (var s = 0; s < spans.length; s++) {{
                    var span = spans[s];
                    if (direction === "west" || direction === "east") {{
                      if (blockY >= span.top && blockY <= span.bottom) {{
                        matchedExitIndex = s;
                        break;
                      }}
                    }} else if (direction === "north" || direction === "south") {{
                      if (blockX >= span.left && blockX <= span.right) {{
                        matchedExitIndex = s;
                        break;
                      }}
                    }}
                  }}

                  // If we found a block-range match, map it safely to our candidate array
                  if (matchedExitIndex !== -1 && matchedExitIndex < conns.length) {{
                    conn = conns[matchedExitIndex];
                    console.log("[ER DEBUG] Block match successful! Target selected via index:", matchedExitIndex);
                  }}
                }}
              }}
            }}

            console.log("[ER DEBUG] Success! Redirecting room target to:", conn.newNorth + "," + conn.newEast, "Placing character at:", conn.newX + "," + conn.newY, conn);

            erUpdatingInternal = true
            try {{
              manager.north = conn.newNorth
              manager.east = conn.newEast
              if (manager.char && manager.char[0]) {{
                if (typeof manager.char[0].set_x === 'function') {{
                  manager.char[0].set_x(conn.newX)
                  manager.char[0].set_y(conn.newY)
                }} else {{
                  manager.char[0].x = conn.newX
                  manager.char[0].y = conn.newY
                }}
              }}
              setTimeout(()=>{{
                test.newScreen()
                if (manager.char && manager.char[0]) {{
                  if (typeof manager.char[0].set_x === 'function') {{
                    manager.char[0].set_x(conn.newX)
                    manager.char[0].set_y(conn.newY)
                  }} else {{
                    manager.char[0].x = conn.newX
                    manager.char[0].y = conn.newY
                  }}
                }}
              }})
            }} finally {{
              erUpdatingInternal = false
            }}
          }} else {{
            console.log("[ER DEBUG] No randomizer override entry for key [" + key + "]. Retaining game defaults.");
          }}
          erInTransition = false
        }}
        return erOriginalLoca.apply(this, arguments)
      }}
    }})()
    // === ENTRANCE RANDOMIZER PATCH END ===
  """

  ANCHOR = "      manager.north = 20\n      manager.east = 20\n"
  assert src.count(ANCHOR) == 1, f"expected exactly one occurrence of anchor, found {src.count(ANCHOR)}"

  patched = src.replace(ANCHOR, PATCH + ANCHOR)
  print(f"Patched file successfully")

  return patched
