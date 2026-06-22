import os
import re
import json

IMAGE_FOLDER = "map"
GEOMETRY_JSON_PATH = "./json/room_geometry.json"

def find_unmapped_images():
    if not os.path.exists(GEOMETRY_JSON_PATH):
        print(f"[-] Error: '{GEOMETRY_JSON_PATH}' not found.")
        return

    if not os.path.exists(IMAGE_FOLDER):
        print(f"[-] Error: '{IMAGE_FOLDER}' folder not found.")
        return

    # 1. Load your existing structured entries into a fast lookup set
    registered_rooms = set()
    try:
        with open(GEOMETRY_JSON_PATH, "r", encoding="utf-8") as f:
            rooms_list = json.load(f)
            for room in rooms_list:
                if "north" in room and "east" in room:
                    n = int(float(room["north"]))
                    e = int(float(room["east"]))
                    registered_rooms.add((e, n)) # Store as tuple pair (east, north)
    except Exception as err:
        print(f"[-] Failed to read layout json reference data: {err}")
        return

    # 2. Iterate and scan through the map image folder files
    all_files = os.listdir(IMAGE_FOLDER)
    unmapped_tiles = []

    print(f"[*] Scanning {len(all_files)} files inside '{IMAGE_FOLDER}' directory...")

    for filename in all_files:
        # Match files starting with coordinates like 13,6.jpg or 13-6.jpg
        match = re.match(r"^(\d+)[,\-](\d+)", filename)
        if match:
            east = int(match.group(1))
            north = int(match.group(2))

            # If the folder image coordinate pair isn't in our geometry database tracker
            if (east, north) not in registered_rooms:
                unmapped_tiles.append((east, north, filename))

    # 3. Output results clearly
    print("---")
    if not unmapped_tiles:
        print("[+] Awesome! All localized images have an active entry in your geometry JSON file.")
    else:
        # Sort sequentially by East, then North for a clean reading layout
        unmapped_tiles.sort(key=lambda t: (t[0], t[1]))
        print(f"[!] Found {len(unmapped_tiles)} images missing geometry definitions:\n")

        for east, north, filename in unmapped_tiles:
            print(f"  - Coordinate: {east},{north}  (File: {IMAGE_FOLDER}/{filename})")

        print("\n[*] You can click these tiles in your browser view to auto-initialize them via your clipboard watcher daemon.")

if __name__ == "__main__":
    find_unmapped_images()