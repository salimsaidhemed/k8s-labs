import os
import socket
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)

def page(color: str, title: str, lines: list[str]) -> bytes:
    safe_color = color.strip() or "#2d7ef7"
    items = "".join(f"<li><code>{line}</code></li>" for line in lines)
    html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; padding: 24px; }}
    .box {{ height: 180px; border-radius: 18px; background: {safe_color}; }}
    code {{ background: #f2f2f2; padding: 2px 6px; border-radius: 6px; }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <div class="box"></div>
  <p>Theme: <code>{safe_color}</code></p>
  <ul>{items}</ul>
</body>
</html>
"""
    return html.encode("utf-8")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path not in ("/", "/color", "/healthz", "/readyz"):
            self.send_response(404); self.end_headers(); return

        if parsed.path == "/healthz":
            self.send_response(200); self.end_headers(); return
        if parsed.path == "/readyz":
            self.send_response(200); self.end_headers(); return

        hostname = socket.gethostname()
        now = datetime.now(timezone.utc).isoformat()

        lines = [
            f"hostname={hostname}",
            f"time_utc={now}",
            f"BUILD_SHA={env('BUILD_SHA','unknown')}",
            f"BUILD_TIME={env('BUILD_TIME','unknown')}",
        ]

        color = env("THEME_COLOR", "#2d7ef7")
        body = page(color, "echo-color", lines)

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

def main():
    port = int(env("PORT", "8080"))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"echo-color listening on :{port}")
    server.serve_forever()

if __name__ == "__main__":
    main()