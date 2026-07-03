# @noregex
"""
Patch MathQuest.js with spatial disambiguation logic for multiple screen exits.
Includes detailed telemetry debug logs and setter recursion-lock fixes.
"""

import json
import os


def init(src):
  OUT_DIR = os.path.dirname(os.path.abspath(__file__))

  connections = json.load(open(f"{OUT_DIR}/json/connections.json"))["connections"]
  seed = "asd"

  PATCH = f"""      // === ENTRANCE RANDOMIZER PATCH START (seed {seed}) ===
    ;(function () {{
      var erNorth = manager.north === undefined ? null : manager.north
      var erEast = manager.east === undefined ? null : manager.east
      var erInTransition = false
      var erUpdatingInternal = false
      var erOrigin = {{ north: null, east: null, x: null, y: null }}

      function erBeginWriteIfNeeded() {{
        if (erUpdatingInternal) return
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
        set: function (v) {{ erBeginWriteIfNeeded(); erEast = v }},
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
          var key = erOrigin.north + "_" + erOrigin.east
          var direction = null
          const n = erNorth-erOrigin.north
          const e = erEast-erOrigin.east
          log(n, e)
          if (e===0&&n==1){{
            direction="north"
          }} else if (e===0&&n==-1){{
            direction="south"
          }} else if (n===0&&e==1){{
            direction="east"
          }} else if (n===0&&e==-1){{
            direction="west"
          }}
          if (key=="9_22_10.1_21"){{
            key = "9_22_9_21"
          }}
          if (erOrigin.north ==21 && erOrigin.east==21 && manager.char[0].get_x()==-1){{
            manager.char[0].set_x(50)
          }}
          console.log("[ER DEBUG] Checking redirection for vanilla move path key:", key, erOrigin.north + "_" + erOrigin.east + "_" + erNorth + "_" + erEast, direction)
          var conns = (ER_MAP.get(key) || []).filter(e=>e.origSide==direction)

          if (conns?.length > 0) {{
            log(erOrigin, "erOrigin")
            // var warptype = "unknown"
              
                // console.log(manager.char[0].get_y(), manager.char[0].get_x(), manager.north, manager.east)
              // if (manager.char[0].get_y() > 550 ||
              // manager.char[0].get_y() < 0 ||
              // manager.char[0].get_x() < 0 ||
              // manager.char[0].get_x() > 660) {{
                // warptype = "edge"
              // }}
              // else if (manager.charBottom[0].hitTestObject(
                // manager.stairsDown,
              // ) &&
              // manager.stairsDown.get_visible() == 1) {{
            // warptype = "stairsDown"
              // }}
              // else if (manager.charBottom[0].hitTestObject(
                // manager.stairsUp2,
              // ) &&
              // manager.stairsUp2.get_visible() == 1) {{
            // warptype = "stairsUp2"
              // }}
              // else if (manager.charBottom[0].hitTestObject(
                // manager.stairsUp,
              // ) &&
              // manager.stairsUp.get_visible() == 1) {{
            // warptype = "stairsUp"
              // }}
              // else if (manager.charBottom[0].hitTestObject(
                // manager.grimsbane,
              // ) &&
              // manager.grimsbane.get_visible() == 1) {{
            // warptype = "grimsbane"
              // }}
              // else if (manager.charBottom[0].hitTestObject(
                // manager.castleDoors,
              // ) &&
              // manager.castleDoors.get_visible() == 1) {{
            // warptype = "castleDoors"
              // }}
              // else if (manager.charBottom[0].hitTestObject(manager.isle1) &&
                // manager.isle1.get_visible() == 1) {{
              // warptype = "isle1"
              // }}
              // else if (manager.charBottom[0].hitTestObject(manager.isle2) &&
                // manager.isle2.get_visible() == 1) {{
              // warptype = "isle2"
              // }}
              // else if (manager.charBottom[0].hitTestObject(manager.isle3) &&
                // manager.isle3.get_visible() == 1) {{
              // warptype = "isle3"
              // }}
              // else if (manager.charBottom[0].hitTestObject(manager.temple) &&
                // manager.temple.get_visible() == 1) {{
              // warptype = "temple"
              // }}
              console.log("[ER DEBUG] candidate conns for", direction, conns)
            function colliding(c){{
              return true
            }}
            var conn = conns.find(colliding) || conns[0]

            if (direction && erOrigin.x !== null && erOrigin.y !== null) {{
              // 2. Calculate coordinates relative to tile layout block grids
              var blockX = Math.floor(erOrigin.x / BLOCK_W)
              var blockY = Math.floor(erOrigin.y / BLOCK_H)
              if (blockX < 0) blockX = 0; if (blockX >= BLOCKS_X) blockX = BLOCKS_X - 1
              if (blockY < 0) blockY = 0; if (blockY >= BLOCKS_Y) blockY = BLOCKS_Y - 1

              // 3. Extract correct visual layout bounds via AP_ENTRANCE_IDS configuration matching
              var roomData = AP_ENTRANCE_IDS.find(function(r) {{
                return r.north === erOrigin.north && r.east === erOrigin.east
              }})

              if (roomData && roomData.exits && roomData.exits[direction]) {{
                var spans = roomData.exits[direction]
                var matchedExitIndex = -1

                // 4. Bounds assessment check matching player position coordinates to active exit span
                for (var s = 0; s < spans.length; s++) {{
                  var span = spans[s]
                  if (direction === "west" || direction === "east") {{
                    if (blockY >= span.top && blockY <= span.bottom) {{
                      matchedExitIndex = s
                      break
                    }}
                  }} else if (direction === "north" || direction === "south") {{
                    if (blockX >= span.left && blockX <= span.right) {{
                      matchedExitIndex = s
                      break
                    }}
                  }}
                }}

                // 5. Query matching logic data tracking table entry using direction and index configurations
                if (matchedExitIndex !== -1) {{
                  var specificTarget = conns.find(function(c) {{
                    return c.origSide === direction && String(c.origIdx) === String(matchedExitIndex)
                  }})

                  if (specificTarget) {{
                    conn = specificTarget
                  }}
                }}
              }}
            }}

            // 6. newX/newY describe where to land when ENTERING a room, so pull them from
            // the destination room's entrance span (keyed by exitSide/exitIdx), not the
            // source room's exit span.
            if (conn) {{
              var destRoomData = AP_ENTRANCE_IDS.find(function(r) {{
                return r.north === conn.newNorth && r.east === conn.newEast
              }})
              var destSpan = null
              if (destRoomData && destRoomData.exits && destRoomData.exits[conn.exitSide]) {{
                destSpan = destRoomData.exits[conn.exitSide][Number(conn.exitIdx)]
              }}
              if (destSpan) {{
                var midBlock = (destSpan.left + destSpan.right) / 2
                var midBlockY = (destSpan.top + destSpan.bottom) / 2
                if (conn.exitSide=="north"){{
                  conn.newX = midBlock * BLOCK_W
                  conn.newY = 0
                }}
                if (conn.exitSide=="south"){{
                  conn.newX = midBlock * BLOCK_W
                  conn.newY = 10 * BLOCK_H
                }}
                if (conn.exitSide=="west"){{
                  conn.newX = 0
                  conn.newY = midBlockY * BLOCK_H
                }}
                if (conn.exitSide=="east"){{
                  conn.newX = 13 * BLOCK_W
                  conn.newY = midBlockY * BLOCK_H
                }}
                if (destSpan.newX!==undefined){{
                  conn.newX = destSpan.newX
                }}
                if (destSpan.newY!==undefined){{
                  conn.newY = destSpan.newY
                }}
              }} else {{
                console.log("[ER DEBUG] No destination entrance span found for", conn.newNorth, conn.newEast, conn.exitSide, conn.exitIdx)
              }}
            }}

            console.log("[ER DEBUG] Redirecting to:", conn.newNorth + "," + conn.newEast, "Placing at:", conn.newX + "," + conn.newY, 'from', conn, 'to', destRoomData, destSpan)

            erUpdatingInternal = true
            try {{
              manager.north = conn.newNorth
              manager.east = conn.newEast

              var setCoords = function() {{
                if (manager.char && manager.char[0]) {{
                  if (typeof manager.char[0].set_x === 'function') {{
                    manager.char[0].set_x(conn.newX)
                    manager.char[0].set_y(conn.newY)
                  }} else {{
                    manager.char[0].x = conn.newX
                    manager.char[0].y = conn.newY
                  }}
                }}
              }}

              setCoords()
              setTimeout(function() {{
                if (window.test && typeof window.test.newScreen === 'function') {{
                  test.newScreen()
                }}
                setCoords()
              }})
            }} finally {{
              erUpdatingInternal = false
              debugger
            }}
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
