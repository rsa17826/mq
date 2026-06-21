import os
import re
import json

IMAGE_FOLDER = "mapSmall"
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
    <script src="./live.js#html"></script>
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
            width: 124px;
            height: 98px;
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
        }
        /* Style for incomplete base rooms */
        .exit-square {
            position: absolute;
            background-color: #a009;
            box-sizing: border-box;
            border: 1px solid #ff000055;
            pointer-events: auto; /* Enable clicking */
            cursor: pointer;
            z-index: 10;
        }
        /* Style for baseline complete rooms */
        .exit-square.room-complete {
            background-color: #00a9;
            border: 1px solid #00ffff55;
        }
        /* Highlight when clicked/selected in the active group buffer */
        .exit-square.selected {
            background-color: rgba(255, 215, 0, 0.75) !important;
            border: 2px solid #ffd700 !important;
            z-index: 20;
        }
        /* New style applied to squares that have successfully been mapped into an area */
        .exit-square.completed {
            background-color: rgba(0, 200, 0, 0.6) !important;
            border: 2px solid #00ff00 !important;
            z-index: 15;
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

        // Left Click Handler on wrapper backgrounds to Copy Position
        document.querySelectorAll('.tile-wrapper').forEach(tile => {
            tile.addEventListener('click', function(e) {
                if (e.target.classList.contains('exit-square')) return;
                const posStr = this.getAttribute('data-pos');
                navigator.clipboard.writeText(posStr).then(() => {
                    showToast("Copied: " + posStr);
                }).catch(err => {
                    console.error("[-] Clipboard write exception error:", err);
                });
            });
        });

        // Interactive Area Linking Configuration
        let selectedExits = [];
        let currentTileKey = null;

        // Register exit square selection listeners
        document.querySelectorAll('.exit-square').forEach(square => {
            square.addEventListener('click', function(e) {
                e.stopPropagation(); // Avoid triggering base tile wrapper click

                const parentTile = this.closest('.tile-wrapper');
                const posStr = parentTile.getAttribute('data-pos');

                // If switching rooms, clear out previous buffer tracking automatically
                if (currentTileKey !== posStr) {
                    document.querySelectorAll('.exit-square.selected').forEach(el => el.classList.remove('selected'));
                    selectedExits = [];
                    currentTileKey = posStr;
                }

                if (this.classList.contains('selected')) {
                    this.classList.remove('selected');
                    selectedExits = selectedExits.filter(item => item !== this);
                } else {
                    this.classList.add('selected');
                    selectedExits.push(this);
                }
                console.log(`[+] Exit added to selection group buffer. Total items: ${selectedExits.length}`);
            });
        });

        // Right Click Handler on Tile wrappers to build area lists
        document.querySelectorAll('.tile-wrapper').forEach(tile => {
            tile.addEventListener('contextmenu', function(event) {
                event.preventDefault();

                const posStr = this.getAttribute('data-pos');

                // Fetch full internal data geometry payload from injected script metadata index
                const rawRoomData = GEOM_METADATA_INDEX[posStr];
                if (!rawRoomData) {
                    console.error("[-] Geometry metadata missing for room index:", posStr);
                    return;
                }

                // If context menu is clicked with items selected, save them as a connected group area
                if (selectedExits.length > 0 && currentTileKey === posStr) {
                    if (!rawRoomData.areas) {
                        rawRoomData.areas = [];
                    }

                    const subAreaGroup = selectedExits.map(el => {
                        return {
                            side: el.getAttribute('data-side'),
                            idx: parseInt(el.getAttribute('data-idx'), 10)
                        };
                    });

                    rawRoomData.areas.push(subAreaGroup);

                    console.log(`%c[🎉] Connected Area Linked successfully for room ${posStr}!`, "color: #00ffcc; font-weight: bold;");
                    const stringifiedOut = JSON.stringify(rawRoomData, null, 2);
                    console.log(stringifiedOut);

                    navigator.clipboard.writeText(stringifiedOut).then(() => {
                        showToast(`Saved Area Group for Room ${posStr}!`);
                    });

                    // Transition selected gold squares to the completed green class state
                    selectedExits.forEach(el => {
                        el.classList.remove('selected');
                        el.classList.add('completed');
                    });

                    // Reset the buffer to start mapping the next independent zone inside this room
                    selectedExits = [];
                } else {
                    // Right-clicked with empty selection buffer: reset tracking completely
                    document.querySelectorAll('.exit-square.selected').forEach(el => el.classList.remove('selected'));
                    selectedExits = [];
                    currentTileKey = posStr;
                    console.log(`[x] Reset linked selection tracking buffer context for tile room ${posStr}.`);
                }
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
                    geom_db[key] = room
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
            north = int(match.group(1))
            east = int(match.group(2))
            parsed_tiles.append((north, east, filename))
            if north > max_row:
                max_row = north

    html_elements = []
    js_metadata_lookup = {}

    for north, east, filename in parsed_tiles:
        grid_col = east + 1
        grid_row = (max_row - north) + 1
        img_path = f"{IMAGE_FOLDER}/{filename}"

        lookup_key = f"{north}_{east}"
        room_data = geom_index.get(lookup_key, {"north": north, "east": east, "exits": {}, "complete": False})
        tile_exits = room_data.get("exits", {})
        is_complete = room_data.get("complete", False)

        # Retain original schema contents
        js_metadata_lookup[f"{north},{east}"] = room_data

        # Initial class states based on room level completion status
        class_modifier = " room-complete" if is_complete else ""
        squares_html = []

        if tile_exits and isinstance(tile_exits, dict):
            for side, bounds_list in tile_exits.items():
                if not bounds_list:
                    continue

                if not isinstance(bounds_list, list):
                    bounds_list = [bounds_list]

                for idx, bounds in enumerate(bounds_list):
                    if not bounds or not isinstance(bounds, dict):
                        continue

                    # Check if this exit was already stored in an area segment to persist green state on build reload
                    completed_modifier = ""
                    if "areas" in room_data:
                        for area in room_data["areas"]:
                            if any(item.get("side") == side and item.get("idx") == idx for item in area):
                                completed_modifier = " completed"
                                break

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
                            f'<div class="exit-square{class_modifier}{completed_modifier}" data-side="{side}" data-idx="{idx}" style="left:{x_pos}%; top:{y_pos}%; width:{w_size}%; height:{h_size}%;"></div>'
                        )

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
                            f'<div class="exit-square{class_modifier}{completed_modifier}" data-side="{side}" data-idx="{idx}" style="left:{x_pos}%; top:{y_pos}%; width:{w_size}%; height:{h_size}%;"></div>'
                        )

        overlay_content = "\n".join(squares_html)

        tag = f"""        <div class="tile-wrapper" style="grid-column: {grid_col}; grid-row: {grid_row};" title="Position: {north},{east}" data-pos="{north},{east}">
            <img src="{img_path}" class="grid-item" alt="Tile {north},{east}">
            <div class="overlay-layer">
{overlay_content}
            </div>
        </div>"""
        html_elements.append(tag)

    # Serialize complete database layout context inline into HTML head scope structures
    injected_js_db = f"<script>const GEOM_METADATA_INDEX = {json.dumps(js_metadata_lookup, indent=2)};</script>"
    final_html_start = html_start.replace('<div class="grid-container">', injected_js_db + '\n    <div class="grid-container">')

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_html_start)
        f.write("\n".join(html_elements))
        f.write("\n" + html_end)

    print(f"Success! Generated flipped {OUTPUT_FILE} with {len(html_elements)} interactive grouping map tiles.")

if __name__ == "__main__":
    generate_html()