# import map.genGrid as _
import os

import gen_exit_data
import gen_map
import progression_to_json # noqa: F401

# import patch_rooms

# playercouldhave, edge_reached, door_reached, warp_reached, all_rooms = shuffle_exits.init()

# gen_exit_data.init()
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(OUT_DIR, "MathQuest/MathQuest.base.js")
OUT_PATH = os.path.join(OUT_DIR, "MathQuest/MathQuest.js")

# with open(SRC_PATH, encoding="utf-8") as f:
#   src = f.read()

# src = patch_rooms.init(src)

# with open(OUT_PATH, "w", encoding="utf-8") as f:
#   f.write(src)

gen_map.main()
