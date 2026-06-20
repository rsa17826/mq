import os
import re

IMAGE_FOLDER = "map"
OUTPUT_FILE = "index.html"

html_start = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dynamic Image Grid Map</title>
  <style>
    body {
      margin: 0;
      background-color: #222;
    }
    .grid-container {
      display: grid;
      grid-auto-columns: max-content;
      grid-auto-rows: max-content;
      gap: 0px;
      padding: 20px;
    }
    .grid-item {
      display: block;
      width: auto;
      height: auto;
    }
  </style>
</head>
<body>
  <div class="grid-container">
"""

html_end = """    </div>
</body>
</html>
"""


def generate_html():
  if not os.path.exists(IMAGE_FOLDER):
    print(f"Error: '{IMAGE_FOLDER}' folder not found.")
    return

  files = os.listdir(IMAGE_FOLDER)
  parsed_tiles = []
  max_row = 0

  # First pass: Gather coordinates and find the maximum row index
  for filename in files:
    match = re.match(r"(\d+)[,\-](\d+)", filename)
    if match:
      col = int(match.group(1))
      row = int(match.group(2))
      parsed_tiles.append((col, row, filename))
      if row > max_row:
        max_row = row

  img_tags = []

  # Second pass: Generate tags with inverted row logic
  for col, row, filename in parsed_tiles:
    grid_col = col + 1

    # INVERSION LOGIC: Subtract current row from max_row to flip it right-side up
    grid_row = (max_row - row) + 1

    img_path = f"{IMAGE_FOLDER}/{filename}"
    tag = f'        <img src="{img_path}" class="grid-item" style="grid-column: {grid_col}; grid-row: {grid_row};" alt="Tile {col},{row}">'
    img_tags.append(tag)

  with open(OUTPUT_FILE, "w") as f:
    f.write(html_start)
    f.write("\n".join(img_tags))
    f.write("\n" + html_end)

  print(f"Success! Generated flipped {OUTPUT_FILE} with {len(img_tags)} image tiles.")


if __name__ == "__main__":
  generate_html()
