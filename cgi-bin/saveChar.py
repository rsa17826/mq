#!/usr/bin/env python3.13
import os
import re
from urllib.parse import parse_qs

reg = re.compile("&stat\\d+=(-?\\d+(?:\\.\\d+)?)")


try:
  query_string = os.environ.get("QUERY_STRING", "")
  parsed_params = parse_qs(query_string)
  saveFile = parsed_params.get("saveFile", ["nonAP"])[0]
  with open(
    os.path.join(os.path.dirname(__file__), f"../MQFiles/loadChar_{saveFile}.php"),
    "w",
  ) as file:
    newstr = re.findall(reg, os.environ.get("QUERY_STRING", ""))
    file.write(" ".join(newstr))
    # with open("C:\\Users\\User\\Desktop\\mq\\cgi-bin\\saves.txt", "w") as file:
    #     file.write(os.environ.get('QUERY_STRING', ''))
    print("go")
except Exception as e:
  print("stop", e)
