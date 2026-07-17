"""
Regenerates prog.js from _progression.py's PROG list.
"""

import ast
import json
import sys


def convert(src_path: str, out_path: str) -> None:
  src = open(src_path).read()
  tree = ast.parse(src)
  prog = None
  for node in ast.walk(tree):
    if isinstance(node, ast.AnnAssign) and getattr(node.target, "id", None) == "PROG":
      prog = ast.literal_eval(node.value)
      break


  if prog is None:
    raise ValueError("Could not find a PROG: list[...] = [...] assignment in the source file")

  out = []
  for entry in prog:
    room = entry["room"]
    out.append(
      {
        "room": f"{room['north']}_{room['east']}",
        "requires": entry.get("requires", []),
        "receive": entry.get("receive", []),
      }
    )

  with open(out_path, "w") as f:
    f.write("const PROG_DATA = ")
    json.dump(out, f)
    f.write(";\n")

  print(f"Wrote {len(out)} entries to {out_path}")


if __name__ == "__main__":
  # if len(sys.argv) != 3:
  #     print(__doc__)
  #     sys.exit(1)
  convert("./_progression.py", "prog.js")
