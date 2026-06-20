import os
from http.server import HTTPServer, CGIHTTPRequestHandler

PORT = 1533
DIRECTORY = "."

class CachedCGIHTTPRequestHandler(CGIHTTPRequestHandler):
  def __init__(self, *args, **kwargs):
    # Set the root serving directory matching the -d flag
    super().__init__(*args, directory=DIRECTORY, **kwargs)

  def end_headers(self):
    # Check if the requested path points to an item inside the map folder
    normalized_path = self.translate_path(self.path)
    relative_path = os.path.relpath(normalized_path, os.getcwd())

    # If it's a JPG inside the map directory, apply an aggressive max-age (1 year)
    if relative_path.startswith("map") and relative_path.lower().endswith(".jpg"):
      self.send_header("Cache-Control", "public, max-age=31536000, immutable")

    super().end_headers()

def run():
  server_address = ("", PORT)
  # Ensure CGI scripts can run by setting up the base handler paths
  handler = CachedCGIHTTPRequestHandler

  print(f"[*] Starting custom CGI server with map/ caching on port {PORT}...")
  print(f"[*] Serving directory: {os.path.abspath(DIRECTORY)}")

  httpd = HTTPServer(server_address, handler)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    print("\n[-] Shutting down server.")
    httpd.server_close()

if __name__ == "__main__":
  run()