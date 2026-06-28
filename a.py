import re
import sys


def find_duplicates(file_path):
  try:
    with open(file_path, "r", encoding="utf-8") as f:
      content = f.read()
  except FileNotFoundError:
    print(f"Error: {file_path} not found.")
    return

  # Regex block to cleanly match each object block inside the list literal
  # It catches "room": { "north": X, "east": Y } and the "receive": [...] array
  pattern = r'\{\s*"room"\s*:\s*\{\s*"north"\s*:\s*([0-9.\-]+)\s*,\s*"east"\s*:\s*([0-9.\-]+)\s*\}[^}]+?"receive"\s*:\s*(\[[^\]]*?\])'
  matches = re.findall(pattern, content, re.DOTALL)

  seen = {} # Maps (north, east) -> set of individual items already seen
  duplicates = [] # Keeps track of unique (north, east, item_str) duplicates to print

  for north_str, east_str, receive_raw in matches:
    # Canonicalize numbers
    north = int(north_str) if "." not in north_str else float(north_str)
    east = int(east_str) if "." not in east_str else float(east_str)

    # Parse individual items from the current receive list
    items = re.findall(r'"([^"]+)"', receive_raw)

    coord = (north, east)
    if coord not in seen:
      seen[coord] = set()

    for item in items:
      if item.split('#')[0] in seen[coord]:
        item_str = item.split('#')[0]
        # Ensure we only record this specific duplicate item once per room coordinate
        if (north, east, item_str) not in duplicates:
          duplicates.append((north, east, item_str))
      else:
        seen[coord].add(item)

  # Output matching template format: \n{0}\{"north": %s, "east": %s\},[^\}]+?%s
  format_template = r"\n{{0}}\{{\"north\": {0}, \"east\": {1}\}},[^\}}]+?{2}"

  for north, east, item_str in duplicates:
    print(format_template.format(north, east, item_str).replace('\\"', '"'))


if __name__ == "__main__":
  find_duplicates("_progression.py")
