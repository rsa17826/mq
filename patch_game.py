"""
Patch MathQuest.js with spatial disambiguation logic for multiple screen exits.
"""

import json
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(OUT_DIR, "MathQuest/MathQuest.base.js")
OUT_PATH = os.path.join(OUT_DIR, "MathQuest/MathQuest.js")

with open(SRC_PATH, encoding="utf-8") as f:
  src = f.read()

conn_data = json.load(open(f"{OUT_DIR}/connections.json"))
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
      "[%s,%s,%s,%s,%s,%s,%s,%s,%s,%s]"
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
      )
  )
# @noregex
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
        dirCode: r[9]
      }})
    }}

    var erNorth = manager.north === undefined ? null : manager.north
    var erEast = manager.east === undefined ? null : manager.east
    var erInTransition = false
    var erOrigin = {{ north: null, east: null, x: null, y: null }}

    function erBeginWriteIfNeeded() {{
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

    var erOriginalLoca = __createObject.loca
    __createObject.loca = function () {{
      if (erInTransition) {{
        var key = erOrigin.north + "_" + erOrigin.east + "_" + erNorth + "_" + erEast
        var conns = ER_MAP.get(key)
        if (conns && conns.length > 0) {{
          var conn = conns[0]
          // If multiple warps share a room boundary edge, find the closest match based on player exit location
          if (conns.length > 1 && erOrigin.x !== null && erOrigin.y !== null) {{
            var minDiff = Infinity
            for (var j = 0; j < conns.length; j++) {{
              var c = conns[j]
              if (c.dirCode > 0 && c.srcCoord !== -1) {{
                var pCoord = (c.dirCode === 1 || c.dirCode === 2) ? erOrigin.x : erOrigin.y
                var diff = Math.abs(pCoord - c.srcCoord)
                if (diff < minDiff) {{
                  minDiff = diff
                  conn = c
                }}
              }}
            }}
          }}
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

with open(OUT_PATH, "w", encoding="utf-8") as f:
  f.write(patched)

print(f"Patched file successfully written to {OUT_PATH}")