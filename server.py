import hashlib
import os
import re
from http.server import CGIHTTPRequestHandler, HTTPServer

from PIL import Image, ImageDraw
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import main

PORT = 1533
DIRECTORY = "."
WATCH_FILE = os.path.normpath("MathQuest/play.base.html")


class CachedCGIHTTPRequestHandler(CGIHTTPRequestHandler):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, directory=DIRECTORY, **kwargs)

  def do_GET(self):
    clean_path = self.path.split("?")[0]

    if clean_path.lower().endswith(".mp3"):
      self.path = "/empty.mp3"

    normalized_path = self.translate_path(self.path)
    relative_path = os.path.relpath(normalized_path, os.getcwd())

    is_image = relative_path.lower().endswith((".jpg", ".jpeg", ".png"))

    if relative_path.startswith("mapimgs") and is_image:
      if not os.path.exists(normalized_path):
        self.generate_placeholder_image(normalized_path)

    super().do_GET()

  def address_string(self):
    return self.client_address[0]

  def generate_placeholder_image(self, target_path):
    os.makedirs(os.path.dirname(target_path), exist_ok=True)

    filename = os.path.basename(target_path)
    name_part, ext = os.path.splitext(filename)

    clean_name = re.sub(r"\.\d+", "", name_part)
    clean_filename = f"{clean_name}{ext}"

    hash_object = hashlib.md5(clean_filename.encode("utf-8"))
    hex_dig = hash_object.hexdigest()

    bg_color = f"#{hex_dig[0:6]}"
    pattern_color = f"#{hex_dig[6:12]}"

    pattern_style = int(hex_dig[12:15], 16) % 4

    size = (250, 250)
    img = Image.new("RGB", size, color=bg_color)
    draw = ImageDraw.Draw(img)

    if pattern_style == 0:
      for x in range(0, 250, 25):
        if (x // 25) % 2 == 0:
          draw.rectangle([(x, 0), (x + 12, 250)], fill=pattern_color)

    elif pattern_style == 1:
      for x in range(0, 250, 50):
        for y in range(0, 250, 50):
          if ((x // 50) + (y // 50)) % 2 == 0:
            draw.rectangle([(x, y), (x + 50, y + 50)], fill=pattern_color)

    elif pattern_style == 2:
      for i in range(0, 125, 25):
        if (i // 25) % 2 == 1:
          draw.rectangle([(i, i), (250 - i, 250 - i)], outline=pattern_color, width=10)

    elif pattern_style == 3:
      for offset in range(-250, 250, 30):
        draw.line([(offset, 0), (offset + 250, 250)], fill=pattern_color, width=8)

    draw.rectangle([(0, 0), (249, 249)], outline="black", width=2)

    try:
      pil_format = "PNG" if ext.lower() == ".png" else "JPEG"
      img.save(target_path, pil_format)
      print(f"[+] Dynamically generated patterned image: {target_path} (Hashed from: {clean_filename}, Pattern: {pattern_style})")
    except Exception as e:
      print(f"[-] Failed to generate image: {e}")

  def end_headers(self):
    normalized_path = self.translate_path(self.path)
    relative_path = os.path.relpath(normalized_path, os.getcwd())

    if (relative_path.startswith("map") or relative_path.startswith("mapimgs")) or relative_path.lower().split("?")[0].endswith((".jpg", ".jpeg", ".png", ".mp3", ".ogg", ".eot", ".svg", ".ttf")):
      self.send_header("Cache-Control", "public, max-age=31536000, immutable")

    super().end_headers()


# --- File Watcher Logic ---
class HTMLChangeHandler(FileSystemEventHandler):
  """Listens for modifications specifically on the target HTML file."""

  def on_modified(self, event):
    # Normalize the event path to match WATCH_FILE style
    event_path = os.path.normpath(os.path.relpath(event.src_path, os.getcwd()))

    if event_path == WATCH_FILE:
      print(f"\n[!] Change detected in {WATCH_FILE}!")
      # Add whatever action you want to run here.
      # Example: You could clear server caches or flag a state change.
      self.execute_on_change()

  def execute_on_change(self):

    main.main()


def start_file_watcher():
  """Initializes and runs the watchdog observer in a background thread."""
  watch_dir = os.path.dirname(WATCH_FILE) or "."

  # Ensure the directory exists before watching it
  if not os.path.exists(watch_dir):
    os.makedirs(watch_dir, exist_ok=True)

  event_handler = HTMLChangeHandler()
  observer = Observer()
  observer.schedule(event_handler, path=watch_dir, recursive=False)
  observer.start()
  print(f"[*] File watcher active: Monitoring updates to '{WATCH_FILE}'")
  return observer


def run():
  server_address = ("", PORT)
  handler = CachedCGIHTTPRequestHandler

  print(f"[*] Starting custom CGI server with map/ caching on port {PORT}...")
  print(f"[*] Serving directory: {os.path.abspath(DIRECTORY)}")

  # Start the watchdog observer thread
  watcher = start_file_watcher()

  httpd = HTTPServer(server_address, handler)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    print("\n[-] Shutting down server.")
    watcher.stop()
    httpd.server_close()

  watcher.join()


if __name__ == "__main__":
  run()
