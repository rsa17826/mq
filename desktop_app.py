#!/usr/bin/env python3
"""
Standalone desktop wrapper for server.py.

Runs the HTTP server in a background thread and opens it inside a native
app window (via pywebview / WebKitGTK) instead of a browser tab, so it
looks and behaves like a normal desktop application.
"""

import threading
from http.server import HTTPServer

import webview

from server import PORT, CachedCGIHTTPRequestHandler

SERVER_URL = f"http://127.0.0.1:{PORT}/MathQuest/play.html?connect=127.0.0.1:38281&name=test1&passwd="


class ServerApp:
  def __init__(self):
    self.httpd = HTTPServer(("", PORT), CachedCGIHTTPRequestHandler)
    self.server_thread = threading.Thread(
      target=self.httpd.serve_forever, daemon=True
    )

  def shutdown_server(self):
    self.httpd.shutdown()
    self.httpd.server_close()

  def run(self):
    self.server_thread.start()

    window = webview.create_window(
      "Server App",
      SERVER_URL,
      width=1100,
      height=750,
      min_size=(500, 400),
    )
    # Make sure the HTTP server dies when the window is closed, so the
    # process doesn't hang around in the background afterward.
    window.events.closed += self.shutdown_server

    webview.start()


if __name__ == "__main__":
  ServerApp().run()
