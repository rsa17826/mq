import re
from _progression import PROG

# Regex to match quest items with levels, e.g. "quest:curse.2" or "quest:gTree.15"
QUEST_PATTERN = re.compile(r"^quest:([^.]+)\.(\d+)$")


def find_missing_quest_prerequisites(prog_list):
  results = []

  for idx, node in enumerate(prog_list):
    receives = node.get("receive", [])
    requires_branches = node.get("requires", [])

    # Flatten all required items across all OR branches for easy checking
    all_required_items = {item for branch in requires_branches for item in branch}

    for item in receives:
      match = QUEST_PATTERN.match(item)
      if not match:
        continue

      quest_name = match.group(1)
      level = int(match.group(2))

      # Only check for previous level if level > 1
      if level > 1:
        required_prev_quest = f"quest:{quest_name}.{level - 1}"

        # If the previous quest level is missing from requirements
        if required_prev_quest not in all_required_items:
          results.append(
            {
              "index": idx,
              "room": node.get("room"),
              "received": item,
              "missing_requirement": required_prev_quest,
              "requires": requires_branches,
            }
          )




  return results


if __name__ == "__main__":
  missing = find_missing_quest_prerequisites(PROG)

  print(f"Found {len(missing)} node(s) where 'requires' is missing the previous quest level:\n")

  for entry in missing:
    print(f"Index: {entry['index']}")
    print(f"Room: {entry['room']}")
    print(f"Received Quest: {entry['received']}")
    print(f"Missing Prerequisite: {entry['missing_requirement']}")
    print(f"Current Requires: {entry['requires']}")
    print("-" * 50)

