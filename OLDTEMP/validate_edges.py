import os
import re
import json

IMAGE_FOLDER = "map"
EXITS_JSON_PATH = "./json/exits.json"


def validate_map_edges():
  if not os.path.exists(EXITS_JSON_PATH):
    print(f"[-] Error: '{EXITS_JSON_PATH}' not found.")
    return

  if not os.path.exists(IMAGE_FOLDER):
    print(f"[-] Error: '{IMAGE_FOLDER}' folder not found.")
    return

  # 1. Scan the map folder and build a quick-lookup set of existing images
  # Format stored: (east, north)
  existing_images = set()
  all_files = os.listdir(IMAGE_FOLDER)

  for filename in all_files:
    match = re.match(r"^(\d+)[,\-](\d+)\.jpg$", filename.lower())
    if match:
      east = int(match.group(1))
      north = int(match.group(2))
      existing_images.add((east, north))

  print(f"[*] Indexed {len(existing_images)} tile images from '{IMAGE_FOLDER}/'.")

  # 2. Parse json/exits.json and cross-reference the edges
  try:
    with open(EXITS_JSON_PATH, "r", encoding="utf-8") as f:
      data = json.load(f)
      # Handle if top-level is an object with 'edges' or a direct list
      edges = data if isinstance(data, list) else data.get("edges", [])
  except Exception as err:
    print(f"[-] Failed to read or parse exits JSON data: {err}")
    return

  print(f"[*] Checking {len(edges)} edge definitions...")
  print("---")

  invalid_count = 0

  for index, edge in enumerate(edges, start=1):
    edge_id = edge.get("id", f"Index {index}")
    direction = edge.get("direction", "unknown")

    origin = edge.get("origin")
    dest = edge.get("dest")

    # Skip check if structural layout elements are entirely missing
    if not origin or not dest:
      print(f"[!] Flagged: Edge '{edge_id}' is missing origin or dest coordinate objects.")
      invalid_count += 1
      continue

    try:
      orig_e = int(float(origin.get("east")))
      orig_n = int(float(origin.get("north")))
      dest_e = int(float(dest.get("east")))
      dest_n = int(float(dest.get("north")))
    except (ValueError, TypeError):
      print(f"[!] Flagged: Edge '{edge_id}' contains malformed coordinate numbers.")
      invalid_count += 1
      continue

    # Check if images exist for both endpoints
    origin_has_image = (orig_n, orig_e) in existing_images
    dest_has_image = (dest_n, dest_e) in existing_images

    # Flag if either (or both) are missing an image tile
    if not origin_has_image or not dest_has_image:
      invalid_count += 1
      print(f"[!] Invalid Edge Detected: '{edge_id}' ({direction})")

      if not origin_has_image:
        print(f"    -> Origin Room Missing Image: {orig_n},{orig_e}.jpg")
      if not dest_has_image:
        print(f"    -> Destination Room Missing Image: {dest_n},{dest_e}.jpg")
      print()

  print("---")
  if invalid_count == 0:
    print("[+] Success! All edge origins and destinations have valid matching images.")
  else:
    print(f"[!] Validation complete. Flagged {invalid_count} invalid edge records.")


if __name__ == "__main__":
  validate_map_edges()
