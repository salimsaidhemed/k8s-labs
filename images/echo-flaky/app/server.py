import json
import os
import random
import socket
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

START_TIME = time.time()

def env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, str(default)))
    except ValueError:
        return default

def pct_roll(percent: int) -> bool:
    """Return True if event should fail based on percent [0..100]."""
    if percent <= 0:
        return False
    if percent >= 100:
        return True
    return random.randint(1, 100) <= percent

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

        # Optional startup delay to simulate slow boots
        startup_delay = env_int("STARTUP_DELAY_SECONDS", 0)
        if startup_delay > 0:
            uptime = time.time() - START_TIME
            if uptime < startup_delay and parsed.path not in ("/healthz",):
                return self._send(503, {"error": "starting", "uptime_seconds": round(uptime, 2)})

        hostname = socket.gethostname()
        now = datetime.now(timezone.utc).isoformat()

        # Endpoints
        if parsed.path == "/healthz":
            # liveness should usually be stable unless you want chaos
            if pct_roll(env_int("HEALTH_FAIL_PERCENT", 0)):
                return self._send(500, {"ok": False, "reason": "health_fail_percent"})
            return self._send(200, {"ok": True})

        if parsed.path == "/readyz":
            # readiness can be intentionally flaky to stall rollouts
            if pct_roll(env_int("READY_FAIL_PERCENT", 0)):
                return self._send(503, {"ready": False, "reason": "ready_fail_percent"})
            return self._send(200, {"ready": True})

        if parsed.path in ("/", "/info", "/fail"):
            # /fail?rate=30 overrides FAIL_PERCENT just for this request
            fail_percent = env_int("FAIL_PERCENT", 0)
            if "rate" in qs and qs["rate"]:
                try:
                    fail_percent = int(qs["rate"][0])
                except ValueError:
                    pass

            if pct_roll(fail_percent):
                return self._send(500, {"error": "simulated_failure", "fail_percent": fail_percent})

            return self._send(200, {
                "app": "echo-flaky",
                "path": parsed.path,
                "time_utc": now,
                "hostname": hostname,
                "build": {
                    "sha": os.environ.get("BUILD_SHA", "unknown"),
                    "time": os.environ.get("BUILD_TIME", "unknown"),
                },
                "settings": {
                    "STARTUP_DELAY_SECONDS": startup_delay,
                    "READY_FAIL_PERCENT": env_int("READY_FAIL_PERCENT", 0),
                    "FAIL_PERCENT": env_int("FAIL_PERCENT", 0),
                }
            })

        return self._send(404, {"error": "not_found", "hint": "try /info, /healthz, /readyz, /fail?rate=30"})

def main():
    port = env_int("PORT", 8080)
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"echo-flaky listening on :{port}")
    server.serve_forever()

if __name__ == "__main__":
    main()