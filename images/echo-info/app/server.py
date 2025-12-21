import json
import os
import socket
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)

class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: dict):
        data = json.dumps(body, indent=2).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)

        now = datetime.now(timezone.utc).isoformat()
        hostname = socket.gethostname()

        body = {
            "app": "echo-info",
            "path": parsed.path,
            "query": {k: v for k, v in qs.items()},
            "time_utc": now,
            "hostname": hostname,
            "build": {
                "sha": env("BUILD_SHA", "unknown"),
                "time": env("BUILD_TIME", "unknown"),
                "image_tag": env("IMAGE_TAG", ""),
            },
            "runtime": {
                "pod": env("POD_NAME", ""),
                "namespace": env("POD_NAMESPACE", ""),
                "node": env("NODE_NAME", ""),
            },
            "headers": {k: v for (k, v) in self.headers.items()},
        }

        if parsed.path in ("/", "/info"):
            return self._send(200, body)

        if parsed.path == "/healthz":
            return self._send(200, {"ok": True})

        if parsed.path == "/readyz":
            return self._send(200, {"ready": True})

        return self._send(404, {"error": "not_found", "hint": "try /info, /healthz, /readyz"})

def main():
    port = int(env("PORT", "8080"))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"echo-info listening on :{port}")
    server.serve_forever()

if __name__ == "__main__":
    main()