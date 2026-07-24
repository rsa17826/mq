#!/usr/bin/env bash

# Define scales
declare -A SCALES=(
  ["map_80"]="80%"
  ["map_30"]="30%"
  ["map_20"]="20%"
  ["map_07"]="7%"
)

# Detect available CPU cores
NPROC=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)

# 1. Define the function FIRST
process_image() {
  local f="$1"
  local dir="$2"
  local scale="$3"
  local filename
  filename=$(basename "$f" .jpg)

  magick "$f" -resize "$scale" -quality 80 "$dir/${filename}.webp"
}

# 2. Export the function AFTER defining it
export -f process_image

echo "[+] Starting parallel processing using $NPROC CPU cores..."

for dir in "${!SCALES[@]}"; do
  scale="${SCALES[$dir]}"
  rm -rf "$dir" && mkdir -p "$dir"

  echo "[+] Processing $dir ($scale)..."

  # 3. Cleaned xargs command (removed redundant -n 1)
  find ./map -maxdepth 1 -name "*.jpg" -print0 |
    xargs -0 -P "$NPROC" -I {} bash -c 'process_image "$@"' _ {} "$dir" "$scale"
done

echo "[+] Done scaling and converting to WebP!"
