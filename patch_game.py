import patch_items_advanced
import patch_rooms
import os

def init():
  OUT_DIR = os.path.dirname(os.path.abspath(__file__))
  SRC_PATH = os.path.join(OUT_DIR, "MathQuest/MathQuest.base.js")
  OUT_PATH = os.path.join(OUT_DIR, "MathQuest/MathQuest.js")

  with open(SRC_PATH, encoding="utf-8") as f:
    src = f.read()

  patched = patch_items_advanced.init(src)
  patched = patch_rooms.init(patched)

  with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(patched)