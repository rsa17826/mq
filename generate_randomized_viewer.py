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
        /* FIXED: Switched to relative box container instead of standard CSS Grid track lines */
        .grid-container {
            position: relative;
            padding: 20px;
            margin: 0;
        }
        .tile-wrapper {
            position: absolute;
            width: 62.4px;
            height: 49.3px;
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
            z-index: 100;
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
                    geom_db[key] = room.get("exits", {})
    except Exception as err:
        print(f"[-] Failed to read room geometry config details: {err}")
    return geom_db

def main():
    if not os.path.exists(IMAGE_FOLDER):
        print(f"[-] Error: '{IMAGE_FOLDER}' folder not found.")
        return

    connections = load_connections()
    geom_index = load_geometry_map()

    files = os.listdir(IMAGE_FOLDER)
    parsed_tiles = []

    for filename in files:
        match = re.match(r"^(\d+)[,\-](\d+)", filename)
        if match:
            east = int(match.group(1))
            north = int(match.group(2))
            parsed_tiles.append((east, north, filename))

    if not parsed_tiles:
        print("[-] No valid tiles found in image folder.")
        return

    # FIXED: Map large sparse gaps into sequential track lists to clear empty row blocks
    unique_norths = sorted(list(set(t[1] for t in parsed_tiles)), reverse=True)
    unique_easts = sorted(list(set(t[0] for t in parsed_tiles)))

    north_to_track = {n: idx for idx, n in enumerate(unique_norths)}
    east_to_track = {e: idx for idx, e in enumerate(unique_easts)}

    cols = len(unique_easts)
    rows = len(unique_norths)

    js_routes_db = {f"{t[1]}_{t[0]}": [] for t in parsed_tiles}
    tile_step_w = TILE_WIDTH + GAP_SIZE
    tile_step_h = TILE_HEIGHT + GAP_SIZE

    # 1. Compute arrows tracking compact positional mapping layout offsets
    for conn in connections:
        o_n, o_e = int(conn["originNorth"]), int(conn["originEast"])
        room_key = f"{o_n}_{o_e}"

        if o_n not in north_to_track or o_e not in east_to_track:
            continue

        direction = conn.get("direction")
        src_coord = conn.get("srcCoord")

        if not direction or src_coord is None:
            v_n, v_e = int(conn["vanillaDestNorth"]), int(conn["vanillaDestEast"])
            if v_n > o_n: direction = "north"
            elif v_n < o_n: direction = "south"
            elif v_e > o_e: direction = "east"
            else: direction = "west"
            src_coord = 624 / 2 if direction in ["north", "south"] else 493 / 2

        src_coord_scaled = float(src_coord) * 0.1

        # Calculate using track sequences
        track_col = east_to_track[o_e]
        track_row = north_to_track[o_n]
        base_x = 20 + track_col * tile_step_w
        base_y = 20 + track_row * tile_step_h

        if direction == "west":
            arrow_src_x, arrow_src_y = base_x, base_y + src_coord_scaled
        elif direction == "east":
            arrow_src_x, arrow_src_y = base_x + TILE_WIDTH, base_y + src_coord_scaled
        elif direction == "north":
            arrow_src_x, arrow_src_y = base_x + src_coord_scaled, base_y
        elif direction == "south":
            arrow_src_x, arrow_src_y = base_x + src_coord_scaled, base_y + TILE_HEIGHT

        dest_o_n, dest_o_e = int(conn["newDestNorth"]), int(conn["newDestEast"])

        # Fallback to current space if values don't exist in the parsed collection map bounds
        dest_track_col = east_to_track.get(dest_o_e, track_col)
        dest_track_row = north_to_track.get(dest_o_n, track_row)

        dest_base_x = 20 + dest_track_col * tile_step_w
        dest_base_y = 20 + dest_track_row * tile_step_h

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

        if room_key in js_routes_db:
            js_routes_db[room_key].append({
                "d": path_d,
                "color": color
            })

    # 2. Render absolute positions directly to strip the blank spaces
    html_elements = []
    for east, north, filename in parsed_tiles:
        track_col = east_to_track[east]
        track_row = north_to_track[north]

        # Explicit absolute translation metrics style assignment
        pixel_left = 20 + track_col * tile_step_w
        pixel_top = 20 + track_row * tile_step_h
        room_key = f"{north}_{east}"

        img_path = f"{IMAGE_FOLDER}/{filename}"
        tile_exits = geom_index.get(room_key, {})
        squares_html = []

        active_connections = [
            c for c in connections
            if int(c["originNorth"]) == north and int(c["originEast"]) == east
        ]

        if tile_exits and isinstance(tile_exits, dict):
            for side, bounds_list in tile_exits.items():
                if not bounds_list:
                    continue

                if not isinstance(bounds_list, list):
                    bounds_list = [bounds_list]

                for bounds in bounds_list:
                    if not bounds or not isinstance(bounds, dict):
                        continue

                    matched_color = "rgba(255,255,255,0.5)"
                    for conn in active_connections:
                        if conn.get("direction") == side:
                            matched_color = djb2_color_hash(conn["fromExitId"], conn["toExitId"])
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
                            f'<div class="exit-square" style="left:{x_pos}%; top:{y_pos}%; width:{w_size}%; height:{h_size}%; background-color:{matched_color};"></div>'
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
                            f'<div class="exit-square" style="left:{x_pos}%; top:{y_pos}%; width:{w_size}%; height:{h_size}%; background-color:{matched_color};"></div>'
                        )

        overlay_content = "\n".join(squares_html)
        wrapper_tag = f"""        <div class="tile-wrapper" data-room="{room_key}" style="left: {pixel_left:.1f}px; top: {pixel_top:.1f}px;" title="Position: {east},{north}">
            <img src="{img_path}" class="grid-item" alt="Tile {east},{north}">
            <div class="overlay-layer">
{overlay_content}
            </div>
        </div>"""
        html_elements.append(wrapper_tag)

    total_svg_width = 40 + (cols * tile_step_w)
    total_svg_height = 40 + (rows * tile_step_h)

    # Set container limits to allow natural absolute layout box matching sizing properties
    container_style = f'id="grid" style="width: {total_svg_width}px; height: {total_svg_height}px;"'
    dynamic_html_start = html_start.replace('id="grid"', container_style)

    svg_layer = f"""    <svg class="global-svg-layer" style="width: {total_svg_width}px; height: {total_svg_height}px;">
        <defs>
            <marker id="arrowhead" markerWidth="3" markerHeight="3" refX="2" refY="1.5" orient="auto">
                <polygon points="0 0, 3 1.5, 0 3" fill="#fff" />
            </marker>
        </defs>
        <g id="arrow-canvas"></g>
    </svg>"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(dynamic_html_start)
        f.write("\n".join(html_elements))
        f.write("\n" + svg_layer)
        f.write(f"\n    <script>const ROUTES_DATA = {json.dumps(js_routes_db, indent=2)};</script>")
        f.write("\n" + html_end)

    print(f"[+] Success! Cleanly compressed absolute positioning mapping completed inside {OUTPUT_FILE}")

if __name__ == "__main__":
    main()