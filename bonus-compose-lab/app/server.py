import json
import os
import socket
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer


APP_PORT = int(os.getenv("APP_PORT", "8000"))
APP_MODE = os.getenv("APP_MODE", "basic")
HELPER_URL = os.getenv("HELPER_URL", "").rstrip("/")
HOSTNAME = socket.gethostname()


def fetch_helper():
    if not HELPER_URL:
        return {
            "connected": False,
            "message": "not configured",
        }

    info_url = f"{HELPER_URL}/info"
    try:
        with urllib.request.urlopen(info_url, timeout=2) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return {
            "connected": True,
            "url": info_url,
            "payload": payload,
        }
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {
            "connected": False,
            "url": info_url,
            "message": str(exc),
        }


def render_home():
    helper = fetch_helper()
    helper_block = json.dumps(helper, ensure_ascii=False, indent=2)
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>Compose Web Lab</title>
  <style>
    body {{
      font-family: sans-serif;
      max-width: 860px;
      margin: 40px auto;
      line-height: 1.6;
      padding: 0 16px;
    }}
    code, pre {{
      background: #f4f4f4;
      border-radius: 8px;
      padding: 2px 6px;
    }}
    pre {{
      padding: 16px;
      overflow-x: auto;
    }}
  </style>
</head>
<body>
  <h1>Docker Compose Web Service</h1>
  <p>웹 서비스가 정상 실행 중입니다.</p>
  <ul>
    <li>APP_MODE: <strong>{APP_MODE}</strong></li>
    <li>APP_PORT: <strong>{APP_PORT}</strong></li>
    <li>HOSTNAME: <strong>{HOSTNAME}</strong></li>
    <li>HELPER_URL: <strong>{HELPER_URL or "not configured"}</strong></li>
  </ul>
  <h2>Helper 상태</h2>
  <pre>{helper_block}</pre>
  <p>이 페이지에 helper 응답이 보이면 서비스 이름 기반 통신이 성공한 것입니다.</p>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, body, content_type):
        encoded = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        if self.path == "/health":
            payload = json.dumps(
                {
                    "status": "ok",
                    "service": "web",
                    "mode": APP_MODE,
                    "hostname": HOSTNAME,
                },
                ensure_ascii=False,
            )
            self._send(payload, "application/json; charset=utf-8")
            return

        if self.path == "/api/helper":
            payload = json.dumps(fetch_helper(), ensure_ascii=False)
            self._send(payload, "application/json; charset=utf-8")
            return

        self._send(render_home(), "text/html; charset=utf-8")


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", APP_PORT), Handler)
    print(f"[web] listening on 0.0.0.0:{APP_PORT} mode={APP_MODE}")
    server.serve_forever()
