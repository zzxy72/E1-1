import json
import os
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer


HELPER_PORT = int(os.getenv("HELPER_PORT", "9000"))
HELPER_MESSAGE = os.getenv("HELPER_MESSAGE", "Hello from helper service")
HOSTNAME = socket.gethostname()


class Handler(BaseHTTPRequestHandler):
    def _send(self, body):
        encoded = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        payload = json.dumps(
            {
                "status": "ok",
                "service": "helper",
                "message": HELPER_MESSAGE,
                "hostname": HOSTNAME,
                "path": self.path,
            },
            ensure_ascii=False,
        )
        self._send(payload)


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", HELPER_PORT), Handler)
    print(f"[helper] listening on 0.0.0.0:{HELPER_PORT}")
    server.serve_forever()
