import os
import re
import json
import time
import subprocess

GEOMETRY_JSON_PATH = "./room_geometry.json"
GEN_GRID_SCRIPT = "map/genGrid.py"

def find_line_number_in_file(east, north):
    """Scans the geometry file sequentially to find the line number of the specific block matching both coordinates."""
    if not os.path.exists(GEOMETRY_JSON_PATH):
        return None

    pattern_n = f'"north": {north}'
    pattern_e = f'"east": {east}'

    current_block_start_line = None
    has_north = False
    has_east = False

    with open(GEOMETRY_JSON_PATH, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            # Track when a new JSON object entry block begins
            if "{" in line:
                current_block_start_line = line_num
                has_north = False
                has_east = False

            # Check for coordinates within the active block
            if pattern_n in line:
                has_north = True
            if pattern_e in line:
                has_east = True

            # Once BOTH conditions match within the same object wrapper, return the line number
            if has_north and has_east:
                return current_block_start_line

    return None

def mark_room_complete(east, north):
    if not os.path.exists(GEOMETRY_JSON_PATH):
        print(f"[-] Error: '{GEOMETRY_JSON_PATH}' not found.")
        return False

    try:
        with open(GEOMETRY_JSON_PATH, "r", encoding="utf-8") as f:
            rooms_list = json.load(f)

        modified = False
        for room in rooms_list:
            if int(float(room.get("north", -1))) == north and int(float(room.get("east", -1))) == east:
                if not room.get("complete"):
                    room["complete"] = True
                    modified = True
                    print(f"[+] Marking Room (East: {east}, North: {north}) as complete.")
                break

        if modified:
            with open(GEOMETRY_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump(rooms_list, f, indent=2, ensure_ascii=False)
            return True

    except Exception as err:
        print(f"[-] Failed to edit geometry file: {err}")

    return False

def open_in_codium(line_number):
    """Spawns VSCodium focused exactly on the target line entry."""
    if line_number is None:
        return
    try:
        target = f"{GEOMETRY_JSON_PATH}:{line_number}"
        print(f"[*] Opening Codium at line {line_number}...")
        subprocess.run(["codium", "--goto", target], check=True)
    except Exception as err:
        print(f"[-] Failed to open VSCodium: {err}. Make sure 'codium' is in your PATH.")

def run_grid_generator():
    print("[*] Running grid generator...")
    try:
        result = subprocess.run(["python", GEN_GRID_SCRIPT], capture_output=True, text=True)
        if result.returncode == 0:
            print("[+] Grid successfully regenerated!")
        else:
            print(f"[-] {GEN_GRID_SCRIPT} failed: {result.stderr}")
    except Exception as err:
        print(f"[-] Failed to run {GEN_GRID_SCRIPT}: {err}")

def start_clipboard_monitor():
    try:
        import pyperclip
    except ImportError:
        print("[-] Missing dependency: Please run 'pip install pyperclip' to support clipboard tracking.")
        return

    print("[*] Clipboard background listener active with block-precise Codium line lookup...")
    last_paste = pyperclip.paste()

    while True:
        try:
            current_paste = pyperclip.paste()
            if current_paste != last_paste:
                last_paste = current_paste

                match = re.search(r"(\d+)[,\-](\d+)", current_paste)
                if match:
                    east = int(match.group(1))
                    north = int(match.group(2))

                    # 1. Update complete: True field inside room_geometry.json
                    file_was_modified = mark_room_complete(east, north)

                    # 2. Extract block-validated target line position
                    line_no = find_line_number_in_file(east, north)

                    # 3. Focus Codium context
                    if line_no:
                        open_in_codium(line_no)
                    else:
                        print(f"[-] Coordinate set {east},{north} not found in structured layout.")

                    # 4. Regenerate grid
                    if file_was_modified:
                        run_grid_generator()

        except Exception as e:
            print(f"[-] Loop monitoring error: {e}")

        time.sleep(0.5)

if __name__ == "__main__":
    運転 = start_clipboard_monitor()