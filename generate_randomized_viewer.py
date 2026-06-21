import os
import re
import json

# Target folder pointing to the downsized versions
IMAGE_FOLDER = "mapSmall"
OUTPUT_FILE = "randomized_index.html"
GEOMETRY_JSON_PATH = "./room_geometry.json"
CONNECTIONS_JSON_PATH = "./connections.json"
PROGRESSION_JSON_PATH = "./progression.json"

# Path to the icon image representing progression events (adjust filename as needed)
PROGRESSION_ICON_PATH = "./mapimgs/"

# Constants scaled down to 10% to match the downsized image sizes perfectly
TILE_WIDTH = 149.76
TILE_HEIGHT = 118.32
BLOCKS_X = 14
BLOCKS_Y = 11

BLOCK_WIDTH_PCT = 100 / BLOCKS_X
BLOCK_HEIGHT_PCT = 100 / BLOCKS_Y
GAP_SIZE = 0 # Sizing gap between tiles

html_start = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>High-Performance Interactive Map Viewer</title>
    <style>
        html, body {{
            margin: 0;
            background-color: #111;
            color: #fff;
            font-family: sans-serif;
            scrollbar-width: none;
            -ms-overflow-style: none;
        }}
        html::-webkit-scrollbar, body::-webkit-scrollbar {{
            display: none;
        }}
        .fr {{
            display:flex;
            flex-direction:row;
            gap:4px;
            position: absolute;
            bottom: calc(3px + {BLOCK_WIDTH_PCT}%);
            right: calc(3px + {BLOCK_WIDTH_PCT}%);
            pointer-events: none;
            z-index:9999999999;
        }}
        .grid-container {{
            position: relative;
            padding: 20px;
            margin: 0;
        }}
        .tile-wrapper {{
            position: absolute;
            width: {TILE_WIDTH}px;
            height: {TILE_HEIGHT}px;
            background-color: #222;
            border: 1px solid #444;
            box-sizing: border-box;
            z-index: 5;
            transition: border-color 0.1s ease-in-out;
        }}
        .tile-wrapper:hover {{
            border-color: #fff;
            z-index: 15;
        }}
        .grid-item {{
            display: block;
            width: 100%;
            height: 100%;
            opacity: 0.85;
        }}
        .overlay-layer {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 6;
        }}
        .exit-square {{
            position: absolute;
            box-sizing: border-box;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}
        .progression-icon {{
            width: 14px;
            height: 14px;
            z-index: 12;
            filter: drop-shadow(0px 1px 2px rgba(0,0,0,0.8));
        }}
        .global-svg-layer {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 100;
        }}
        .route-arrow {{
            fill: none;
            stroke-width: 1.8;
            stroke-linecap: round;
            stroke-dasharray: 4, 3;
            animation: dash 20s linear infinite;
        }}
        @keyframes dash {{
            to {{
                stroke-dashoffset: -1000;
            }}
        }}
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
    return f"hsla({hash_val % 360}, 90%, 50%, 60%)"

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

