#!/usr/bin/env python3.13
import os
import sys
import json

# Print required CGI header first
print("Content-Type: text/plain\n")

try:
  # 1. Read the Content-Length to know how many bytes to read from stdin
  content_length = int(os.environ.get("CONTENT_LENGTH", 0))

  if content_length > 0:
    # 2. Read and parse the JSON data
    data = json.loads(sys.stdin.read(content_length))

    # 3. Extract your variables safely
    saveFile = data.get("saveFile", "nonAP")
    my_var_data = data.get("myVar", "{}")

    # 4. Define your file path safely
    target_dir = os.path.join(os.path.dirname(__file__), "../MQFiles")
    file_path = os.path.join(target_dir, f"loadChar_{saveFile}.json")

    # Ensure directory exists if needed, then write the data
    with open(file_path, "w") as file:
      json.dump(my_var_data, file, indent=2)

    print("go")
  else:
    print("stop No data received")

except Exception as e:
  print("stop", e)
