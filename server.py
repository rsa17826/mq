import hashlib
import os
import re
from http.server import CGIHTTPRequestHandler, HTTPServer

from PIL import Image, ImageDraw

PORT = 1533
DIRECTORY = "."


class CachedCGIHTTPRequestHandler(CGIHTTPRequestHandler):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, directory=DIRECTORY, **kwargs)

  def do_GET(self):
    # Split out query parameters to safely check the file extension
    clean_path = self.path.split("?")[0]

    # Reroute any .mp3 request to /empty.mp3
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

    # Remove .\d+ pattern from the filename base
    clean_name = re.sub(r"\.\d+", "", name_part)
    clean_filename = f"{clean_name}{ext}"

    # Generate MD5 hash string
    hash_object = hashlib.md5(clean_filename.encode("utf-8"))
    hex_dig = hash_object.hexdigest()

    # Derive attributes from slices of the hash string
    bg_color = f"#{hex_dig[0:6]}"
    pattern_color = f"#{hex_dig[6:12]}"

    # Use a segment of the hash to pick a pattern style (integer 0 to 3)
    pattern_style = int(hex_dig[12:15], 16) % 4

    # Image setup
    size = (250, 250)
    img = Image.new("RGB", size, color=bg_color)
    draw = ImageDraw.Draw(img)

    # Draw patterns based on the hash value
    if pattern_style == 0:
      # Vertical Stripes
      for x in range(0, 250, 25):
        if (x // 25) % 2 == 0:
          draw.rectangle([(x, 0), (x + 12, 250)], fill=pattern_color)

    elif pattern_style == 1:
      # Checkerboard
      for x in range(0, 250, 50):
        for y in range(0, 250, 50):
          if ((x // 50) + (y // 50)) % 2 == 0:
            draw.rectangle([(x, y), (x + 50, y + 50)], fill=pattern_color)

    elif pattern_style == 2:
      # Concentric Frames
      for i in range(0, 125, 25):
        if (i // 25) % 2 == 1:
          draw.rectangle(
            [(i, i), (250 - i, 250 - i)], outline=pattern_color, width=10
          )

    elif pattern_style == 3:
      # Diagonal Lines
      for offset in range(-250, 250, 30):
        draw.line(
          [(offset, 0), (offset + 250, 250)], fill=pattern_color, width=8
        )

    # Border outline
    draw.rectangle([(0, 0), (249, 249)], outline="black", width=2)

    try:
      pil_format = "PNG" if ext.lower() == ".png" else "JPEG"
      img.save(target_path, pil_format)
      print(
        f"[+] Dynamically generated patterned image: {target_path} (Hashed from: {clean_filename}, Pattern: {pattern_style})"
      )
    except Exception as e:
      print(f"[-] Failed to generate image: {e}")

  def end_headers(self):
    normalized_path = self.translate_path(self.path)
    relative_path = os.path.relpath(normalized_path, os.getcwd())

    if (
      relative_path.startswith("map") or relative_path.startswith("mapimgs")
    ) or relative_path.lower().split("?")[0].endswith(
      (".jpg", ".jpeg", ".png", ".mp3", ".ogg", ".eot", ".svg", ".ttf")
    ):
      self.send_header("Cache-Control", "public, max-age=31536000, immutable")

    super().end_headers()


def run():
  server_address = ("", PORT)
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