def load_progression_map():
    prog_db = {}
    if not os.path.exists(PROGRESSION_JSON_PATH):
        print(f"[-] Warn: {PROGRESSION_JSON_PATH} not found.")
        return prog_db
    try:
        with open(PROGRESSION_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            for loc in data.get("locations", []):
                room_coord = loc.get("room")
                if room_coord and "north" in room_coord and "east" in room_coord:
                    n = int(room_coord["north"])
                    e = int(room_coord["east"])
                    key = f"{n}_{e}"
                    if key not in prog_db:
                        prog_db[key] = []
                    prog_db[key].append(loc)
    except Exception as err:
        print(f"[-] Failed to read progression config details: {err}")
    return prog_db

def build_tooltip_text(north, east, prog_entries):
    title_lines = [f"Position: {north},{east}"]

    if not prog_entries:
        return "\n".join(title_lines)

    for idx, entry in enumerate(prog_entries):
        if len(prog_entries) > 1:
            title_lines.append(f"--- Event #{idx + 1} ---")

        if "info" in entry:
            title_lines.append(f"Info: {entry['info']}")

        if "requires" in entry:
            req_groups = []
            for group in entry["requires"]:
                req_groups.append(" AND ".join(group))
            req_str = " OR ".join(f"({r})" for r in req_groups) if len(req_groups) > 1 else req_groups[0]
            title_lines.append(f"Requires: {req_str}")

        if "receive" in entry:
            rec_str = ", ".join(entry["receive"])
            title_lines.append(f"Receive: {rec_str}")

    return "\n".join(title_lines)

def main():
    if not os.path.exists(IMAGE_FOLDER):
        print(f"[-] Error: '{IMAGE_FOLDER}' folder not found.")
        return

    connections = load_connections()
    geom_index = load_geometry_map()
    prog_index = load_progression_map()

    files = os.listdir(IMAGE_FOLDER)
    parsed_tiles = []

    for filename in files:
        match = re.match(r"^(\d+)[,\-](\d+)", filename)
        if match:
            north = int(match.group(1))
            east = int(match.group(2))
            parsed_tiles.append((north, east, filename))

    if not parsed_tiles:
        print("[-] No valid tiles found in image folder.")
        return

    unique_norths = sorted(list(set(t[0] for t in parsed_tiles)), reverse=True)
    unique_easts = sorted(list(set(t[1] for t in parsed_tiles)))

    north_to_track = {n: idx for idx, n in enumerate(unique_norths)}
    east_to_track = {e: idx for idx, e in enumerate(unique_easts)}

    cols = len(unique_easts)
    rows = len(unique_norths)

    js_routes_db = {f"{north}_{east}": [] for north, east, _ in parsed_tiles}
    tile_step_w = TILE_WIDTH + GAP_SIZE
    tile_step_h = TILE_HEIGHT + GAP_SIZE

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

    html_elements = []
    for north, east, filename in parsed_tiles:
        track_col = east_to_track[east]
        track_row = north_to_track[north]

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

                side_connections = [
                    c for c in active_connections
                    if c.get("direction") == side and c.get("srcCoord") is not None
                ]
                side_connections.sort(key=lambda c: float(c["srcCoord"]))

                if side in ["west", "east"]:
                    sorted_bounds = sorted(bounds_list, key=lambda b: int(float(b.get("top", 0))))
                else:
                    sorted_bounds = sorted(bounds_list, key=lambda b: int(float(b.get("left", 0))))

                for idx, bounds in enumerate(sorted_bounds):
                    if not bounds or not isinstance(bounds, dict):
                        continue

                    matched_color = "rgba(255,255,255,0.5)"
                    if idx < len(side_connections):
                        conn = side_connections[idx]
                        matched_color = djb2_color_hash(conn["fromExitId"], conn["toExitId"])

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

        # Pull progression events for this specific room
        room_prog_data = prog_index.get(room_key, [])
        tooltip_str = build_tooltip_text(north, east, room_prog_data)

        # Generate an icon tag if the room demands actions (has requires or receive entries)
        icon_html = "<span class=fr>"

        # Pull progression events for this specific room
        room_prog_data = prog_index.get(room_key, [])
        tooltip_str = build_tooltip_text(north, east, room_prog_data)

        # Replicating JavaScript .map(e => e?.receive).unique() dynamically in Python
        unique_receives = set()
        for entry in room_prog_data:
            receive_list = entry.get("receive")
            if receive_list and isinstance(receive_list, list):
                for item in receive_list:
                    if item: # Ensure item is not null/empty
                        unique_receives.add(item)

        # Generate individual icon tags for each unique item type found
        icon_html = "<span class=fr>"
        for item in sorted(unique_receives): # Sorting ensures stable element ordering
            # Sanitize colons, hash symbols, or question marks into underscores
            sanitized_name = re.sub(r"[:#?]", "_", re.sub(r"[#?].+$", "", item))
            icon_filename = f"{sanitized_name}.png"
            icon_src = os.path.join(PROGRESSION_ICON_PATH, icon_filename).replace("\\", "/")

            icon_html += f'\n            <img src="{icon_src}" class="progression-icon" alt="{item}" title="{item}">'
        icon_html += "</span>"

        overlay_content = "\n".join(squares_html)
        wrapper_tag = f"""        <div class="tile-wrapper" data-room="{room_key}" style="left: {pixel_left:.1f}px; top: {pixel_top:.1f}px;" title="{tooltip_str}">
            <img src="{img_path}" class="grid-item" alt="Tile {north},{east}">{icon_html}
            <div class="overlay-layer">
{overlay_content}
            </div>
        </div>"""
        html_elements.append(wrapper_tag)

    total_svg_width = 40 + (cols * tile_step_w)
    total_svg_height = 40 + (rows * tile_step_h)

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

    print(f"[+] Success! Cleanly integrated progression tooltips and icons into {OUTPUT_FILE}")

if __name__ == "__main__":
    main()