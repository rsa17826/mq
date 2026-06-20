import os
import re
import json

# Target folder pointing to the downsized versions
IMAGE_FOLDER = "mapSmall"
OUTPUT_FILE = "randomized_index.html"
GEOMETRY_JSON_PATH = "./room_geometry.json"
CONNECTIONS_JSON_PATH = "./connections.json"

# Constants scaled down to 10% to match the downsized image sizes perfectly
TILE_WIDTH = 62.4
TILE_HEIGHT = 49.3
BLOCKS_X = 14
BLOCKS_Y = 11

BLOCK_WIDTH_PCT = 100 / BLOCKS_X
BLOCK_HEIGHT_PCT = 100 / BLOCKS_Y
GAP_SIZE = 15 # Sizing gap between tiles

html_start = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>High-Performance Interactive Map Viewer</title>
    <style>
        html, body {
            margin: 0;
            background-color: #111;
            color: #fff;
            font-family: sans-serif;
            scrollbar-width: none;
            -ms-overflow-style: none;
        }
        html::-webkit-scrollbar, body::-webkit-scrollbar {
            display: none;
        }
        /* FIXED: Explicitly defined rows/cols prevent empty spaces from collapsing to 0px */
        .grid-container {
            display: grid;
            grid-template-columns: repeat(var(--cols), 62.4px);
            grid-template-rows: repeat(var(--rows), 49.3px);
            gap: 15px;
            padding: 20px;
            position: relative;
        }
        .tile-wrapper {
            position: relative;
            width: 100%;
            height: 100%;
            background-color: #222;
            border: 1px solid #444;
            box-sizing: border-box;
            z-index: 5;
            transition: border-color 0.1s ease-in-out;
        }
        .tile-wrapper:hover {
            border-color: #fff;
            z-index: 15;
        }
        .grid-item {
            display: block;
            width: 100%;
            height: 100%;
            opacity: 0.85;
        }
        .overlay-layer {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 6;
        }
        .exit-square {
            position: absolute;
            box-sizing: border-box;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        .global-svg-layer {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 10;
        }
        .route-arrow {
            fill: none;
            stroke-width: 1.8;
            stroke-linecap: round;
            stroke-dasharray: 4, 3;
            animation: dash 20s linear infinite;
        }
        @keyframes dash {
            to {
                stroke-dashoffset: -1000;
            }
        }
    </style>
</head>
<body>
    <div class="grid-container" id="grid">
"""

html_end = """    </div>

    <script>
        const svgCanvas = document.getElementById('arrow-canvas');

        document.querySelectorAll('.tile-wrapper').forEach(tile => {
            tile.addEventListener('mouseenter', function() {
                const roomKey = this.getAttribute('data-room');
                const routes = ROUTES_DATA[roomKey] || [];

                let pathsHtml = '';
                routes.forEach(route => {
                    pathsHtml += `<path d="${route.d}" class="route-arrow" stroke="${route.color}" marker-end="url(#arrowhead)"/>`;
                });
                svgCanvas.innerHTML = pathsHtml;
            });

            tile.addEventListener('mouseleave', function() {
                svgCanvas.innerHTML = '';
            });
        });
    </script>
</body>
</html>
"""

def djb2_color_hash(id_a, id_b):
    sorted_ids = sorted([str(id_a), str(id_b)])
    combined_str = f"{sorted_ids[0]}<->{sorted_ids[1]}"
    hash_val = 5381
    for char in combined_str:
        hash_val = ((hash_val << 5) + hash_val) + ord(char)
        hash_val &= 0xFFFFFFFF
    return f"hsl({hash_val % 360}, 90%, 50%)"

def load_connections():
    if not os.path.exists(CONNECTIONS_JSON_PATH):
        print(f"[-] Error: {CONNECTIONS_JSON_PATH} required.")
        return []
    with open(CONNECTIONS_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f).get("connections", [])

def main():
    if not os.path.exists(IMAGE_FOLDER):
        print(f"[-] Error: '{IMAGE_FOLDER}' folder not found.")
        return

    connections = load_connections()

    # 1. Map every Origin Room to its New Destination grid slot
    grid_positions = {}
    for conn in connections:
        o = (int(conn["originNorth"]), int(conn["originEast"]))
        d = (int(conn["newDestNorth"]), int(conn["newDestEast"]))
        # Assign the room to its first discovered destination slot
        if o not in grid_positions:
            grid_positions[o] = d

    if not grid_positions:
        return

    # Calculate unified bounds based on where the rooms are ACTUALLY placed now
    min_g_n = min(pos[0] for pos in grid_positions.values())
    max_g_n = max(pos[0] for pos in grid_positions.values())
    min_g_e = min(pos[1] for pos in grid_positions.values())
    max_g_e = max(pos[1] for pos in grid_positions.values())

    cols = max_g_e - min_g_e + 1
    rows = max_g_n - min_g_n + 1

    filename_map = {}
    for fname in os.listdir(IMAGE_FOLDER):
        match = re.match(r"^(\d+)[,\-](\d+)", fname)
        if match:
            e, n = int(match.group(1)), int(match.group(2))
            filename_map[(n, e)] = fname

    js_routes_db = {f"{r[0]}_{r[1]}": [] for r in grid_positions.keys()}
    tile_step_w = TILE_WIDTH + GAP_SIZE
    tile_step_h = TILE_HEIGHT + GAP_SIZE

    # 2. Build JavaScript memory database tracking coordinates across the NEW grid mapping
    for conn in connections:
        o_n, o_e = int(conn["originNorth"]), int(conn["originEast"])
        room_key = f"{o_n}_{o_e}"

        direction = conn.get("direction")
        src_coord = conn.get("srcCoord")

        # Fallback if direction missing
        if not direction or src_coord is None:
            v_n, v_e = int(conn["vanillaDestNorth"]), int(conn["vanillaDestEast"])
            if v_n > o_n: direction = "north"
            elif v_n < o_n: direction = "south"
            elif v_e > o_e: direction = "east"
            else: direction = "west"
            src_coord = 624 / 2 if direction in ["north", "south"] else 493 / 2

        src_coord_scaled = float(src_coord) * 0.1

        # Calculate Arrow Source relative to the room's NEW mapped grid position
        src_g_n, src_g_e = grid_positions[(o_n, o_e)]
        base_x = 20 + (src_g_e - min_g_e) * tile_step_w
        base_y = 20 + (max_g_n - src_g_n) * tile_step_h

        if direction == "west":
            arrow_src_x, arrow_src_y = base_x, base_y + src_coord_scaled
        elif direction == "east":
            arrow_src_x, arrow_src_y = base_x + TILE_WIDTH, base_y + src_coord_scaled
        elif direction == "north":
            arrow_src_x, arrow_src_y = base_x + src_coord_scaled, base_y
        elif direction == "south":
            arrow_src_x, arrow_src_y = base_x + src_coord_scaled, base_y + TILE_HEIGHT

        # Calculate Arrow Destination finding where the target room was placed
        dest_o = (int(conn["newDestNorth"]), int(conn["newDestEast"]))
        dest_g_n, dest_g_e = grid_positions.get(dest_o, dest_o) # default to standard coords if missing

        dest_base_x = 20 + (dest_g_e - min_g_e) * tile_step_w
        dest_base_y = 20 + (max_g_n - dest_g_n) * tile_step_h

        # Safe Float conversion for NoneTypes
        new_x, new_y = conn.get("newX"), conn.get("newY")
        float_new_x = float(new_x) if new_x is not None else 624 / 2
        float_new_y = float(new_y) if new_y is not None else 493 / 2

        arrow_dest_x = dest_base_x + (float_new_x * 0.1)
        arrow_dest_y = dest_base_y + (float_new_y * 0.1)

        mid_x, mid_y = (arrow_src_x + arrow_dest_x) / 2, (arrow_src_y + arrow_dest_y) / 2
        if direction in ["west", "east"]:
            ctrl_x, ctrl_y = (mid_x + (12 if direction == "east" else -12), mid_y)
        else:
            ctrl_x, ctrl_y = (mid_x, mid_y + (12 if direction == "south" else -12))

        path_d = f"M {arrow_src_x:.1f} {arrow_src_y:.1f} Q {ctrl_x:.1f} {ctrl_y:.1f} {arrow_dest_x:.1f} {arrow_dest_y:.1f}"
        color = djb2_color_hash(conn["fromExitId"], conn["toExitId"])

        js_routes_db[room_key].append({
            "d": path_d,
            "color": color
        })

    # 3. Output HTML layout mapping origin images to destination positions
    html_elements = []
    for (r_north, r_east), (g_n, g_e) in grid_positions.items():
        grid_col = (g_e - min_g_e) + 1
        grid_row = (max_g_n - g_n) + 1
        room_key = f"{r_north}_{r_east}"

        # Origin image filename mapped to New Destination grid space
        img_filename = filename_map.get((r_north, r_east), "")
        img_tag = f'<img src="{IMAGE_FOLDER}/{img_filename}" class="grid-item" alt="Tile {r_east},{r_north}">' if img_filename else ''

        squares_html = []
        for conn in connections:
            if int(conn["originNorth"]) == r_north and int(conn["originEast"]) == r_east:
                color = djb2_color_hash(conn["fromExitId"], conn["toExitId"])
                direction = conn.get("direction")
                src_coord = conn.get("srcCoord")

                if not direction or src_coord is None:
                    v_n, v_e = int(conn["vanillaDestNorth"]), int(conn["vanillaDestEast"])
                    if v_n > r_north: direction = "north"
                    elif v_n < r_north: direction = "south"
                    elif v_e > r_east: direction = "east"
                    else: direction = "west"
                    src_coord = 624 / 2 if direction in ["north", "south"] else 493 / 2

                if direction in ["west", "east"]:
                    pct_y = (float(src_coord) / 493) * 100
                    x_pos = 0 if direction == "west" else 100 - BLOCK_WIDTH_PCT
                    y_pos = pct_y - (BLOCK_HEIGHT_PCT / 2)
                    squares_html.append(f'<div class="exit-square" style="left:{x_pos}%; top:{y_pos}%; width:{BLOCK_WIDTH_PCT}%; height:{BLOCK_HEIGHT_PCT}%; background-color:{color};"></div>')
                elif direction in ["north", "south"]:
                    pct_x = (float(src_coord) / 624) * 100
                    x_pos = pct_x - (BLOCK_WIDTH_PCT / 2)
                    y_pos = 0 if direction == "north" else 100 - BLOCK_HEIGHT_PCT
                    squares_html.append(f'<div class="exit-square" style="left:{x_pos}%; top:{y_pos}%; width:{BLOCK_WIDTH_PCT}%; height:{BLOCK_HEIGHT_PCT}%; background-color:{color};"></div>')

        overlay_content = "\n".join(squares_html)
        wrapper_tag = f"""        <div class="tile-wrapper" data-room="{room_key}" style="grid-column: {grid_col}; grid-row: {grid_row};" title="Origin: {r_east},{r_north} -> Placed At: {g_e},{g_n}">
            {img_tag}
            <div class="overlay-layer">
{overlay_content}
            </div>
        </div>"""
        html_elements.append(wrapper_tag)

    svg_layer = """    <svg class="global-svg-layer">
        <defs>
            <marker id="arrowhead" markerWidth="3" markerHeight="3" refX="2" refY="1.5" orient="auto">
                <polygon points="0 0, 3 1.5, 0 3" fill="#fff" />
            </marker>
        </defs>
        <g id="arrow-canvas"></g>
    </svg>"""

    # Inject dynamic grid rows and columns bounds directly into the HTML
    dynamic_html_start = html_start.replace('id="grid"', f'id="grid" style="--cols: {cols}; --rows: {rows};"')

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(dynamic_html_start)
        f.write("\n".join(html_elements))
        f.write("\n" + svg_layer)
        f.write(f"\n    <script>const ROUTES_DATA = {json.dumps(js_routes_db, indent=2)};</script>")
        f.write("\n" + html_end)

    print(f"[+] Success! Layout calculations aligned perfectly inside {OUTPUT_FILE}")

if __name__ == "__main__":
    main()