#!/usr/bin/env bash

# Define directories
declare -A SCALES
SCALES=(
  ["map_80"]="80%"
  ["map_30"]="30%"
  ["map_20"]="20%"
  ["map_07"]="7%"
)
. progress-bar
# Recreate folders and downsize images
i=0
for dir in "${!SCALES[@]}"; do
  echo "[+] Creating and sizing $dir to ${SCALES[$dir]}..."
  rm -rf "$dir"
  mkdir -p "$dir"
  files=(./map/*.jpg)
  len=$((${#files[@]} * 4))
  for f in "${files[@]}"; do
    if [ -f "$f" ]; then
      ((i++))
      # Extract filename without the extension
      filename=$(basename "$f" .jpg)
      progress-bar "$i" "$len"

      # Resize and convert to .webp with quality 80
      magick "$f" -resize "${SCALES[$dir]}" -quality 80 "$dir/${filename}.webp"
    fi
  done
done
# sleep 10
progress-bar "$len" "$len"
echo "[+] Done scaling and converting to WebP!"
