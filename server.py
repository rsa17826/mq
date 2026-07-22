import hashlib
import os
import queue
import re
import subprocess
import threading
import urllib.parse
from http.server import CGIHTTPRequestHandler, ThreadingHTTPServer

from PIL import Image, ImageDraw
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import main

main.main()

PORT = 1533
DIRECTORY = "."
WATCH_FILE = os.path.normpath("MathQuest/play.base.html")


class ProcessManager:
  """Manages a single running process, broadcasts output to all connected

  clients, and automatically kills the process after 10 idle seconds.
  """

  def __init__(self):
    self.lock = threading.Lock()
    self.process = None
    self.subscribers = []
    self.idle_timer = None

  def subscribe(self, cmd):
    with self.lock:
      # Cancel active idle timer if a client connects/reconnects
      if self.idle_timer:
        self.idle_timer.cancel()
        self.idle_timer = None
        print("[*] Client connected. Idle countdown cancelled.")

      # Create dedicated output queue for this HTTP handler thread
      q = queue.Queue()
      self.subscribers.append(q)

      # Start process if it's not already running
      if self.process is None or self.process.poll() is not None:
        print(f"[*] Starting shared process: {' '.join(cmd)}")
        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, cwd=os.path.dirname(cmd[0]))
        # Start background thread to read process stdout
        threading.Thread(target=self._reader_loop, daemon=True).start()

      return q


  def unsubscribe(self, q):
    with self.lock:
      if q in self.subscribers:
        self.subscribers.remove(q)

      # Start 10s countdown if no active clients remain
      if len(self.subscribers) == 0 and self.process and self.process.poll() is None:
        print("[!] No active connections. Starting 10s idle timer...")
        self.idle_timer = threading.Timer(10.0, self._stop_process)
        self.idle_timer.start()



  def _reader_loop(self):
    """Continuously reads stdout and pushes lines to all connected subscriber queues."""
    for line in iter(self.process.stdout.readline, ""):
      if not line:
        break

      with self.lock:
        for q in list(self.subscribers):
          q.put(line)



    self.process.wait()
    # Notify remaining subscribers that the process has finished
    with self.lock:
      for q in list(self.subscribers):
        q.put(None)



  def _stop_process(self):
    """Kills process when 10 seconds elapse with zero active connections."""
    with self.lock:
      if self.process and self.process.poll() is None:
        print("[!] 10s idle timeout reached. Stopping process...")
        self.process.terminate()
        try:
          self.process.wait(timeout=2)

        except subprocess.TimeoutExpired:
          self.process.kill()


      self.process = None



# Global process manager instance
process_manager = ProcessManager()


class CachedCGIHTTPRequestHandler(CGIHTTPRequestHandler):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, directory=DIRECTORY, **kwargs)

  def do_GET(self):
    parsed_url = urllib.parse.urlparse(self.path)
    clean_path = parsed_url.path

    if clean_path == "/run":
      self.handle_run_script(parsed_url.query)
      return

    if clean_path.lower().endswith(".mp3"):
      self.path = "/empty.mp3"

    normalized_path = self.translate_path(self.path)
    relative_path = os.path.relpath(normalized_path, os.getcwd())

    is_image = relative_path.lower().endswith((".jpg", ".jpeg", ".png"))

    if relative_path.startswith("mapimgs") and is_image:
      if not os.path.exists(normalized_path):
        self.generate_placeholder_image(normalized_path)


    super().do_GET()

  def handle_run_script(self, query_string):
    query_params = urllib.parse.parse_qs(query_string)
    arg1 = query_params.get("arg", [None])[0]

    if not arg1 and query_string:
      arg1 = urllib.parse.unquote(query_string)

    try:
      with open("./apWorldPath", "r") as f:
        base_path = f.read().strip()


    except Exception as e:
      self.send_error(500, f"Failed to read ./apWorldPath file: {e}")
      return

    executable_path = os.path.join(base_path, "start")

    if not os.path.exists(executable_path):
      self.send_error(404, f"Executable not found at: {executable_path}")
      return

    cmd = [executable_path]
    if arg1 is not None:
      arg1 = arg1.split("=", 1)
      arg1 = arg1[1] if len(arg1) > 1 else None

    print("[" + arg1 + "]", "arg1", not not arg1)
    if arg1:
      cmd.append(arg1)

    # Set response headers
    self.send_response(200)
    self.send_header("Content-Type", "text/plain; charset=utf-8")
    self.send_header("Cache-Control", "no-cache")
    self.send_header("X-Content-Type-Options", "nosniff")
    self.end_headers()

    # Subscribe connection to shared process output
    sub_queue = process_manager.subscribe(cmd)

    try:
      while True:
        line = sub_queue.get()
        if line is None: # Process ended
          break

        self.wfile.write(line.encode("utf-8"))
        self.wfile.flush()


    except (BrokenPipeError, ConnectionResetError, OSError):
      # Client disconnected (browser tab closed, network dropped, etc.)
      pass

    finally:
      process_manager.unsubscribe(sub_queue)


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

    if (relative_path.startswith("map") or relative_path.startswith("mapimgs")) or relative_path.lower().split("?")[0].endswith(
      (
        ".jpg",
        ".jpeg",
        ".png",
        ".mp3",
        ".ogg",
        ".eot",
        ".svg",
        ".ttf",
      )
    ):
      self.send_header("Cache-Control", "public, max-age=31536000, immutable")
    elif relative_path.lower().endswith(".js"):
      self.send_header("Cache-Control", "no-store, must-revalidate")

    super().end_headers()


# --- File Watcher Logic ---
class HTMLChangeHandler(FileSystemEventHandler):
  def on_modified(self, event):
    event_path = os.path.normpath(os.path.relpath(event.src_path, os.getcwd()))
    if event_path == WATCH_FILE:
      print(f"\n[!] Change detected in {WATCH_FILE}!")
      self.execute_on_change()


  def execute_on_change(self):
    main.main()


def start_file_watcher():
  watch_dir = os.path.dirname(WATCH_FILE) or "."
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
  # Switched to ThreadingHTTPServer for concurrent HTTP request handling
  handler = CachedCGIHTTPRequestHandler

  print(f"[*] Starting multithreaded CGI server with map/ caching on port {PORT}...")
  print(f"[*] Serving directory: {os.path.abspath(DIRECTORY)}")

  watcher = start_file_watcher()

  httpd = ThreadingHTTPServer(server_address, handler)
  try:
    httpd.serve_forever()

  except KeyboardInterrupt:
    print("\n[-] Shutting down server.")
    watcher.stop()
    httpd.server_close()

  watcher.join()


if __name__ == "__main__":
  run()
