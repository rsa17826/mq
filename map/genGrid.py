import os
import re
import json

IMAGE_FOLDER = "map"
OUTPUT_FILE = "index.html"
GEOMETRY_JSON_PATH = "./room_geometry.json"

# Constants to map the 14x11 grid layout inside the 624x493 tile box
TILE_WIDTH = 624
TILE_HEIGHT = 493
BLOCKS_X = 14
BLOCKS_Y = 11

BLOCK_WIDTH_PCT = 100 / BLOCKS_X
BLOCK_HEIGHT_PCT = 100 / BLOCKS_Y

html_start = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dynamic Image Grid Map with Overlays</title>
    <script src="./live.js"></script>
    <style>
        /* Hide scrollbars globally across the entire page while maintaining scroll functionality */
        html, body {
            margin: 0;
            background-color: #222;
            color: #fff;
            font-family: sans-serif;

            /* Firefox */
            scrollbar-width: none;

            /* IE and Legacy Edge */
            -ms-overflow-style: none;
        }

        /* Chrome, Safari, and Opera/Modern Edge */
        html::-webkit-scrollbar,
        body::-webkit-scrollbar {
            display: none;
        }

        .grid-container {
            display: grid;
            grid-auto-columns: max-content;
            grid-auto-rows: max-content;
            gap: 0px;
            padding: 20px;
            transform-origin: top left;
            scale: 0.5;
        }
        .tile-wrapper {
            position: relative;
            width: 624px;
            height: 493px;
            cursor: pointer;
        }
        .grid-item {
            display: block;
            width: 100%;
            height: 100%;
        }
        .overlay-layer {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
        }
        /* Style for complete rooms */
        .exit-square {
            position: absolute;
            background-color: #00a9;
            box-sizing: border-box;
            border: 1px solid #00ffff55;
        }
        /* New style for incomplete rooms */
        .exit-square.incomplete {
            background-color: #a009;
            border: 1px solid #ff000055;
        }

        /* Floating notification indicator style */
        .toast-notify {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #333;
            color: #00ffcc;
            padding: 10px 16px;
            border-radius: 4px;
            font-weight: bold;
            border: 1px solid #00ffcc;
            z-index: 10000;
            opacity: 0;
            transition: opacity 0.2s ease-in-out;
            pointer-events: none;
        }
    </style>
</head>
<body>
    <div id="toast" class="toast-notify">Copied!</div>
    <div class="grid-container">
"""

html_end = """    </div>
    <script>
        function showToast(text) {
            const el = document.getElementById("toast");
            el.innerText = text;
            el.style.opacity = "1";
            setTimeout(() => { el.style.opacity = "0"; }, 1500);
        }

        // Setup global event listener delegation for tracking map grid interaction
        document.querySelectorAll('.tile-wrapper').forEach(tile => {
            tile.addEventListener('click', function() {
                const posStr = this.getAttribute('data-pos');
                navigator.clipboard.writeText(posStr).then(() => {
                    showToast("Copied: " + posStr);
                }).catch(err => {
                    console.error("[-] Clipboard write exception error:", err);
                });
            });
        });
    </script>
</body>
</html>
"""

def load_geometry_map():
    geom_db = {}
    if not os.path.exists(GEOMETRY_JSON_PATH):
        print(f"[-] Warn: {GEOMETRY_JSON_PATH} not found.")
        return geom_db
    try:
        with open(GEOMETRY_JSON_PATH, "r", encoding="utf-8") as f:
            rooms_list = json.load(f)
            for room in rooms_list:
                if "north" in room and "east" in room:
                    n = int(float(room["north"]))
                    e = int(float(room["east"]))
                    key = f"{n}_{e}"
                    geom_db[key] = {
                        "exits": room.get("exits", {}),
                        "complete": room.get("complete", False)
                    }
    except Exception as err:
        print(f"[-] Failed to read room geometry config details: {err}")
    return geom_db

def generate_html():
    if not os.path.exists(IMAGE_FOLDER):
        print(f"Error: '{IMAGE_FOLDER}' folder not found.")
        return

    geom_index = load_geometry_map()
    files = os.listdir(IMAGE_FOLDER)
    parsed_tiles = []
    max_row = 0

    for filename in files:
        match = re.match(r"^(\d+)[,\-](\d+)", filename)
        if match:
            east = int(match.group(1))
            north = int(match.group(2))
            parsed_tiles.append((east, north, filename))
            if north > max_row:
                max_row = north

    html_elements = []

    for east, north, filename in parsed_tiles:
        grid_col = east + 1
        grid_row = (max_row - north) + 1
        img_path = f"{IMAGE_FOLDER}/{filename}"

        lookup_key = f"{north}_{east}"
        room_data = geom_index.get(lookup_key, {"exits": {}, "complete": False})
        tile_exits = room_data["exits"]
        is_complete = room_data["complete"]

        class_modifier = "" if is_complete else " incomplete"
        squares_html = []

        if tile_exits and isinstance(tile_exits, dict):
            for side, bounds_list in tile_exits.items():
                if not bounds_list:
                    continue

                # Standardize so we always iterate a list structure
                if not isinstance(bounds_list, list):
                    bounds_list = [bounds_list]

                for bounds in bounds_list:
                    if not bounds or not isinstance(bounds, dict):
                        continue

                    # West & East bounds (Vertical placements)
                    if side in ["west", "east"]:
                        if bounds.get("top") is None or bounds.get("bottom") is None:
                            continue

                        start_val = int(float(bounds["top"]))
                        end_val = int(float(bounds["bottom"]))

                        x_pos = 0 if side == "west" else 100 - BLOCK_WIDTH_PCT
                        y_pos = start_val * BLOCK_HEIGHT_PCT

                        w_size = BLOCK_WIDTH_PCT
                        h_size = ((end_val - start_val) + 1) * BLOCK_HEIGHT_PCT

                        squares_html.append(
                            f'<div class="exit-square{class_modifier}" style="left:{x_pos}%; top:{y_pos}%; width:{w_size}%; height:{h_size}%;"></div>'
                        )

                    # North & South bounds (Horizontal placements)
                    elif side in ["north", "south"]:
                        if bounds.get("left") is None or bounds.get("right") is None:
                            continue

                        start_val = int(float(bounds["left"]))
                        end_val = int(float(bounds["right"]))

                        x_pos = start_val * BLOCK_WIDTH_PCT
                        y_pos = 0 if side == "north" else 100 - BLOCK_HEIGHT_PCT

                        w_size = ((end_val - start_val) + 1) * BLOCK_WIDTH_PCT
                        h_size = BLOCK_HEIGHT_PCT

                        squares_html.append(
                            f'<div class="exit-square{class_modifier}" style="left:{x_pos}%; top:{y_pos}%; width:{w_size}%; height:{h_size}%;"></div>'
                        )

        overlay_content = "\n".join(squares_html)

        tag = f"""        <div class="tile-wrapper" style="grid-column: {grid_col}; grid-row: {grid_row};" title="Position: {east},{north}" data-pos="{east},{north}">
            <img src="{img_path}" class="grid-item" alt="Tile {east},{north}">
            <div class="overlay-layer">
{overlay_content}
            </div>
        </div>"""
        html_elements.append(tag)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_start)
        f.write("\n".join(html_elements))
        f.write("\n" + html_end)

    print(f"Success! Generated flipped {OUTPUT_FILE} with {len(html_elements)} overlaid image tiles using updated array geometry data.")

if __name__ == "__main__":
    generate_html()