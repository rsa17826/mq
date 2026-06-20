import json
import re
import sys

try:
    import pyperclip
except ImportError:
    print("[-] Dependency missing: 'pyperclip' is required to copy directly to your clipboard.")
    print("[*] Please run: pip install pyperclip")
    sys.exit(1)


def generate_edge_data(input_string):
    # Parse input like: 8,24,north,south,east,west
    parts = [p.strip().lower() for p in input_string.split(",") if p.strip()]

    if len(parts) < 3:
        print("[-] Invalid format. Expected format: north,east,dir1,dir2...")
        return None

    try:
        origin_east = int(parts[1])
        origin_north = int(parts[0])
    except ValueError:
        print("[-] Error: 'east' and 'north' positions must be valid integers.")
        return None

    requested_directions = parts[2:]
    valid_directions = 'wasd'

    # Positional changes map for standard grid direction mechanics
    direction_offsets = {
        "w": {"north": 1, "east": 0, "dest_y": 510},
        "s": {"north": -1, "east": 0, "dest_y": 0},
        "d": {"north": 0, "east": 1, "dest_x": 0},
        "a": {"north": 0, "east": -1, "dest_x": 624},
    }

    payload_array = []

    for direction in requested_directions:
        if direction not in valid_directions:
            print(f"[-] Warning: '{direction}' is not a valid wall direction. Skipping.")
            continue

        offset = direction_offsets[direction]

        # Calculate destination coordinates based on direction offset
        dest_north = origin_north + offset["north"]
        dest_east = origin_east + offset["east"]

        edge_object = {
            "id": f"edge:{({'w':'north','a':'west','s':'south','d':'east'}[direction])}:{float(origin_north)}_{float(origin_east)}",
            "mechanism": "edge",
            "direction": {'w':'north','a':'west','s':'south','d':'east'}[direction],
            "origin": {"north": origin_north, "east": origin_east},
            "dest": {"north": dest_north, "east": dest_east},
            "dest_x": offset.get("dest_x", None),
            "dest_y": offset.get("dest_y", None),
            "gated": False,
            "gate": None,
            "one_way": False,
            "dest_room_exists_in_census": True,
            "notes": None,
        }

        payload_array.append(edge_object)

    return payload_array


def main():
    print("=== Bulk Edge Data Generator ===")
    print("Enter string (e.g., 8,24,north,south,east,west):")

    try:
        user_input = input("> ")
        if not user_input.strip():
            return

        result_data = generate_edge_data(user_input)

        if result_data:
            # Format cleanly into JSON syntax matching your requirements
            json_output = json.dumps(result_data, indent=2)[1:-2]

            # Write to the clipboard
            pyperclip.copy(json_output)

            print("\n[+] Success! The following JSON was copied to your clipboard:\n")
            print(json_output)

    except KeyboardInterrupt:
        print("\n[-] Exiting.")


if __name__ == "__main__":
    main()