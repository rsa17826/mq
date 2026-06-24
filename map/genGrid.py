# @noregex
import os
import re
import json

IMAGE_FOLDER = "mapSmall"
OUTPUT_FILE = "index.html"
GEOMETRY_JSON_PATH = "./json/room_geometry.json"

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
            margin-right: 460px; /* Leave clean workspace margin for the code side panel */
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
        /* Style for complete rooms */
        .exit-square {
            position: absolute;
            background-color: #00a9;
            box-sizing: border-box;
            border: 1px solid #00ffff55;
            pointer-events: auto; /* Enable clicking */
            cursor: pointer;
            z-index: 10;
        }
        /* Highlight when clicked/selected */
        .exit-square.selected {
            background-color: rgba(255, 215, 0, 0.75) !important;
            border: 2px solid #ffd700 !important;
            z-index: 20;
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
            left: 20px; /* Moved left to prevent overlaying the generator panel */
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

        /* Test Boilerplate Generator UI Side Panel */
        .test-generator-panel {
            position: fixed;
            top: 20px;
            right: 20px;
            width: 420px;
            height: calc(100vh - 40px);
            background-color: #1a1a1a;
            border: 2px solid #00ffcc;
            border-radius: 6px;
            padding: 15px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            z-index: 10000;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }
        .test-generator-panel h3 {
            margin-top: 0;
            color: #00ffcc;
            font-size: 16px;
            border-bottom: 1px solid #333;
            padding-bottom: 8px;
            margin-bottom: 10px;
        }
        .test-generator-panel textarea {
            flex-grow: 1;
            background-color: #101010;
            color: #00ff66;
            border: 1px solid #444;
            border-radius: 4px;
            padding: 10px;
            resize: none;
            font-family: 'Courier New', Courier, monospace;
            font-size: 11px;
            line-height: 1.4;
        }
        .test-generator-panel .btn-group {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
        .test-generator-panel button {
            background-color: #00ffcc;
            color: #111;
            border: none;
            padding: 10px;
            font-weight: bold;
            cursor: pointer;
            border-radius: 4px;
            flex: 1;
            font-size: 13px;
            transition: background 0.1s;
        }
        .test-generator-panel button:hover {
            background-color: #00ccaa;
        }
        .test-generator-panel button.clear-btn {
            background-color: #ff4444;
            color: #fff;
        }
        .test-generator-panel button.clear-btn:hover {
            background-color: #cc2222;
        }
    </style>
</head>
<body>
    <div id="toast" class="toast-notify">Copied!</div>
    <div class="grid-container">
"""

html_end = """    </div>

    <div class="test-generator-panel">
        <h3>Test Automation Generator</h3>
        <textarea id="test-code-output" readonly></textarea>
        <div class="btn-group">
            <button onclick="copyTestCode()">Copy Python Code</button>
            <button class="clear-btn" onclick="clearTestCode()">Clear Lines</button>
        </div>
    </div>

    <script>
        function showToast(text) {
            const el = document.getElementById("toast");
            el.innerText = text;
            el.style.opacity = "1";
            setTimeout(() => { el.style.opacity = "0"; }, 1500);
        }

        // State tracker for generated assertions
        let assertionLines = [];

        function updateCodeBox() {
            const textarea = document.getElementById("test-code-output");
            let boilerplate = "from .bases import MathQuestTestBase\\n\\n";
            boilerplate += "class TestEasyModeLogic(MathQuestTestBase):\\n";
            boilerplate += "    options = {\\n        \\\"hard_mode\\\": False,\\n    }\\n\\n";
            boilerplate += "    def test_easy_mode_access(self) -> None:\\n";
            boilerplate += "        with self.subTest(\\\"Verified Room Grid Access Requirements\\\"):\\n";
            
            if (assertionLines.length === 0) {
                boilerplate += "            # [!] Left-Click tiles/exits for assertTrue\\n";
                boilerplate += "            # [!] Right-Click tiles/exits for assertFalse\\n";
                boilerplate += "            pass\\n";
            } else {
                assertionLines.forEach(item => {
                    boilerplate += `            # Verify reachability rules for ${item.region}\\n`;
                    boilerplate += `            self.assert${item.isTrue ? 'True' : 'False'}(self.world.get_region("${item.region}").can_reach(self.multiworld.state))\\n\\n`;
                });
            }
            textarea.value = boilerplate;
            textarea.scrollTop = textarea.scrollHeight; // Auto scroll to newest additions
        }

        function addAssertion(regionName, isTrue) {
            assertionLines.push({ region: regionName, isTrue: isTrue });
            updateCodeBox();
        }

        function clearTestCode() {
            assertionLines = [];
            updateCodeBox();
            showToast("Cleared generated code buffer.");
        }

        function copyTestCode() {
            const textarea = document.getElementById("test-code-output");
            navigator.clipboard.writeText(textarea.value).then(() => {
                showToast("Copied Test Script to Clipboard!");
            }).catch(err => {
                console.error("[-] Failed copying code: ", err);
            });
        }

        // Room Background Clicks (Base Regions)
        document.querySelectorAll('.tile-wrapper').forEach(tile => {
            // Left Click -> Assert Accessible (True)
            tile.addEventListener('click', function(e) {
                if (e.target.classList.contains('exit-square')) return;
                const posStr = this.getAttribute('data-pos');
                const [north, east] = posStr.split(',');
                const regionId = `${north}_${east}`;
                
                addAssertion(regionId, true);
                showToast(`[+] Added True check for Room: ${regionId}`);
            });

            // Right Click -> Assert Unreachable (False)
            tile.addEventListener('contextmenu', function(e) {
                if (e.target.classList.contains('exit-square')) return;
                e.preventDefault();
                const posStr = this.getAttribute('data-pos');
                const [north, east] = posStr.split(',');
                const regionId = `${north}_${east}`;
                
                addAssertion(regionId, false);
                showToast(`[-] Added False check for Room: ${regionId}`);
            });
        });

        // Exit Squares Click Overrides (Sub-Regions)
        document.querySelectorAll('.exit-square').forEach(square => {
            // Left Click Sub-Region -> Assert Accessible (True)
            square.addEventListener('click', function(e) {
                e.stopPropagation(); // Block cascading down to base tile
                const parentTile = this.closest('.tile-wrapper');
                const [north, east] = parentTile.getAttribute('data-pos').split(',');
                const side = this.getAttribute('data-side');
                const idx = this.getAttribute('data-idx');
                const subRegionId = `${north}_${east}#${side}.${idx}`;
                
                addAssertion(subRegionId, true);
                showToast(`[+] Added True check for Slot: ${subRegionId}`);
            });

            // Right Click Sub-Region -> Assert Unreachable (False)
            square.addEventListener('contextmenu', function(e) {
                e.stopPropagation();
                e.preventDefault();
                const parentTile = this.closest('.tile-wrapper');
                const [north, east] = parentTile.getAttribute('data-pos').split(',');
                const side = this.getAttribute('data-side');
                const idx = this.getAttribute('data-idx');
                const subRegionId = `${north}_${east}#${side}.${idx}`;
                
                addAssertion(subRegionId, false);
                showToast(`[-] Added False check for Slot: ${subRegionId}`);
            });
        });

        // Initialize empty view template on layout boot
        updateCodeBox();
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

        # Retain original schema object contents so they can be extended cleanly via JavaScript tools
        js_metadata_lookup[f"{north},{east}"] = room_data

        class_modifier = "" if is_complete else " incomplete"
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
                            f'<div class="exit-square{class_modifier}" data-side="{side}" data-idx="{idx}" style="left:{x_pos}%; top:{y_pos}%; width:{w_size}%; height:{h_size}%;"></div>'
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
                            f'<div class="exit-square{class_modifier}" data-side="{side}" data-idx="{idx}" style="left:{x_pos}%; top:{y_pos}%; width:{w_size}%; height:{h_size}%;"></div>'
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

generate_html()