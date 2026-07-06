#!/usr/bin/env bash

# Define directories
declare -A SCALES
SCALES=(
  ["map_80"]="80%"
  ["map_30"]="30%"
  ["map_20"]="20%"
  ["map_07"]="7%"
)

# Recreate folders and downsize images
for dir in "${!SCALES[@]}"; do
  echo "[+] Creating and sizing $dir to ${SCALES[$dir]}..."
  rm -rf "$dir"
  mkdir -p "$dir"

  for f in map/*.jpg; do
    if [ -f "$f" ]; then
      magick "$f" -resize "${SCALES[$dir]}" "$dir/$(basename "$f")"
    fi
  done
done

echo "[+] Done scaling!"
