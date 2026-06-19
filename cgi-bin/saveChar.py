#!/usr/bin/env python3.13
import os
import re

reg = re.compile("&stat\\d+=(-?\\d+(?:\\.\\d+)?)")

try:
  with open(
    os.path.join(os.path.dirname(__file__), "../MQ2Files/loadChar.php"), "w"
  ) as file:
    newstr = re.findall(reg, os.environ.get("QUERY_STRING", ""))
    file.write(" ".join(newstr))
    # with open("C:\\Users\\User\\Desktop\\mq\\cgi-bin\\saves.txt", "w") as file:
    #     file.write(os.environ.get('QUERY_STRING', ''))
    print("go")
except Exception as e:
  print("stop")
