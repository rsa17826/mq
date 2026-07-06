#!/usr/bin/env python3
"""
Standalone desktop wrapper for server.py.
"""

import threading
from http.server import HTTPServer

import webview

from server import PORT, CachedCGIHTTPRequestHandler

SERVER_URL = f"http://127.0.0.1:{PORT}/MathQuest/play.html?connect=127.0.0.1:38281&name=test1&passwd="


class ServerApp:
  def __init__(self):
    self.httpd = HTTPServer(("", PORT), CachedCGIHTTPRequestHandler)
    self.server_thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)

  def shutdown_server(self):
    self.httpd.shutdown()
    self.httpd.server_close()

  def run(self):
    self.server_thread.start()

    # 1. Initialize the window as transparent.
    # A transparent window uses the alpha channel of your desktop compositor.
    # This prevents the window manager from filling it with a default white template!
    window = webview.create_window(
      "MathQuest",
      SERVER_URL,
      width=1100,
      height=750,
      min_size=(500, 400),
      transparent=True, # <-- Prevents the white canvas allocation entirely
    )

    window.events.closed += self.shutdown_server

    # 2. We keep transparent=True. Because your HTML/CSS file specifies
    # background-color: #111; the browser will automatically fill the space
    # with your dark gray color as soon as it renders.

    webview.start()


if __name__ == "__main__":
  ServerApp().run()
