import os
import re
import json
import time
import subprocess

GEOMETRY_JSON_PATH = "./room_geometry.json"
GEN_GRID_SCRIPT = "map/genGrid.py" # Adjusted to point to the current directory matching your setup

def mark_room_complete(east, north):
    if not os.path.exists(GEOMETRY_JSON_PATH):
        print(f"[-] Error: '{GEOMETRY_JSON_PATH}' not found.")
        return False

    try:
        with open(GEOMETRY_JSON_PATH, "r", encoding="utf-8") as f:
            rooms_list = json.load(f)

        modified = False
        for room in rooms_list:
            # Safely match coordinates regardless of string or numeric types
            if int(float(room.get("north", -1))) == north and int(float(room.get("east", -1))) == east:
                # Only update and trigger regeneration if it wasn't already marked complete
                if not room.get("complete"):
                    room["complete"] = True
                    modified = True
                    print(f"[+] Marking Room (East: {east}, North: {north}) as complete.")
                break

        if modified:
            # Write back the modified array structured clearly with indents
            with open(GEOMETRY_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump(rooms_list, f, indent=2, ensure_ascii=False)
            return True

    except Exception as err:
        print(f"[-] Failed to edit geometry file: {err}")

    return False

def run_grid_generator():
    print("[*] Running grid generator...")
    try:
        # Executes the script in its folder context
        result = subprocess.run(["python", GEN_GRID_SCRIPT], capture_output=True, text=True)
        if result.returncode == 0:
            print("[+] Grid successfully regenerated!")
        else:
            print(f"[-] genGrid.py failed: {result.stderr}")
    except Exception as err:
        print(f"[-] Failed to run {GEN_GRID_SCRIPT}: {err}")

def start_clipboard_monitor():
    # Attempt to import pyperclip dynamically
    try:
        import pyperclip
    except ImportError:
        print("[-] Missing dependency: Please run 'pip install pyperclip' to support clipboard tracking.")
        return

    print("[*] Clipboard background listener active. Click tiles to mark them complete...")

    # Store initial state to avoid treating existing clipboard data as a new click
    last_paste = pyperclip.paste()

    while True:
        try:
            current_paste = pyperclip.paste()
            if current_paste != last_paste:
                last_paste = current_paste

                # Regex patterns to parse standard "X,Y" or "Copied: X,Y" formats
                match = re.search(r"(\d+)[,\-](\d+)", current_paste)
                if match:
                    east = int(match.group(1))
                    north = int(match.group(2))

                    # Attempt to update the file registry
                    if mark_room_complete(east, north):
                        run_grid_generator()

        except Exception as e:
            print(f"[-] Loop monitoring error: {e}")

        time.sleep(0.5) # Interval poll checking to prevent high CPU utilization

if __name__ == "__main__":
    start_clipboard_monitor()