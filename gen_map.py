# @noregex
import json
import os
import re

# make warp colors same color on each side!!!
# make warps show correct dest not vinela dest!!!!!!!!!!!1

# Target folder pointing to the downsized versions
FULL_IMAGE_FOLDER = "map"

OUTPUT_FILE = "randomized_index.html"
CONNECTIONS_JSON_PATH = "./json/connections.json"

# Path to the icon image representing progression events
PROGRESSION_ICON_PATH = "/mapimgs/"

# Constants scaled down to match the layout sizes perfectly
TILE_WIDTH = 710
TILE_HEIGHT = 560
BLOCKS_X = 14
BLOCKS_Y = 11

BLOCK_WIDTH_PCT = 100 / BLOCKS_X
BLOCK_HEIGHT_PCT = 100 / BLOCKS_Y

# Local coordinate dimensions from game engine data structures
ROOM_INTERNAL_WIDTH = 710.0
ROOM_INTERNAL_HEIGHT = 560.0

html_start = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>High-Performance Interactive Map Viewer</title>
    <style>
        img {{
            pointer-events:none;
        }}
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
        #viewport {{
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            position: relative;
        }}
        /* Info Panel Top Right */
        #info-panel {{
            position: absolute;
            top: 20px;
            right: 20px;
            width: 320px;
            max-height: 85vh;
            background: rgba(20, 20, 20, 0.92);
            backdrop-filter: blur(8px);
            border: 1px solid #444;
            border-radius: 8px;
            padding: 16px;
            box-sizing: border-box;
            z-index: 10000000;
            pointer-events: none;
            font-family: monospace;
            font-size: 13px;
            line-height: 1.6;
            box-shadow: 0 4px 20px rgba(0,0,0,0.6);
            color: #e0e0e0;
            overflow-y: auto;
        }}
        .info-header {{
            font-weight: bold;
            border-bottom: 1px solid #555;
            padding-bottom: 4px;
            margin-bottom: 8px;
            color: #fff;
        }}
        .info-event-sep {{
            border-top: 1px dashed #444;
            margin: 8px 0;
            padding-top: 8px;
        }}
        .info-line {{
            margin: 6px 0;
        }}
        .info-item-token {{
            white-space: nowrap;
            display: inline-flex;
            align-items: center;
            background: rgba(255, 255, 255, 0.05);
            padding: 2px 6px;
            border-radius: 4px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin: 2px;
            vertical-align: middle;
        }}
        .info-inline-icon {{
            height: 18px;
            width: auto;
            margin-right: 6px;
            filter: drop-shadow(0px 1px 1px rgba(0,0,0,0.8));
        }}
        #pan-layer {{
            position: absolute;
            top: 0;
            left: 0;
            z-index: 1;
        }}
        #grid {{
            position: relative;
            transform-origin: 0 0;
        }}
        .tile-wrapper {{
            position: absolute;
            width: {TILE_WIDTH}px;
            height: {TILE_HEIGHT}px;
            box-sizing: border-box;
            z-index: 5;
            background-repeat: no-repeat;
            background-size: 100% 100%;
            image-rendering: pixelated;
            image-rendering: crisp-edges;
        }}
        .fc {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            align-items:right;
            position: absolute;
            bottom: calc(3px + {BLOCK_HEIGHT_PCT}%);
            right: calc(3px + {BLOCK_WIDTH_PCT}%);
            pointer-events: none;
            z-index: 9999999999;
        }}
        .fr {{
            display: flex;
            flex-direction: row;
            gap: 4px;
            margin-left: auto;
            pointer-events: none;
            z-index: 9999999999;
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
        .warp-square {{
            position: absolute;
            box-sizing: border-box;
            border: 1.5px dashed #00ffff;
            background-color: rgba(0, 255, 255, 0.2);
            border-radius: 50%;
        }}
        .progression-icon {{
            height: 32px;
            z-index: 12;
            filter: drop-shadow(0px 1px 2px rgba(0,0,0,0.8));
        }}
        .tile-wrapper.room-has-available-item {{
            outline: 10px solid #2020aa;
            outline-offset: -11px;
            z-index: 20;
        }}
        .tile-wrapper.room-has-available-quest {{
            outline: 10px solid #f1c40f;
            outline-offset: -11px;
            z-index: 20;
        }}
        .progression-icon.checked {{
            filter: grayscale(1) brightness(0.55);
            outline: 5px solid #20aa20;
            outline-offset: -4px;
            border-radius: 4px;
        }}
        .progression-icon.in-logic {{
            outline: 5px solid #f1c40f;
            outline-offset: -4px;
            border-radius: 4px;
        }}
        .progression-icon.route-unknown {{
            outline: 5px dashed #e67e22;
            outline-offset: -4px;
            border-radius: 4px;
        }}
        .progression-icon.out-of-logic {{
            filter: grayscale(1) opacity(0.35);
        }}
        .tile-wrapper.room-partial {{
            filter: grayscale(0.5) brightness(0.75);
        }}
        .tile-wrapper.room-unreachable {{
            filter: grayscale(1) brightness(0.45);
        }}
        #arrow-canvas-2d {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 999999;
        }}
    </style>
