import re
import json

def parse_mathquest_with_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    results = {}

    # Helper regexes
    coord_pattern = r'manager\.(north|east)\s*==\s*(\d+)\s*&&\s*manager\.(north|east)\s*==\s*(\d+)'
    single_north = r'manager\.north\s*==\s*(\d+)'
    single_east = r'manager\.east\s*==\s*(\d+)'

    quest_patterns = [
        (r'manager\.quest\[manager\.(\w+)\]\s*(==|>=|<=|=)\s*(\d+)', True),
        (r'manager\.quest\[manager\.(\w+)\]\s*(\+\+|--)', False)
    ]

    # Persistent state tracking for contexts across lines
    current_north = None
    current_east = None

    for idx, line in enumerate(lines, start=1):
        # 1. Update coordinate tracking if we find direct matches on this line
        coord_match = re.search(coord_pattern, line)
        if coord_match:
            g = coord_match.groups()
            if g[0] == 'north':
                current_north, current_east = int(g[1]), int(g[3])
            else:
                current_east, current_north = int(g[1]), int(g[3])
        else:
            # Check individual components
            n_m = re.search(single_north, line)
            e_m = re.search(single_east, line)
            if n_m: current_north = int(n_m.group(1))
            if e_m: current_east = int(e_m.group(1))

        # If we don't have valid context coordinates yet, skip quest matching
        if current_north is None or current_east is None:
            continue

        coord_key = (current_north, current_east)

        # 2. Extract quest comparisons/assignments
        for pattern, has_val in quest_patterns:
            for q_match in re.finditer(pattern, line):
                groups = q_match.groups()
                quest_name = groups[0]
                op = groups[1] if has_val else groups[1]
                val = groups[2] if has_val else op # For ++ or --, keep operator as indicator

                if coord_key not in results:
                    results[coord_key] = {"comparisons": [], "assignments": []}

                entry = {
                    "name": quest_name,
                    "value": val,
                    "line": idx
                }

                # Categorize based on assignment vs comparison operator
                if op in ('==', '>=', '<='):
                    results[coord_key]["comparisons"].append(entry)
                elif op in ('=', '++', '--'):
                    results[coord_key]["assignments"].append(entry)

    # Transform output structure into sorted clean JSON lists
    json_output = []
    for (north, east), data in sorted(results.items()):
        if not data["comparisons"] and not data["assignments"]:
            continue

        json_output.append({
            "north": north,
            "east": east,
            "comparisons": data["comparisons"],
            "assignments": data["assignments"]
        })

    return json_output

if __name__ == '__main__':
    extracted_data = parse_mathquest_with_lines('MathQuest/MathQuest.js')
    print(json.dumps(extracted_data, indent=2))