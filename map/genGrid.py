import os
import re
import json

IMAGE_FOLDER = "map"
OUTPUT_FILE = "index.html"
EXITS_JSON_PATH = "exits.json"

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
        body {
            margin: 0;
            background-color: #222;
            color: #fff;
            font-family: sans-serif;
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
        .exit-square {
            position: absolute;
            background-color: #00a9;
            box-sizing: border-box;
            border: 1px solid #00ffff55;
        }
    </style>
</head>
<body>
    <div class="grid-container">
"""

html_end = """    </div>
</body>
</html>
"""

def load_exits_map():
    exits_db = {}
    if not os.path.exists(EXITS_JSON_PATH):
        print(f"[-] Warn: {EXITS_JSON_PATH} not found.")
        return exits_db
    try:
        with open(EXITS_JSON_PATH, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            edges = raw_data if isinstance(raw_data, list) else raw_data.get("edges", [])
            for edge in edges:
                if edge.get("origin"):
                    n = int(float(edge["origin"]["north"]))
                    e = int(float(edge["origin"]["east"]))
                    key = f"{n}_{e}"

                    # If this room coordinate hasn't been seen yet, initialize it
                    if key not in exits_db:
                        exits_db[key] = {}

                    # FIX: Merge the side keys instead of overwriting the whole room object
                    edge_exits = edge.get("exits")
                    if edge_exits and isinstance(edge_exits, dict):
                        for side, bounds in edge_exits.items():
                            if bounds: # Only migrate active boundary sets
                                exits_db[key][side] = bounds
    except Exception as err:
        print(f"[-] Failed to read exits database config details: {err}")
    return exits_db

def generate_html():
    if not os.path.exists(IMAGE_FOLDER):
        print(f"Error: '{IMAGE_FOLDER}' folder not found.")
        return

    exits_index = load_exits_map()
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
        tile_exits = exits_index.get(lookup_key, {})

        squares_html = []

        if tile_exits:
            for side, bounds in tile_exits.items():
                if not bounds:
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
                        f'<div class="exit-square" style="left:{x_pos}%; top:{y_pos}%; width:{w_size}%; height:{h_size}%;"></div>'
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
                        f'<div class="exit-square" style="left:{x_pos}%; top:{y_pos}%; width:{w_size}%; height:{h_size}%;"></div>'
                    )

        overlay_content = "\n".join(squares_html)

        tag = f"""        <div class="tile-wrapper" style="grid-column: {grid_col}; grid-row: {grid_row};">
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

    print(f"Success! Generated flipped {OUTPUT_FILE} with {len(html_elements)} overlaid image tiles.")

if __name__ == "__main__":
    generate_html()