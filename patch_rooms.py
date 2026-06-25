# @noregex
"""
Patch MathQuest.js with spatial disambiguation logic for multiple screen exits.
Includes detailed telemetry debug logs and setter recursion-lock fixes.
"""

import json
import os

def init(src):
  OUT_DIR = os.path.dirname(os.path.abspath(__file__))
  
  conn_data = json.load(open(f"{OUT_DIR}/json/connections.json"))
  connections = conn_data["connections"]
  seed = conn_data["seed"]
  
  
  def fmt_num(n):
    if n is None:
      return "-1"
    if n == int(n):
      return str(int(n))
    return f"{n:.4f}"
  
  
  DIR_CODES = {"north": 1, "south": 2, "west": 3, "east": 4}
  
  rows = []
  for c in connections:
    d_code = DIR_CODES.get(c.get("direction"), 0)
    rows.append(
      "[%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s]"
      % (
        fmt_num(c["originNorth"]),
        fmt_num(c["originEast"]),
        fmt_num(c["vanillaDestNorth"]),
        fmt_num(c["vanillaDestEast"]),
        fmt_num(c["newDestNorth"]),
        fmt_num(c["newDestEast"]),
        fmt_num(c["newX"]),
        fmt_num(c["newY"]),
        fmt_num(c.get("srcCoord")),
        str(d_code),
        fmt_num(c.get("xIsEven")),
        fmt_num(c.get("yIsEven")),
      )
    )
    #  "originNorth": origin["north"],
    #   "originEast": origin["east"],
    #   "vanillaDestNorth": vdest[0],
    #   "vanillaDestEast": vdest[1],
    #   "newDestNorth": to_exit["origin"]["north"],
    #   "newDestEast": to_exit["origin"]["east"],
    #   "newX": to_exit.get("dest_x", 330),
    #   "newY": to_exit.get("dest_y", 255),
    #   "xIsEven": to_exit.get("xIsEven",0),
    #   "yIsEven": to_exit.get("yIsEven",0),
    #   "srcCoord": from_exit.get("src_coord"),
    #   "direction": from_exit.get("direction"),
    #   "mechanism": from_exit["mechanism"],
    #   "requires": requires_raw,
    #   "fromExitId": from_exit["id"],
    #   "toExitId": to_exit["id"],
  table_js = ",".join(rows)
  
  PATCH = f"""      // === ENTRANCE RANDOMIZER PATCH START (seed {seed}) ===
    ;(function () {{
      var ER_TABLE = [{table_js}]
      var ER_MAP = new Map()
      window.ER_MAP=ER_MAP
      for (var i = 0; i < ER_TABLE.length; i++) {{
        var r = ER_TABLE[i]
        var key = r[0] + "_" + r[1] + "_" + r[2] + "_" + r[3]
        if (!ER_MAP.has(key)) {{
          ER_MAP.set(key, [])
        }}
        ER_MAP.get(key).push({{
          newNorth: r[4],
          newEast: r[5],
          newX: r[6],
          newY: r[7],
          srcCoord: r[8],
          dirCode: r[9],
          xIsEven: r[10],
          yIsEven: r[11]
        }})
      }}
  
      var erNorth = manager.north === undefined ? null : manager.north
      var erEast = manager.east === undefined ? null : manager.east
      var erInTransition = false
      var erUpdatingInternal = false // Safety flag to prevent infinite loops from our own writes
      var erOrigin = {{ north: null, east: null, x: null, y: null }}
  
      function erBeginWriteIfNeeded() {{
        if (erUpdatingInternal) return; // Ignore updates performed inside loca()
        if (!erInTransition) {{
          erOrigin.north = erNorth
          erOrigin.east = erEast
          if (manager.char && manager.char[0]) {{
            erOrigin.x = typeof manager.char[0].get_x === 'function' ? manager.char[0].get_x() : manager.char[0].x
            erOrigin.y = typeof manager.char[0].get_y === 'function' ? manager.char[0].get_y() : manager.char[0].y
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
          var key = erOrigin.north + "_" + erOrigin.east + "_" + erNorth + "_" + erEast
          if (erOrigin.north ==21&& erOrigin.east==21&&manager.char[0].get_x()==-1){{
            manager.char[0].set_x(50)
          }}
          console.log("[ER DEBUG] Checking redirection for vanilla move path key:", key);
          
          var conns = ER_MAP.get(key)
          if (conns && conns.length > 0) {{
            var conn = conns[0]
            
            if (conns.length > 1 && erOrigin.x !== null && erOrigin.y !== null) {{
              console.log("[ER DEBUG] Multi-gap overlap discovered! Choices count:", conns.length);
              var warptype = "unknown"
              
                console.log(manager.char[0].get_y(), manager.char[0].get_x(), manager.north, manager.east)
              if (manager.char[0].get_y() > 550 ||
              manager.char[0].get_y() < 0 ||
              manager.char[0].get_x() < 0 ||
              manager.char[0].get_x() > 660) {{
                warptype = "edge"
              }}
              else if (manager.charBottom[0].hitTestObject(
                manager.stairsDown,
              ) &&
              manager.stairsDown.get_visible() == 1) {{
            warptype = "stairsDown"
              }}
              else if (manager.charBottom[0].hitTestObject(
                manager.stairsUp2,
              ) &&
              manager.stairsUp2.get_visible() == 1) {{
            warptype = "stairsUp2"
              }}
              else if (manager.charBottom[0].hitTestObject(
                manager.stairsUp,
              ) &&
              manager.stairsUp.get_visible() == 1) {{
            warptype = "stairsUp"
              }}
              else if (manager.charBottom[0].hitTestObject(
                manager.grimsbane,
              ) &&
              manager.grimsbane.get_visible() == 1) {{
            warptype = "grimsbane"
              }}
              else if (manager.charBottom[0].hitTestObject(
                manager.castleDoors,
              ) &&
              manager.castleDoors.get_visible() == 1) {{
            warptype = "castleDoors"
              }}
              else if (manager.charBottom[0].hitTestObject(manager.isle1) &&
                manager.isle1.get_visible() == 1) {{
              warptype = "isle1"
              }}
              else if (manager.charBottom[0].hitTestObject(manager.isle2) &&
                manager.isle2.get_visible() == 1) {{
              warptype = "isle2"
              }}
              else if (manager.charBottom[0].hitTestObject(manager.isle3) &&
                manager.isle3.get_visible() == 1) {{
              warptype = "isle3"
              }}
              else if (manager.charBottom[0].hitTestObject(manager.temple) &&
                manager.temple.get_visible() == 1) {{
              warptype = "temple"
              }}
              console.log("warptype", warptype, conns)
              var minDiff = Infinity
              for (var j = 0; j < conns.length; j++) {{
                var c = conns[j]
                if (c.dirCode > 0 && c.srcCoord !== -1) {{
                  var pCoord = (c.dirCode === 1 || c.dirCode === 2) ? erOrigin.x : erOrigin.y
                  var diff = Math.abs(pCoord - c.srcCoord)
                  console.log(" -> Match Check candidate [" + j + "]: dir=" + c.dirCode + " expectedCoord=" + c.srcCoord + " distance=" + diff);
                  if (diff < minDiff) {{
                    minDiff = diff
                    conn = c
                  }}
                }}
              }}
            }}
            // TODO
            if (key=="9_22_10.1_21"){{
              conn = {{...conn, newNorth:9,newEast:21,newX:384,newY:69}}
            }}
            console.log("[ER DEBUG] Success! Redirecting room target to:", conn.newNorth + "," + conn.newEast, "Placing character at:", conn.newX + "," + conn.newY, conn.xIsEven, conn.yIsEven, conn);
            
            // Set safety lock flag to prevent our proxy properties from creating bad transition tracking chains
            erUpdatingInternal = true
            try {{
              manager.north = conn.newNorth
              manager.east = conn.newEast
              if (manager.char && manager.char[0]) {{
                if (typeof manager.char[0].set_x === 'function') {{
                  manager.char[0].set_x(conn.newX)
                  // left or right trnasitions move player down .5*blockY to get centered dont know why only l/r needs this
                  if (conn.dirCode>=3)
                  manager.char[0].set_y(conn.newY+25.3571)
                  else
                  manager.char[0].set_y(conn.newY)
                }} else {{
                  manager.char[0].x = conn.newX
                  manager.char[0].y = conn.newY
                }}
              }}
              setTimeout(()=>{{
                // prevents duplicate stairs appearing from the orig room in the new random room
                test.newScreen()
                // prevents warp rings from moving player to wrong position
                if (manager.char && manager.char[0]) {{
                  if (typeof manager.char[0].set_x === 'function') {{
                    manager.char[0].set_x(conn.newX)
                    if (conn.dirCode>=3)
                  manager.char[0].set_y(conn.newY+25.3571)
                  else
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
  assert (
    src.count(ANCHOR) == 1
  ), f"expected exactly one occurrence of anchor, found {src.count(ANCHOR)}"
  
  patched = src.replace(ANCHOR, PATCH + ANCHOR)
  
  print(f"Patched file successfully")
  
  return patched