from collections import defaultdict
import re
from _progression import PROG

# Pattern to extract quest name and level, e.g. "quest:curse.2" or "quest:gTree.15"
QUEST_PATTERN = re.compile(r"^quest:([^.]+)\.(\d+)$")


def check_quest_sparsity(prog_list):
  # Dictionary mapping quest_name -> set of levels found
  quests = defaultdict(set)

  # Collect all quest levels defined across all receive entries
  for node in prog_list:
    for item in node.get("receive", []):
      match = QUEST_PATTERN.match(item)
      if match:
        quest_name = match.group(1)
        level = int(match.group(2))
        quests[quest_name].add(level)



  sparse_quests = {}
  valid_quests = {}

  for quest_name, levels in quests.items():
    max_level = max(levels)
    expected_levels = set(range(1, max_level + 1))
    missing_levels = sorted(list(expected_levels - levels))

    if missing_levels:
      sparse_quests[quest_name] = {
        "max_level": max_level,
        "found_levels": sorted(list(levels)),
        "missing_levels": missing_levels,
      }
    else:
      valid_quests[quest_name] = {
        "max_level": max_level,
        "total_levels": len(levels),
      }


  return sparse_quests, valid_quests


if __name__ == "__main__":
  sparse, valid = check_quest_sparsity(PROG)

  print("=== SPARSE QUEST REPORT ===")
  if not sparse:
    print("All quests are continuous with no gaps (1 to MAX)!\n")
  else:
    print(f"Found {len(sparse)} quest series with gaps/missing levels:\n")
    for quest_name, info in sparse.items():
      print(f"Quest Name    : {quest_name}")
      print(f"Max Level     : {info['max_level']}")
      print(f"Found Levels  : {info['found_levels']}")
      print(f"Missing Levels: {info['missing_levels']}")
      print("-" * 50)


  print("\n=== COMPLETE / GAPLESS QUESTS ===")
  for quest_name, info in sorted(valid.items()):
    print(f"• {quest_name}: levels 1 -> {info['max_level']}")

