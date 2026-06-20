"""
Patch MathQuest.js to use the shuffled connections table.

Injects, right before the first real assignment to manager.north/east
(the "new game" initializer), a self-contained block that:

  1. Converts manager.north and manager.east from plain data properties
    into accessor properties (get/set). The setter's only job is to
    remember the room the player was in *before* the current batch of
    writes started (origin-before-transition) -- it does NOT try to
    redirect anything itself, since a single transition can write north
    and/or east one or more times before the room is actually drawn.

  2. Wraps __createObject.loca (confirmed to run exactly once at the end
    of every transition -- edge-walk or door/object teleport alike,
    verified across all 16 trigger mechanisms) to do the actual
    redirect: once both axes have settled to their vanilla-computed
    destination, look up (origin, vanillaDest) in the shuffled
    connections table and, if found, overwrite manager.north/east and
    the player's x/y before the original loca() runs and draws the room.

This means none of the ~15 scattered transition call sites (newScreen's
four edge branches + all door/object triggers) need to be touched
individually -- this single hook point sees every one of them, because
they all funnel through __createObject.loca() before the room is drawn.
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
  # JSON gives us floats like 17.0 -- emit as JS-friendly numbers,
  # preserving real decimals like 10.1/17.1.
  if n == int(n):
    return str(int(n))
  return str(n)


# compact array-of-arrays to keep the inlined table small:
# [originNorth, originEast, vanillaDestNorth, vanillaDestEast, newDestNorth, newDestEast, newX, newY]
rows = []
for c in connections:
  rows.append(
    "[%s,%s,%s,%s,%s,%s,%s,%s]"
    % (
      fmt_num(c["originNorth"]),
      fmt_num(c["originEast"]),
      fmt_num(c["vanillaDestNorth"]),
      fmt_num(c["vanillaDestEast"]),
      fmt_num(c["newDestNorth"]),
      fmt_num(c["newDestEast"]),
      c["newX"],
      c["newY"],
    )
  )
table_js = ",".join(rows)
# @noregex
PATCH = f"""      // === ENTRANCE RANDOMIZER PATCH START (seed {seed}) ===
  ;(function () {{
    var ER_TABLE = [{table_js}]
    var ER_MAP = new Map()
    for (var i = 0; i < ER_TABLE.length; i++) {{
      var r = ER_TABLE[i]
      ER_MAP.set(r[0] + "_" + r[1] + "_" + r[2] + "_" + r[3], {{
        newNorth: r[4],
        newEast: r[5],
        newX: r[6],
        newY: r[7],
      }})
    }}

    var erNorth = manager.north === undefined ? null : manager.north
    var erEast = manager.east === undefined ? null : manager.east
    var erInTransition = false
    var erOrigin = {{ north: null, east: null }}

    function erBeginWriteIfNeeded() {{
      if (!erInTransition) {{
        erOrigin.north = erNorth
        erOrigin.east = erEast
        erInTransition = true
      }}
    }}

    Object.defineProperty(manager, "north", {{
      get: function () {{
        return erNorth
      }},
      set: function (v) {{
        erBeginWriteIfNeeded()
        erNorth = v
      }},
      enumerable: true,
      configurable: true,
    }})
    Object.defineProperty(manager, "east", {{
      get: function () {{
        return erEast
      }},
      set: function (v) {{
        erBeginWriteIfNeeded()
        erEast = v
      }},
      enumerable: true,
      configurable: true,
    }})

    var erOriginalLoca = __createObject.loca
    __createObject.loca = function () {{
      if (erInTransition) {{
        var key =
          erOrigin.north + "_" + erOrigin.east + "_" + erNorth + "_" + erEast
        var conn = ER_MAP.get(key)
        if (conn) {{
          manager.north = conn.newNorth
          manager.east = conn.newEast
          if (manager.char && manager.char[0]) {{
            manager.char[0].set_x(conn.newX)
            manager.char[0].set_y(conn.newY)
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

print(f"Patched file written to {OUT_PATH}")
print(f"Original size: {len(src)} chars, patched size: {len(patched)} chars")
print(f"Connections table: {len(connections)} entries inlined")
