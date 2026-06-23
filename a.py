import re
import json
import sys

# Regex patterns
TARGET_PAT = re.compile(r"manager\.quest\[manager\.(\w+)\]\s*= ")
NORTH_PAT = re.compile(r"manager\.north\s*==\s*(\d+)")
EAST_PAT = re.compile(r"manager\.east\s*==\s*(\d+)")

def parse_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    results = []

    for i, line in enumerate(lines):
        if s:=TARGET_PAT.search(line):
            line_num = i + 1

            closest_north_idx = None
            closest_east_idx = None
            north_val = None
            east_val = None

            # 1. Scan backwards up to 50 lines to find the closest north and east
            for j in range(i - 1, max(-1, i - 50), -1):
                check_line = lines[j]

                if closest_north_idx is None:
                    n_match = NORTH_PAT.search(check_line)
                    if n_match:
                        closest_north_idx = j
                        north_val = int(n_match.group(1))

                if closest_east_idx is None:
                    e_match = EAST_PAT.search(check_line)
                    if e_match:
                        closest_east_idx = j
                        east_val = int(e_match.group(1))

                # Stop scanning if we found both a north and an east
                if closest_north_idx is not None and closest_east_idx is not None:
                    break

            # If we didn't find either coordinate, skip this target entirely
            if closest_north_idx is None and closest_east_idx is None:
                continue

            # 2. Warning Logic: Check if there are MORE than these 2 coordinate lines nearby
            # Determine the boundaries of our found pair block
            found_indices = [idx for idx in [closest_north_idx, closest_east_idx] if idx is not None]
            min_idx = min(found_indices)
            max_idx = max(found_indices)

            # Check a small buffer window around our found block (5 lines above and below)
            search_start = max(0, min_idx - 5)
            search_end = min(len(lines), max_idx + 6)

            total_coordinates_found = 0
            for scan_idx in range(search_start, search_end):
                scan_line = lines[scan_idx]
                if NORTH_PAT.search(scan_line) or EAST_PAT.search(scan_line):
                    total_coordinates_found += 1

            # If we found more than the 2 expected coordinate lines in this block, flag it
            if total_coordinates_found > len(found_indices):
                print(f"[WARNING] More than 2 coordinate checks found near line {line_num}. Verify block layout.", file=sys.stderr)

            # 3. Build JSON data
            quest_data = {
                "room": {
                    "north": north_val,
                    "east": east_val
                },
                "requires": [["quest:"+str(s[1])+".2"]],
                "receive": ["quest:"+str(s[1])+".3"]
            }
            results.append(quest_data)

    print(json.dumps(results, indent=6))

if __name__ == "__main__":
    parse_file("MathQuest/MathQuest.js")