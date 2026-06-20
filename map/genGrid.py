import os
import re

# Path to the folder containing your cropped images
IMAGE_FOLDER = "map"
OUTPUT_FILE = "index.html"

# HTML Template
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
      gap: 0px; /* Set to 0 for a seamless map */
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
  img_tags = []

  # Check if folder exists
  if not os.path.exists(IMAGE_FOLDER):
    print(f"Error: '{IMAGE_FOLDER}' folder not found.")
    return

  # Scan the folder for files matching the coordinate pattern (e.g., 26,14.jpg)
  files = os.listdir(IMAGE_FOLDER)

  for filename in files:
    # Match digits separated by a comma or underscore (handles '26,14.jpg' or '26,14.crop.jpg')
    match = re.match(r"(\d+)[,\-](\d+)", filename)

    if match:
      col = int(match.group(1))
      row = int(match.group(2))

      # NOTE: If your image coordinates start at 0 (e.g. 0,0.jpg),
      # CSS grid lines must start at 1, so we add 1 to the position.
      grid_col = col + 1
      grid_row = row + 1

      # Create the image element with inline grid coordinates
      img_path = f"{IMAGE_FOLDER}/{filename}"
      tag = f'        <img src="{img_path}" class="grid-item" style="grid-column: {grid_col}; grid-row: {grid_row};" alt="Tile {col},{row}">'
      img_tags.append(tag)

  # Write everything to the index.html file
  with open(OUTPUT_FILE, "w") as f:
    f.write(html_start)
    f.write("\n".join(img_tags))
    f.write("\n" + html_end)

  print(f"Success! Generated {OUTPUT_FILE} with {len(img_tags)} image tiles.")


if __name__ == "__main__":
  generate_html()