</head>
<body>
<div id="viewport">
    <div id="info-panel">Hover over a room to view details.</div>
    <div id="pan-layer">
        <div id="grid">
"""

html_end = r"""    </div>
    </div>
    <canvas id="arrow-canvas-2d"></canvas>
</div>
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
    return json.load(f)["connections"]


def load_doors():
  from _exits import EXITS

  return EXITS["doors"]


def load_geometry_map():
  from _room_geometry import GEOM

  geom_db = {}
  for room in GEOM:
    if "north" in room and "east" in room:
      n = int(float(room["north"]))
      e = int(float(room["east"]))
      key = f"{n}_{e}"
      geom_db[key] = room.get("exits", {})
  return geom_db


def load_progression_map():
  prog_db = {}
  try:
    from _progression import PROG as data

    for loc in data:
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


def get_item_token_html(item_name):
  """Generates an HTML token where item name and icon are kept unbroken together."""
  sanitized_name = re.sub(r"[:#?]", "_", re.sub(r"[#?].+$", "", item_name))
  icon_filename = f"{sanitized_name}.png"
  icon_src = os.path.join(PROGRESSION_ICON_PATH, icon_filename).replace("\\", "/")
  return f'<span class="info-item-token"><img src="{icon_src}" class="info-inline-icon" alt="{item_name}">{item_name}</span>'


def build_room_info_json(north, east, prog_entries):
  info_data = {"north": north, "east": east, "entries": []}
  for entry in prog_entries:
    parsed_entry = {}
    if "info" in entry:
      parsed_entry["info"] = entry["info"]

    # Omit 'Requires' section entirely if empty or only contains empty groups
    if "requires" in entry and len(entry["requires"]) > 0 and any(group for group in entry["requires"]):
      req_groups = []
      for group in entry["requires"]:
        item_htmls = [get_item_token_html(item) for item in group if item]
        if item_htmls:
          req_groups.append(" AND ".join(item_htmls))
      if req_groups:
        parsed_entry["requiresHtml"] = " OR ".join(f"({r})" for r in req_groups) if len(req_groups) > 1 else req_groups[0]

    if "receive" in entry and len(entry["receive"]) > 0:
      rec_htmls = [get_item_token_html(item) for item in entry["receive"] if item]
      if rec_htmls:
        parsed_entry["receiveHtml"] = ", ".join(rec_htmls)

    info_data["entries"].append(parsed_entry)
  return json.dumps(info_data).replace('"', "&quot;")


