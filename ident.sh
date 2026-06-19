#!/usr/bin/env bash

while true; do
  grep -oP "(?<![\w_-])_+(\w[\w+])(?=[^\w_-])" ./MathQuest/MathQuest.js | uniq | sort >a
  # Read user input into the variable 'v'
  read -p "Enter identifier: " v

  # If the input is empty, skip to the next iteration
  [[ -z "$v" ]] && continue

  # Loop as long as the exact word 'v' is found in the file
  while grep -Pq "(?<!\w)$v(?!\w)" ./MathQuest/MathQuest.js; do
    # Prepend an underscore if a match is found
    v="_$v"
  done

  # Copy the unique identifier to the Wayland clipboard
  echo -n "$v" | wl-copy

  echo "Unique identifier copied: $v"
  echo "-----------------------------------"
done
