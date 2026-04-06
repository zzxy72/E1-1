import json          # JSON 형식으로 데이터를 변환(직렬화/역직렬화)하기 위한 표준 라이브러리
import os             # 운영체제 환경변수를 읽기 위한 표준 라이브러리
import socket         # 호스트명(컴퓨터 이름)을 가져오기 위한 네트워크 관련 표준 라이브러리
from http.server import BaseHTTPRequestHandler, HTTPServer
# BaseHTTPRequestHandler: HTTP 요청을 처리하는 핸들러의 기본 클래스
# HTTPServer: 간단한 HTTP 서버를 만들어주는 클래스

# ──────────────────────────────────────────────
# 환경변수에서 설정값 읽기 (없으면 기본값 사용)
# ──────────────────────────────────────────────

HELPER_PORT = int(os.getenv("HELPER_PORT", "9000"))
# 환경변수 "HELPER_PORT"를 읽어서 정수로 변환. 없으면 기본값 9000번 포트 사용

HELPER_MESSAGE = os.getenv("HELPER_MESSAGE", "Hello from helper service")
# 환경변수 "HELPER_MESSAGE"를 읽음. 없으면 기본 인사 메시지 사용

HOSTNAME = socket.gethostname()
# 현재 서버(컨테이너)의 호스트명을 가져옴 (Docker 환경에서는 컨테이너 ID가 됨)


# ──────────────────────────────────────────────
# HTTP 요청을 처리하는 핸들러 클래스 정의
# ──────────────────────────────────────────────

class Handler(BaseHTTPRequestHandler):
    # BaseHTTPRequestHandler를 상속받아 커스텀 핸들러를 만듦

    def _send(self, body):
        # 응답을 보내는 공통 메서드 (내부에서만 사용하므로 _로 시작)

        encoded = body.encode("utf-8")
        # 문자열을 UTF-8 바이트로 인코딩 (네트워크 전송을 위해)

        self.send_response(200)
        # HTTP 상태코드 200(성공)을 응답으로 보냄

        self.send_header("Content-Type", "application/json; charset=utf-8")
        # 응답 헤더: "이 데이터는 JSON 형식이고 UTF-8 인코딩이다"라고 알려줌

        self.send_header("Content-Length", str(len(encoded)))
        # 응답 헤더: 보낼 데이터의 바이트 크기를 알려줌

        self.end_headers()
        # 헤더 작성 완료를 알림 (헤더와 본문 사이에 빈 줄 삽입)

        self.wfile.write(encoded)
        # 실제 응답 본문(body)을 클라이언트에게 전송

    def do_GET(self):
        # GET 요청이 들어왔을 때 자동으로 호출되는 메서드

        payload = json.dumps(
            # 파이썬 딕셔너리를 JSON 문자열로 변환
            {
                "status": "ok",              # 서비스 상태: 정상
                "service": "helper",         # 서비스 이름: helper
                "message": HELPER_MESSAGE,   # 환경변수에서 읽은 메시지
                "hostname": HOSTNAME,        # 현재 서버의 호스트명
                "path": self.path,           # 클라이언트가 요청한 URL 경로 (예: "/health")
            },
            ensure_ascii=False,
            # 한글 등 비ASCII 문자를 \uXXXX로 변환하지 않고 그대로 출력
        )
        self._send(payload)
        # 위에서 만든 JSON 문자열을 클라이언트에게 응답으로 보냄


# ──────────────────────────────────────────────
# 서버 실행 (이 파일을 직접 실행할 때만 동작)
# ──────────────────────────────────────────────

if __name__ == "__main__":
    # 이 파일이 직접 실행될 때만 아래 코드 실행 (import 될 때는 실행 안 됨)

    server = HTTPServer(("0.0.0.0", HELPER_PORT), Handler)
    # HTTP 서버 생성
    # "0.0.0.0": 모든 네트워크 인터페이스에서 접속 허용 (외부에서도 접근 가능)
    # HELPER_PORT: 위에서 설정한 포트 번호 (기본 9000)
    # Handler: 요청이 오면 위에서 정의한 Handler 클래스가 처리

    print(f"[helper] listening on 0.0.0.0:{HELPER_PORT}")
    # 서버가 시작되었음을 콘솔에 출력 (어떤 포트에서 대기 중인지 표시)

    server.serve_forever()
    # 서버를 무한 루프로 실행하여 계속 요청을 받음 (Ctrl+C로 종료 가능)
    