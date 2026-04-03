# Docker Compose 보너스 실습

이 폴더는 기존 과제 파일을 건드리지 않고, 보너스 과제 5개를 한 번에 연습할 수 있도록 만든 독립 실습 세트입니다.

## 실습 목표

이 실습을 마치면 아래를 직접 확인할 수 있습니다.

* `docker run ...` 명령이 `docker-compose.yml`에 정리되면 왜 "문서화된 실행 설정"이 되는지
* 웹 서버와 보조 서비스가 같은 Compose 네트워크에서 어떻게 서로를 찾는지
* `up`, `down`, `ps`, `logs`로 실행 상태를 어떻게 관리하는지
* 환경 변수로 포트와 모드를 바꾸는 방식
* GitHub SSH 키로 HTTPS 대신 푸시하는 흐름

## 폴더 구조

```text
bonus-compose-lab/
├── .env.example
├── .gitignore
├── app/
│   ├── Dockerfile
│   └── server.py
├── helper/
│   ├── Dockerfile
│   └── server.py
├── docker-compose.basic.yml
└── docker-compose.multi.yml
```

## 1. Compose 기초: 단일 서비스 실행

### 왜 Compose를 쓰나?

일반 `docker run`은 한 줄 명령으로 끝나서 다시 실행할 때 옵션을 잊기 쉽습니다.

예를 들어 아래 명령은 실행은 되지만, 나중에 다시 보면 옵션 의미를 기억하기 어렵습니다.

```bash
docker run -d --name my-web -p 8081:8000 -e APP_MODE=basic my-web-image
```

반면 Compose는 이 설정을 파일에 남겨 둡니다.

```yaml
services:
  web:
    build:
      context: ./app
    ports:
      - "8081:8000"
    environment:
      APP_MODE: basic
```

즉, "실행 명령"이 아니라 "실행 설정 문서"가 됩니다.

### 실행 순서

작업 위치를 실습 폴더로 이동합니다.

```bash
cd /home/keytest/E1-1/bonus-compose-lab
```

단일 서비스 Compose를 실행합니다.

```bash
docker compose -f docker-compose.basic.yml up --build -d
```

상태를 확인합니다.

```bash
docker compose -f docker-compose.basic.yml ps
```

브라우저 또는 `curl`로 확인합니다.

```bash
curl http://localhost:8081
```

예상 포인트:

* 웹 페이지에 `APP_MODE=basic`이 표시됩니다.
* 아직 보조 서비스가 없어서 helper 상태는 `not configured`로 보입니다.

종료할 때는 아래 명령을 사용합니다.

```bash
docker compose -f docker-compose.basic.yml down
```

## 2. Compose 멀티 컨테이너: 웹 + 보조 서비스

이번에는 웹 서버와 helper 서버를 같이 실행합니다.

### 핵심 개념

`docker-compose.multi.yml`에서는 `web`과 `helper`가 같은 Compose 네트워크에 들어갑니다.

그래서 `web` 컨테이너는 `helper`라는 서비스 이름만으로 아래 주소에 접속할 수 있습니다.

```text
http://helper:9000/info
```

이게 서비스 디스커버리의 가장 기초적인 모습입니다.

### 실행 순서

```bash
docker compose -f docker-compose.multi.yml up --build -d
```

상태를 확인합니다.

```bash
docker compose -f docker-compose.multi.yml ps
```

웹 페이지 확인:

```bash
curl http://localhost:8082
```

컨테이너 내부에서 helper 호출 확인:

```bash
docker compose -f docker-compose.multi.yml exec web \
python -c "import urllib.request; print(urllib.request.urlopen('http://helper:9000/info').read().decode())"
```

예상 포인트:

* 웹 페이지에 helper 메시지가 함께 보입니다.
* 위 Python 명령이 JSON 응답을 출력하면 컨테이너 간 통신이 성공한 것입니다.

종료:

```bash
docker compose -f docker-compose.multi.yml down
```

## 3. 운영 명령어 루틴 만들기

Compose를 띄운 뒤, 아래 4개 명령을 루틴처럼 반복해 보면 운영 감각을 익히기 좋습니다.

### 1. 실행

```bash
docker compose -f docker-compose.multi.yml up --build -d
```

### 2. 상태 확인

```bash
docker compose -f docker-compose.multi.yml ps
```

확인 포인트:

* 어떤 서비스가 떠 있는지
* 포트가 어떻게 매핑되었는지
* 종료된 서비스가 있는지

### 3. 로그 확인

전체 로그:

```bash
docker compose -f docker-compose.multi.yml logs
```

웹 로그만 보기:

```bash
docker compose -f docker-compose.multi.yml logs web
```

helper 로그만 보기:

```bash
docker compose -f docker-compose.multi.yml logs helper
```

### 4. 종료

```bash
docker compose -f docker-compose.multi.yml down
```

짧은 운영 루틴 예시:

