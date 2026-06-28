import re
import sys

def find_duplicates(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return

    # Regex block to cleanly match each object block inside the list literal
    # It catches "room": { "north": X, "east": Y } and the "receive": [...] array
    pattern = r'\{\s*"room"\s*:\s*\{\s*"north"\s*:\s*([0-9.\-]+)\s*,\s*"east"\s*:\s*([0-9.\-]+)\s*\}[^}]+?"receive"\s*:\s*(\[[^\]]*?\])'
    matches = re.findall(pattern, content, re.DOTALL)

    seen = {}
    duplicates = []

    for north_str, east_str, receive_raw in matches:
        # Canonicalize numbers
        north = int(north_str) if '.' not in north_str else float(north_str)
        east = int(east_str) if '.' not in east_str else float(east_str)

        # Parse the raw receive list (clean up spaces, quotes, and newlines)
        items = re.findall(r'"([^"]+)"', receive_raw)
        receive_tuple = tuple(sorted(items)) # Sort to match regardless of item order if any

        key = (north, east, receive_tuple)

        if key in seen:
            if key not in [d[0] for d in duplicates]:
                # Format exactly as it's found or represented
                # Convert items to JSON/Python double quote list style string format
                receive_str = "[" + ", ".join(f'"{i}"' for i in items) + "]"
                duplicates.append((key, north, east, receive_str))
        else:
            seen[key] = True

    # Output matching template format: \n{0}\{"north": %s, "east": %s\},[^\}]+?%s
    format_template = r"\n{{0}}\{{\"north\": {0}, \"east\": {1}\}},[^\}}]+?{2}"

    for _, north, east, receive_str in duplicates:
        print(format_template.format(north, east, receive_str.replace("[",'').replace("]",'')).replace("\\\"", "\""))

if __name__ == "__main__":
    find_duplicates('_progression.py')