def main():
  connections = load_connections()
  doors = load_doors()
  geom_index = load_geometry_map()
  exit_lookup = {}

  for room_key, exits in geom_index.items():
    exit_lookup[room_key] = {}
    for side, bounds_list in exits.items():
      if not bounds_list:
        continue
      if not isinstance(bounds_list, list):
        bounds_list = [bounds_list]
      processed = []
      for b in bounds_list:
        if not isinstance(b, dict):
          continue
        if side in ["west", "east"]:
          start = int(float(b["top"]))
          end = int(float(b["bottom"]))
          center_block = (start + end) / 2
          processed.append({"side": side, "block": center_block})
        else:
          start = int(float(b["left"]))
          end = int(float(b["right"]))
          center_block = (start + end) / 2
          processed.append({"side": side, "block": center_block})
      exit_lookup[room_key][side] = processed

  prog_index = load_progression_map()
  conn_override_index = {str(c["fromExitId"]): c for c in connections if "fromExitId" in c}
  door_ids = {str(d["id"]) for d in doors}

  files = os.listdir(FULL_IMAGE_FOLDER)
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
  js_exits_db = {f"{north}_{east}": [] for north, east, _ in parsed_tiles}

  scale_x_conn = TILE_WIDTH / ROOM_INTERNAL_WIDTH
  scale_y_conn = TILE_HEIGHT / ROOM_INTERNAL_HEIGHT
  scale_x_room = TILE_WIDTH / ROOM_INTERNAL_WIDTH
  scale_y_room = TILE_HEIGHT / ROOM_INTERNAL_HEIGHT

  half_block_x_room_scaled = (ROOM_INTERNAL_WIDTH / (2 * BLOCKS_X)) * scale_x_room
  half_block_y_room_scaled = (ROOM_INTERNAL_HEIGHT / (2 * BLOCKS_Y)) * scale_y_room

  for conn in connections:
    o_n, o_e = int(conn["north"]), int(conn["east"])
    room_key = f"{o_n}_{o_e}"
    if o_n not in north_to_track or o_e not in east_to_track:
      continue

    direction = conn.get("direction")
    if str(conn.get("fromExitId")) in door_ids or direction == "warp":
      continue

    src_coord = conn.get("srcCoord")
    if not direction or src_coord is None:
      continue

    src_coord_scaled = float(src_coord) * (scale_x_conn if direction in ["north", "south"] else scale_y_conn)

    track_col = east_to_track[o_e]
    track_row = north_to_track[o_n]
    base_x = track_col * TILE_WIDTH
    base_y = track_row * TILE_HEIGHT
    halfTileWidth = (TILE_WIDTH / BLOCKS_X) / 2
    halfTileHeight = (TILE_HEIGHT / BLOCKS_Y) / 2

    dest_o_n, dest_o_e = int(conn["id"].split("_")[2]), int(conn["id"].split("_")[3])
    dest_track_col = east_to_track.get(dest_o_e, track_col)
    dest_track_row = north_to_track.get(dest_o_n, track_row)

    dest_base_x = dest_track_col * TILE_WIDTH
    dest_base_y = dest_track_row * TILE_HEIGHT

    new_x, new_y = conn.get("newX"), conn.get("newY")
    float_new_x = float(new_x) if new_x is not None else ROOM_INTERNAL_WIDTH / 2
    float_new_y = float(new_y) if new_y is not None else ROOM_INTERNAL_HEIGHT / 2

    raw_dest_x = dest_base_x + (float_new_x * scale_x_conn)
    raw_dest_y = dest_base_y + (float_new_y * scale_y_conn)

    if direction == "west":
      arrow_src_x, arrow_src_y = base_x + halfTileWidth, base_y + src_coord_scaled
      arrow_dest_x, arrow_dest_y = raw_dest_x + (halfTileWidth * 2), raw_dest_y
    elif direction == "east":
      arrow_src_x, arrow_src_y = base_x + TILE_WIDTH - halfTileWidth, base_y + src_coord_scaled
      arrow_dest_x, arrow_dest_y = raw_dest_x - (halfTileWidth * 2), raw_dest_y
    elif direction == "north":
      arrow_src_x, arrow_src_y = base_x + src_coord_scaled, base_y + halfTileHeight
      arrow_dest_x, arrow_dest_y = raw_dest_x, raw_dest_y + (halfTileHeight * 2)
    elif direction == "south":
      arrow_src_x, arrow_src_y = base_x + src_coord_scaled, base_y + TILE_HEIGHT - halfTileHeight
      arrow_dest_x, arrow_dest_y = raw_dest_x, raw_dest_y - (halfTileHeight * 2)

    mid_x, mid_y = (arrow_src_x + arrow_dest_x) / 2, (arrow_src_y + arrow_dest_y) / 2
    if direction in ["west", "east"]:
      ctrl_x, ctrl_y = (mid_x + (25 if direction == "east" else -25), mid_y)
    else:
      ctrl_x, ctrl_y = (mid_x, mid_y + (25 if direction == "south" else -25))
    newid = [*map(float, conn["id"].split("_"))]
    match conn["direction"]:
      case "north":
        newid[2] += 1
      case "south":
        newid[2] -= 1
      case "east":
        newid[3] += 1
      case "west":
        newid[3] -= 1
    color = djb2_color_hash(conn["id"], "_".join(map(str, newid)))

    if room_key in js_routes_db:
      js_routes_db[room_key].append({"d": [arrow_src_x, arrow_src_y, ctrl_x, ctrl_y, arrow_dest_x, arrow_dest_y], "color": color})

  room_doors_index = {}
  for d in doors:
    o_n, o_e = int(d["origin"]["north"]), int(d["origin"]["east"])
    d_n, d_e = int(d["dest"]["north"]), int(d["dest"]["east"])
    room_doors_index[f"{o_n}_{o_e}->{d_n}_{d_e}"] = d

  for d in doors:
    o_n, o_e = int(d["origin"]["north"]), int(d["origin"]["east"])
    v_dest_n, v_dest_e = int(d["dest"]["north"]), int(d["dest"]["east"])
    door_id_str = str(d["id"])

    src_x_local, src_y_local = snapToGrid(d["dest_x"], d["dest_y"])
    override = conn_override_index.get(door_id_str)
    if override:
      d_n, d_e = int(override["id"].split("_")[2]), int(override["id"].split("_")[3])
      ov_x, ov_y = override.get("newX"), override.get("newY")
      if ov_x is not None and ov_y is not None:
        dest_x_local, dest_y_local = snapToGrid(float(ov_x), float(ov_y))
      else:
        dest_x_local = ROOM_INTERNAL_WIDTH / 2
        dest_y_local = ROOM_INTERNAL_HEIGHT / 2
      to_exit_id = override.get("toExitId", "warp_gate")
      color = djb2_color_hash(d["id"], to_exit_id)
    else:
      d_n, d_e = int(d["dest"]["north"]), int(d["dest"]["east"])
      reverse_door = room_doors_index.get(f"{d_n}_{d_e}->{o_n}_{o_e}")
      if reverse_door:
        dest_x_local, dest_y_local = snapToGrid(reverse_door["dest_x"], reverse_door["dest_y"])
        color = djb2_color_hash(d["id"], reverse_door["id"])
      else:
        dest_x_local = ROOM_INTERNAL_WIDTH / 2
        dest_y_local = ROOM_INTERNAL_HEIGHT / 2
        color = djb2_color_hash(d["id"], "warp_gate")

    room_key = f"{o_n}_{o_e}"
    if o_n not in north_to_track or o_e not in east_to_track:
      continue
    if d_n not in north_to_track or d_e not in east_to_track:
      continue

    orig_col, orig_row = east_to_track[o_e], north_to_track[o_n]
    dest_col, dest_row = east_to_track[d_e], north_to_track[d_n]

    arrow_src_x = orig_col * TILE_WIDTH + (src_x_local * scale_x_room) + half_block_x_room_scaled
    arrow_src_y = orig_row * TILE_HEIGHT + (src_y_local * scale_y_room) + half_block_y_room_scaled
    arrow_dest_x = dest_col * TILE_WIDTH + (dest_x_local * scale_x_room) + half_block_x_room_scaled
    arrow_dest_y = dest_row * TILE_HEIGHT + (dest_y_local * scale_y_room) + half_block_y_room_scaled

    m_x, m_y = (arrow_src_x + arrow_dest_x) / 2, (arrow_src_y + arrow_dest_y) / 2
    ctrl_x, ctrl_y = m_x, m_y - 45

    if room_key in js_routes_db:
      js_routes_db[room_key].append({"d": [arrow_src_x, arrow_src_y, ctrl_x, ctrl_y, arrow_dest_x, arrow_dest_y], "color": color})

  canvas_tiles_data = []
  html_elements = []
  for north, east, filename in parsed_tiles:
    track_col = east_to_track[east]
    track_row = north_to_track[north]

    pixel_left = track_col * TILE_WIDTH
    pixel_top = track_row * TILE_HEIGHT
    room_key = f"{north}_{east}"

    placeholder_img_path = f"/map_07/{filename}"
    highres_img_path = f"/{FULL_IMAGE_FOLDER}/{filename}"

    tile_exits = geom_index.get(room_key, {})
    squares_html = []

    active_connections = [c for c in connections if int(c["north"]) == north and int(c["east"]) == east]

    if tile_exits and isinstance(tile_exits, dict):
      for side, bounds_list in tile_exits.items():
        if not bounds_list:
          continue
        if not isinstance(bounds_list, list):
          bounds_list = [bounds_list]

        side_connections = [c for c in active_connections if c.get("direction") == side and c.get("srcCoord") is not None]
        side_connections.sort(key=lambda c: float(c["srcCoord"]))

        if side in ["west", "east"]:
          sorted_bounds = sorted(bounds_list, key=lambda b: int(float(b.get("top", 0))))
        else:
          sorted_bounds = sorted(bounds_list, key=lambda b: int(float(b.get("left", 0))))

        for idx, bounds in enumerate(sorted_bounds):
          if not bounds or not isinstance(bounds, dict):
            continue

          matched_color = "rgba(255,255,255,0.5)"
          connection_id = None
          if idx < len(side_connections):
            conn = side_connections[idx]
            newid = [*map(float, conn["id"].split("_"))]
            match conn["direction"]:
              case "north":
                newid[2] += 1
              case "south":
                newid[2] -= 1
              case "east":
                newid[3] += 1
              case "west":
                newid[3] -= 1

            matched_color = djb2_color_hash(conn["id"], "_".join(map(str, newid)))
            connection_id = "_".join(map(str, newid))

          if side in ["west", "east"]:
            if bounds.get("top") is None or bounds.get("bottom") is None:
              continue
            start_val = int(float(bounds["top"]))
            end_val = int(float(bounds["bottom"]))

            x_pos = 0 if side == "west" else 100 - BLOCK_WIDTH_PCT
            y_pos = start_val * BLOCK_HEIGHT_PCT
            w_size = BLOCK_WIDTH_PCT
            h_size = ((end_val - start_val) + 1) * BLOCK_HEIGHT_PCT

            squares_html.append(f'<div class="exit-square" style="left:{x_pos}%; top:{y_pos}%; width:{w_size}%; height:{h_size}%; background-color:{matched_color};"></div>')
            js_exits_db[room_key].append(
              {
                "side": side,
                "top": start_val,
                "bottom": end_val,
                "color": matched_color,
                "connectionId": connection_id,
              }
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

            squares_html.append(f'<div class="exit-square" style="left:{x_pos}%; top:{y_pos}%; width:{w_size}%; height:{h_size}%; background-color:{matched_color};"></div>')
            js_exits_db[room_key].append(
              {
                "side": side,
                "left": start_val,
                "right": end_val,
                "color": matched_color,
                "connectionId": connection_id,
              }
            )

    for d in doors:
      o_n, o_e = int(d["origin"]["north"]), int(d["origin"]["east"])
      v_dest_n, v_dest_e = int(d["dest"]["north"]), int(d["dest"]["east"])

      door_id_str = str(d["id"])
      if door_id_str in conn_override_index:
        override = conn_override_index[door_id_str]
        d_n, d_e = int(override["id"].split("_")[2]), int(override["id"].split("_")[3])
        if override.get("newX") is not None and override.get("newY") is not None:
          dest_x_local = float(override["newX"])
          dest_y_local = float(override["newY"])
        else:
          dest_x_local = float(d["dest_x"])
          dest_y_local = float(d["dest_y"])
      else:
        d_n, d_e = int(d["dest"]["north"]), int(d["dest"]["east"])
        dest_x_local = float(d["dest_x"])
        dest_y_local = float(d["dest_y"])

      if d_n == north and d_e == east:
        x_pos_local, y_pos_local = snapToGrid(dest_x_local, dest_y_local)
        x_pos_pct = (x_pos_local / ROOM_INTERNAL_WIDTH) * 100
        y_pos_pct = (y_pos_local / ROOM_INTERNAL_HEIGHT) * 100

        squares_html.append(f'<div class="warp-square" style="left:{x_pos_pct:.2f}%; top:{y_pos_pct:.2f}%; width:{BLOCK_WIDTH_PCT:.2f}%; height:{BLOCK_HEIGHT_PCT:.2f}%;"></div>')
        js_exits_db[room_key].append(
          {
            "side": "warp",
            "x": round(x_pos_local * BLOCKS_X / ROOM_INTERNAL_WIDTH),
            "y": 11 - round(y_pos_local * BLOCKS_Y / ROOM_INTERNAL_HEIGHT),
            "color": "#1157",
          }
        )

    room_prog_data = prog_index.get(room_key, [])
    info_json_str = build_room_info_json(north, east, room_prog_data)

    unique_receives = set()
    for entry in room_prog_data:
      receive_list = entry.get("receive")
      if receive_list and isinstance(receive_list, list):
        for item in receive_list:
          if item:
            unique_receives.add(item)

    icon_html = "<span class=fc>"
    icon_html += "<span class=fr>"
    ITEM_NAMES = (
      "magic:",
      "weapon:",
      # "flag:final boss dead",
      "permit:",
      "misc:fire crystal",
      "loot:key",
      "item:gold",
      "item:",
      "skill:",
      "food:",
      "flag:magic only resist bypass",
      "misc:blue crystal",
      "misc:headstoneSwitch1",
      "misc:headstoneSwitch2",
      "misc:headstoneSwitch3",
      "misc:headstoneSwitch4",
      # "entrance.",
      "armor:",
      # "quest:",
      # "area:",
      "item:ring",
      "item:aurastones",
      "misc:",
      "craft:",
    )
    for item in sorted(unique_receives):
      if item.startswith(ITEM_NAMES):
        sanitized_name = re.sub(r"[:#?]", "_", re.sub(r"[#?].+$", "", item))
        icon_filename = f"{sanitized_name}.png"
        icon_src = os.path.join(PROGRESSION_ICON_PATH, icon_filename).replace("\\", "/")
        # match the exact key format used when AP_LOCATION_IDS was generated:
        # f"{north}_{east} - {itemInfo.split('#')[0]}"
        base_item_name = item.split("#")[0]
        location_key = f"{room_key} - {base_item_name}".replace('"', "&quot;")
        icon_html += f'\n            <img src="{icon_src}" class="progression-icon" alt="{item}" data-location="{location_key}">'
    icon_html += "</span>"
    icon_html += "<span class=fr>"
    for item in sorted(unique_receives):
      if not item.startswith(ITEM_NAMES):
        sanitized_name = re.sub(r"[:#?]", "_", re.sub(r"[#?].+$", "", item))
        icon_filename = f"{sanitized_name}.png"
        icon_src = os.path.join(PROGRESSION_ICON_PATH, icon_filename).replace("\\", "/")
        # match the exact key format used when AP_LOCATION_IDS was generated:
        # f"{north}_{east} - {itemInfo.split('#')[0]}"
        base_item_name = item.split("#")[0]
        location_key = f"{room_key} - {base_item_name}".replace('"', "&quot;")
        icon_html += f'\n            <img src="{icon_src}" class="progression-icon" alt="{item}" data-location="{location_key}">'
    icon_html += "</span>"
    icon_html += "</span>"
    overlay_content = "\n".join(squares_html)
    wrapper_tag = f"""        <div class="tile-wrapper" data-room="{room_key}" style="left: {pixel_left:.1f}px; top: {pixel_top:.1f}px; background-image: url('{placeholder_img_path}');" data-info="{info_json_str}">{icon_html}
            <div class="overlay-layer" style="z-index: 6; position: absolute; top:0; left:0; width:100%; height:100%;">
{overlay_content}
            </div>
        </div>"""
    html_elements.append(wrapper_tag)

    canvas_tiles_data.append(
      {
        "roomKey": room_key,
        "map": highres_img_path,
        "map_80": f"/map_80/{filename}",
        "map_30": f"/map_30/{filename}",
        "map_20": f"/map_20/{filename}",
        "map_07": f"/map_07/{filename}",
      }
    )

  total_svg_width = 40 + (cols * TILE_WIDTH)
  total_svg_height = 40 + (rows * TILE_HEIGHT)

  container_style = f'id="grid" style="width: {total_svg_width}px; height: {total_svg_height}px;"'
  dynamic_html_start = html_start.replace('id="grid"', container_style)

  script_payload = f"""
    <script>
        const ROUTES_DATA = {json.dumps(js_routes_db, indent=2)};
        const EXITS_DATA = {json.dumps(js_exits_db, indent=2)};
        const TILES_DATA = {json.dumps(canvas_tiles_data)};
    </script>
    """

  with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(dynamic_html_start)
    f.write("\n".join(html_elements))
    f.write(script_payload)
    f.write("\n" + html_end)

  with open("./MathQuest/play.base.html", "r", encoding="utf-8") as ff:
    with open("./MathQuest/play.html", "w", encoding="utf-8") as f:
      oldData = ff.read().split('<map id="map"></map>')
      f.write(oldData[0])
      f.write('<map id="map">')
      f.write(dynamic_html_start)
      f.write("\n".join(html_elements))
      f.write(script_payload)
      f.write("\n" + html_end)
      f.write("</map>")
      f.write(oldData[1])


def snapToGrid(x, y):
  block_width = float(ROOM_INTERNAL_WIDTH) / BLOCKS_X
  block_height = float(ROOM_INTERNAL_HEIGHT) / BLOCKS_Y
  snapped_x = round(float(x) / block_width) * block_width
  snapped_y = round(float(y) / block_height) * block_height
  return snapped_x, snapped_y


if __name__ == "__main__":
  main()