```bash
docker compose -f docker-compose.multi.yml up --build -d
docker compose -f docker-compose.multi.yml ps
docker compose -f docker-compose.multi.yml logs web
docker compose -f docker-compose.multi.yml down
```

## 4. 환경 변수 실습

Compose는 같은 폴더의 `.env` 파일을 자동으로 읽습니다.

먼저 예시 파일을 복사합니다.

```bash
cp .env.example .env
```

기본 예시:

```env
WEB_PORT=8082
APP_PORT=8000
APP_MODE=multi
HELPER_PORT=9000
HELPER_MESSAGE=Hello from helper service
HELPER_URL=http://helper:9000
```

### 실습 A: 웹 포트 바꾸기

`.env`에서 아래 값을 바꿉니다.

```env
WEB_PORT=8090
```

다시 실행합니다.

```bash
docker compose -f docker-compose.multi.yml up --build -d
curl http://localhost:8090
```

배움 포인트:

* 코드 수정 없이 외부 접속 포트만 바뀝니다.

### 실습 B: 앱 모드 바꾸기

`.env`에서 아래 값을 바꿉니다.

```env
APP_MODE=debug
```

다시 실행 후 웹 페이지를 확인합니다.

배움 포인트:

* 코드 안 문자열을 고치지 않아도 실행 모드만 바뀝니다.

### 실습 C: helper 메시지 바꾸기

`.env`에서 아래 값을 바꿉니다.

```env
HELPER_MESSAGE=compose network is working
```

다시 실행 후 웹 페이지를 확인합니다.

배움 포인트:

* 보조 서비스의 설정도 Compose에서 관리할 수 있습니다.

## 5. 파일 읽는 법

### `docker-compose.basic.yml`

* `services`: 실행할 컨테이너 목록
* `build`: 어떤 Dockerfile로 이미지를 만들지
* `ports`: 호스트 포트와 컨테이너 포트 연결
* `environment`: 컨테이너 내부 환경 변수

### `docker-compose.multi.yml`

* `web`: 사용자 접속용 웹 서비스
* `helper`: 웹 서비스가 내부적으로 호출하는 보조 서비스
* `depends_on`: helper를 먼저 띄우도록 힌트 제공

## 6. GitHub SSH 키 설정 실습

이 부분은 Compose와 별개로 따라 하면 됩니다.

### 1. SSH 키 생성

이미 키가 있는지 먼저 확인합니다.

```bash
ls -al ~/.ssh
```

없다면 새 키를 만듭니다.

```bash
ssh-keygen -t ed25519 -C "keytest@naver.com"
```

그다음 SSH 에이전트를 시작하고 키를 등록합니다.

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### 2. 공개키 확인

```bash
cat ~/.ssh/id_ed25519.pub
```

출력된 한 줄 전체를 GitHub의 `Settings > SSH and GPG keys > New SSH key`에 등록합니다.

### 3. 연결 테스트

```bash
ssh -T git@github.com
```

처음 접속 시 호스트 확인 메시지가 나오면 `yes`를 입력합니다.

정상이라면 아래와 비슷한 메시지가 나옵니다.

```text
Hi <github-id>! You've successfully authenticated, but GitHub does not provide shell access.
```

### 4. 원격 저장소 주소를 SSH로 변경

현재 원격 주소 확인:

```bash
git remote -v
```

HTTPS였다면 SSH 주소로 바꿉니다.

```bash
git remote set-url origin git@github.com:zzxy72/E1-1.git
```

다시 확인:

```bash
git remote -v
```

이후 푸시 테스트:

```bash
git push origin main
```

## 7. 추천 실습 순서

아래 순서로 하면 가장 이해가 쉽습니다.

1. `docker-compose.basic.yml`로 단일 서비스 실행
2. `docker-compose.multi.yml`로 멀티 컨테이너 실행
3. `ps`, `logs`, `down` 반복
4. `.env` 수정해서 포트, 모드, helper 메시지 바꾸기
5. 마지막에 GitHub SSH 키 등록 후 `git push` 테스트

## 8. 문제 생겼을 때 확인 포인트

### 포트 접속이 안 될 때

```bash
docker compose -f docker-compose.multi.yml ps
docker compose -f docker-compose.multi.yml logs
```

### helper 연결이 안 될 때

```bash
docker compose -f docker-compose.multi.yml exec web \
python -c "import urllib.request; print(urllib.request.urlopen('http://helper:9000/info').read().decode())"
```

### 포트가 이미 사용 중일 때

`.env`의 `WEB_PORT` 값을 `8090`, `8091`처럼 다른 값으로 바꿔 다시 실행합니다.

---

가장 중요한 한 줄 정리:

* Compose는 "컨테이너 실행 명령을 외워서 치는 방식"을 "파일로 남기는 방식"으로 바꿔 줍니다.
* 멀티 컨테이너에서는 서비스 이름이 곧 내부 네트워크 주소가 됩니다.
* 환경 변수는 설정을 코드 밖으로 빼내는 가장 쉬운 첫걸음입니다.
