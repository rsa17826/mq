import json
import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION ---
PROGRESSION_PATH = "./json/progression.json"
SOURCE_FILE_PATH = "MathQuest/MathQuest.js"

def open_in_codium(file_path, line_number):
    """Launches VSCodium directly focused on the source code line."""
    abs_path = os.path.abspath(file_path)
    target = f"{abs_path}:{line_number}"
    try:
        # Opens file and jumps to the exact line
        subprocess.run(["codium", "--goto", target], check=True)
        print(f"👉 Opened Codium at line {line_number}. Waiting for you to modify and save the file...")
    except FileNotFoundError:
        print("Error: 'codium' command not found in your system's PATH.")

class FileChangeHandler(FileSystemEventHandler):
    """Triggers an internal flag when the watched file is modified/saved."""
    def __init__(self, target_file):
        self.target_file = os.path.abspath(target_file)
        self.modified = False

    def on_modified(self, event):
        if os.path.abspath(event.src_path) == self.target_file:
            self.modified = True

def wait_for_file_save(file_path):
    """Blocks execution until the user edits and saves the file."""
    event_handler = FileChangeHandler(file_path)
    observer = Observer()
    # Watch the directory containing the file
    observer.schedule(event_handler, path=os.path.dirname(os.path.abspath(file_path)) or '.', recursive=False)
    observer.start()

    try:
        while not event_handler.modified:
            time.sleep(0.5)
    finally:
        observer.stop()
        observer.join()
    print("✅ File change detected!")

def main():
    if not os.path.exists(PROGRESSION_PATH):
        print(f"Error: Could not find {PROGRESSION_PATH}")
        return

    # Continuous loop mimicking "do-while" logic
    while True:
        # 1. Reload the progression database fresh each loop
        data=None
        while not data:
          try:
            with open(PROGRESSION_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
          except:
            time.sleep(1)

        locations = data.get("locations", [])

        # 2. Find the first item that has a line number and isn't marked "done"
        target_item = None
        for item in locations:
            if "line" in item and not item.get("processed", False):
                target_item = item
                break

        # If no unprocessed lines are left, exit the script cleanly
        if not target_item:
            print("🎉 All locations with lines have been processed!")
            break

        current_line = target_item["line"]
        print(f"\n📍 Found unprocessed entry for Room [N: {target_item['room']['north']}, E: {target_item['room']['east']}] at Line: {current_line}")

        # 3. Open Codium to the target line suffix
        open_in_codium(SOURCE_FILE_PATH, current_line)

        # 4. Wait for you to inspect code, make your changes, and hit save (Ctrl+S)
        wait_for_file_save("./json/progression.json")

        # 5. Mark this entry as processed inside the JSON schema database
        target_item["processed"] = True

        # Save updates back to disk immediately
        time.sleep(0.1)

if __name__ == "__main__":
    main()