# AI/SW 개발 워크스테이션 구축

## 프로젝트 개요

이 문서는 터미널, Docker, Git/GitHub를 이용해 개발 워크스테이션을 구축하고 검증한 결과를 정리한 README다.

## 실행 환경

| 항목 | 내용 |
| --- | --- |
| 장비 | iMac |
| 운영체제 | `macOS 15.7.4` |
| Shell | `zsh` |
| Terminal | `Apple_Terminal` |
| Docker 실행 환경 | OrbStack |
| Docker Version | `28.5.2, build ecc6942` |
| Git Version | `2.53.0` |
| GitHub 연동 방식 | `HTTPS` |

실습:

```bash
sw_vers
echo $SHELL
echo $TERM_PROGRAM
docker --version
git --version
```

## 수행 체크리스트

* [x] 터미널 기본 조작 수행
* [x] 파일 권한 변경 실습
* [x] 디렉토리 권한 변경 실습
* [x] Docker 설치 및 점검
* [x] Docker 기본 운영 명령 수행
* [x] `hello-world` 실행
* [x] `ubuntu` 컨테이너 내부 진입
* [x] Dockerfile 기반 커스텀 이미지 빌드 및 실행
* [x] 포트 매핑 접속 확인
* [x] Docker 볼륨 영속성 검증
* [x] Git 설정 및 GitHub 연동
* [x] 트러블슈팅 2건 이상 정리

## 검증 방법

| 검증 항목 | 확인 방법 | 기록 위치 |
| --- | --- | --- |
| 실행 환경 | `sw_vers`, `echo $SHELL`, `docker --version`, `git --version` | 실행 환경 |
| 터미널 조작 | `pwd`, `ls -la`, `mkdir`, `cp`, `mv`, `rm`, `cat`, `touch` | 1. 터미널 기본 조작 |
| 권한 실습 | `ls -l`, `chmod` 전/후 비교 | 2. 권한 실습 |
| Docker 점검 | `docker --version`, `docker info` | 3. Docker 설치 및 점검 |
| Docker 운영 | `docker images`, `docker ps`, `docker ps -a`, `docker logs`, `docker stats` | 4. Docker 기본 운영 |
| hello-world | `docker run hello-world`, `docker ps -a`, `docker logs` | 5. 컨테이너 실행 실습 |
| ubuntu | `docker run -it ubuntu bash` | 5. 컨테이너 실행 실습 |
| Dockerfile | `docker build`, `docker run` | 6. Dockerfile 실습 |
| 포트 매핑 | 브라우저 또는 `curl` | 7. 포트 매핑 검증 |
| 볼륨 영속성 | 컨테이너 삭제 전/후 데이터 비교 | 8. Docker 볼륨 검증 |
| Git/GitHub | `git config --list`, `git remote -v`, 연동 화면 | 9. Git 설정 및 연동 |

## 1. 터미널 기본 조작 로그

실습할 명령:

```bash
pwd
ls -la
mkdir -p practice-dir
cd practice-dir
touch empty.txt
echo "hello" > sample.txt
cat sample.txt
cp sample.txt sample-copy.txt
mv sample-copy.txt renamed.txt
cd ..
rm -rf practice-dir
```

실습:

```bash
***@*** E1-1 % pwd
/Users/***/E1-1
***@*** E1-1 % ls -la
total 32
drwxr-xr-x   6 ***  ***    192 Mar 31 19:39 .
drwxr-x---+ 20 ***  ***    640 Mar 31 18:55 ..
drwxr-xr-x  14 ***  ***    448 Mar 31 19:43 .git
-rw-r--r--   1 ***  ***  13334 Mar 31 19:51 README.md
drwxr-xr-x   2 ***  ***     64 Mar 31 19:42 요구분석
drwxr-xr-x   3 ***  ***     96 Mar 31 17:34 요구사항
***@*** E1-1 % mkdir -p practice-dir
***@*** E1-1 % cd practice-dir
***@*** practice-dir % touch empty.txt
***@*** practice-dir % echo "hello" > sample.txt
***@*** practice-dir % cat sample.txt
hello
***@*** practice-dir % cp sample.txt sample-copy.txt
***@*** practice-dir % mv sample-copy.txt renamed.txt
***@*** practice-dir % cd ..
***@*** E1-1 % rm -rf practice-dir
```

## 2. 권한 실습

실습할 명령:

```bash
mkdir -p permission-lab
touch permission-lab/file.txt
ls -ld permission-lab
ls -l permission-lab/file.txt
chmod 700 permission-lab
chmod 600 permission-lab/file.txt
ls -ld permission-lab
ls -l permission-lab/file.txt
chmod 755 permission-lab
chmod 644 permission-lab/file.txt
ls -ld permission-lab
ls -l permission-lab/file.txt
```

실습:

```bash
***@*** E1-1 % mkdir -p permission-lab
***@*** E1-1 % touch permission-lab/file.txt
***@*** E1-1 % ls -ld permission-lab
drwxr-xr-x  3 ***  ***  96 Mar 31 20:06 permission-lab
***@*** E1-1 % ls -l permission-lab/file.txt
-rw-r--r--  1 ***  ***  0 Mar 31 20:06 permission-lab/file.txt
***@*** E1-1 % chmod 755 permission-lab
***@*** E1-1 % chmod 644 permission-lab/file.txt
***@*** E1-1 % ls -ld permission-lab
drwxr-xr-x  3 ***  ***  96 Mar 31 20:06 permission-lab
***@*** E1-1 % chmod 700 permission-lab
***@*** E1-1 % ls -ld 
drwxr-xr-x  7 ***  ***  224 Mar 31 20:06 .
***@*** E1-1 % ls -ld permission-lab
drwx------  3 ***  ***  96 Mar 31 20:06 permission-lab
***@*** E1-1 % chmod 755 permission-lab
***@*** E1-1 % ls -ld
drwxr-xr-x  7 ***  ***  224 Mar 31 20:06 .
***@*** E1-1 % ls -ld permission-lab
drwxr-xr-x  3 ***  ***  96 Mar 31 20:06 permission-lab
***@*** E1-1 % chmod 600 permission-lab/file.txt
***@*** E1-1 % ls -l permission-lab/file.txt
-rw-------  1 ***  ***  0 Mar 31 20:06 permission-lab/file.txt
***@*** E1-1 % chmod 644 permission-lab/file.txt
***@*** E1-1 % ls -l permission-lab/file.txt
-rw-r--r--  1 ***  ***  0 Mar 31 20:06 permission-lab/file.txt
***@*** E1-1 %

```

확인 결과:

* 파일 1개와 디렉토리 1개 모두 전후 비교가 보여야 한다.
* `755`는 디렉토리 예시, `644`는 파일 예시로 쓰기 좋다.

## 3. Docker 설치 및 점검

실습할 명령:

```bash
docker --version
docker info
```

실습:

```bash
***@*** E1-1 % docker --version
Docker version 28.5.2, build ecc6942
***@*** E1-1 % docker info
Client:
 Version:    28.5.2
 Context:    orbstack
 Debug Mode: false
 Plugins:
  buildx: Docker Buildx (Docker Inc.)
    Version:  v0.29.1
    Path:     /Users/***/.docker/cli-plugins/docker-buildx
  compose: Docker Compose (Docker Inc.)
    Version:  v2.40.3
    Path:     /Users/***/.docker/cli-plugins/docker-compose

Server:
 Containers: 1
  Running: 0
  Paused: 0
  Stopped: 1
 Images: 2
 Server Version: 28.5.2
 Storage Driver: overlay2
  Backing Filesystem: btrfs
  Supports d_type: true
  Using metacopy: false
  Native Overlay Diff: true
  userxattr: false
 Logging Driver: json-file
 Cgroup Driver: cgroupfs
 Cgroup Version: 2
 Plugins:
  Volume: local
  Network: bridge host ipvlan macvlan null overlay
  Log: awslogs fluentd gcplogs gelf journald json-file local splunk syslog
 CDI spec directories:
  /etc/cdi
  /var/run/cdi
 Swarm: inactive
 Runtimes: io.containerd.runc.v2 runc
 Default Runtime: runc
 Init Binary: docker-init
 containerd version: 1c4457e00facac03ce1d75f7b6777a7a851e5c41
 runc version: d842d7719497cc3b774fd71620278ac9e17710e0
 init version: de40ad0
 Security Options:
  seccomp
   Profile: builtin
  cgroupns
 Kernel Version: 6.17.8-orbstack-00308-g8f9c941121b1
 Operating System: OrbStack
 OSType: linux
 Architecture: x86_64
 CPUs: 6
 Total Memory: 15.67GiB
 Name: orbstack
 ID: b49c6cdc-98e4-40ba-b429-572fc12bdf86
 Docker Root Dir: /var/lib/docker
 Debug Mode: false
 Experimental: false
 Insecure Registries:
  ::1/128
  127.0.0.0/8
 Live Restore Enabled: false
 Product License: Community Engine
 Default Address Pools:
   Base: 192.168.97.0/24, Size: 24
   Base: 192.168.107.0/24, Size: 24
   Base: 192.168.117.0/24, Size: 24
   Base: 192.168.147.0/24, Size: 24
   Base: 192.168.148.0/24, Size: 24
   Base: 192.168.155.0/24, Size: 24
   Base: 192.168.156.0/24, Size: 24
   Base: 192.168.158.0/24, Size: 24
   Base: 192.168.163.0/24, Size: 24
   Base: 192.168.164.0/24, Size: 24
   Base: 192.168.165.0/24, Size: 24
   Base: 192.168.166.0/24, Size: 24
   Base: 192.168.167.0/24, Size: 24
   Base: 192.168.171.0/24, Size: 24
   Base: 192.168.172.0/24, Size: 24
   Base: 192.168.181.0/24, Size: 24
   Base: 192.168.183.0/24, Size: 24
   Base: 192.168.186.0/24, Size: 24
   Base: 192.168.207.0/24, Size: 24
   Base: 192.168.214.0/24, Size: 24
   Base: 192.168.215.0/24, Size: 24
   Base: 192.168.216.0/24, Size: 24
   Base: 192.168.223.0/24, Size: 24
   Base: 192.168.227.0/24, Size: 24
   Base: 192.168.228.0/24, Size: 24
   Base: 192.168.229.0/24, Size: 24
   Base: 192.168.237.0/24, Size: 24
   Base: 192.168.239.0/24, Size: 24
   Base: 192.168.242.0/24, Size: 24
   Base: 192.168.247.0/24, Size: 24
   Base: fd07:b51a:cc66:d000::/56, Size: 64

WARNING: DOCKER_INSECURE_NO_IPTABLES_RAW is set
***@*** E1-1 %

```

## 4. Docker 기본 운영

실습할 명령:

```bash
docker pull hello-world
docker images
docker rm -f hello-test 2>/dev/null || true
docker run --name hello-test hello-world
docker ps
docker ps -a
docker logs hello-test
docker stats --no-stream
```

실습:

```bash
keytest1591@c3r1s7 E1-1 % 
keytest1591@c3r1s7 E1-1 % docker pull hello-world
Using default tag: latest
latest: Pulling from library/hello-world
4f55086f7dd0: Pull complete 
Digest: sha256:452a468a4bf985040037cb6d5392410206e47db9bf5b7278d281f94d1c2d0931
Status: Downloaded newer image for hello-world:latest
docker.io/library/hello-world:latest
keytest1591@c3r1s7 E1-1 % docker images
REPOSITORY    TAG       IMAGE ID       CREATED      SIZE
hello-world   latest    e2ac70e7319a   8 days ago   10.1kB
keytest1591@c3r1s7 E1-1 % docker rm -f hello-test 2>/dev/null || true
keytest1591@c3r1s7 E1-1 % docker run --name hello-test hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/

keytest1591@c3r1s7 E1-1 % docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
keytest1591@c3r1s7 E1-1 % docker ps -a
CONTAINER ID   IMAGE         COMMAND    CREATED          STATUS                      PORTS     NAMES
2659efcff4c4   hello-world   "/hello"   32 seconds ago   Exited (0) 31 seconds ago             hello-test
keytest1591@c3r1s7 E1-1 % docker logs hello-test

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/

keytest1591@c3r1s7 E1-1 % docker stats --no-stream
CONTAINER ID   NAME      CPU %     MEM USAGE / LIMIT   MEM %     NET I/O   BLOCK I/O   PIDS
keytest1591@c3r1s7 E1-1 % 

```

확인 결과:
* docker pull hello-world 이 명령어는 Docker Hub(온라인 저장소)에서 'hello-world'라는 이미지를 다운로드하는 것입니다.
* `hello-world`는 Docker 공식 테스트용 이미지다.
* docker images 이 명령어는 당신의 컴퓨터에 저장된 모든 Docker 이미지를 목록으로 보여줍니다.
* Docker 이미지 = 프로그램을 실행하기 위한 설계도 또는 템플릿. 
* docker rm -f hello-test 2>/dev/null || true 
  - "hello-test라는 컨테이너를 강제로 삭제하되, 에러가 나도 무시하고 계속 진행하라"
* `docker ps`는 실행 중 컨테이너만 보여준다.
* `hello-world`는 실행 후 바로 종료되므로 `docker ps`에는 안 보일 수 있다.
* 종료된 컨테이너는 `docker ps -a`에서, 출력 내용은 `docker logs hello-test`에서 확인한다.
* docker stats --no-stream  
  - "현재 실행 중인 모든 컨테이너의 자원 사용량을 한 번만 보여줘"


## 5. 컨테이너 실행 실습

### 5.1 hello-world

설명:

* `hello-world`는 Docker에서 제공하는 공식 테스트용 이미지다.
* 이 실습은 이미지 다운로드, 컨테이너 생성, 실행, 종료까지의 가장 기본 흐름이 정상인지 확인하기 위한 단계다.
* `hello-world` 컨테이너는 메시지를 출력한 뒤 바로 종료되므로 `docker ps`에는 안 보일 수 있다.
* 따라서 실행 여부는 `docker ps -a`와 `docker logs hello-test`로 확인하는 것이 맞다.

실습할 명령:

```bash
docker rm -f hello-test 2>/dev/null || true
docker run --name hello-test hello-world
docker ps -a
docker logs hello-test

```

실습:

```bash
keytest1591@c3r1s7 E1-1 % 
keytest1591@c3r1s7 E1-1 % docker rm -f hello-test 2>/dev/null || true
docker run --name hello-test hello-world
docker ps -a
docker logs hello-test
hello-test

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/

CONTAINER ID   IMAGE         COMMAND    CREATED        STATUS                              PORTS     NAMES
3c5e84e0987a   hello-world   "/hello"   1 second ago   Exited (0) Less than a second ago             hello-test

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/

keytest1591@c3r1s7 E1-1 % 


```

### 5.2 ubuntu 컨테이너 내부 진입

실습할 명령:

```bash
docker rm -f ubuntu-test 2>/dev/null || true
docker run -it --name ubuntu-test ubuntu bash
ls
echo "inside container"
exit
docker ps -a
```

실습:

```bash
keytest1591@c3r1s7 E1-1 % 
keytest1591@c3r1s7 E1-1 % docker rm -f ubuntu-test 2>/dev/null || true
docker run -it --name ubuntu-test ubuntu bash
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
817807f3c64e: Pull complete 
Digest: sha256:186072bba1b2f436cbb91ef2567abca677337cfc786c86e107d25b7072feef0c
Status: Downloaded newer image for ubuntu:latest
root@f375ae595e47:/# 
root@f375ae595e47:/# #
root@f375ae595e47:/# ls
bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
root@f375ae595e47:/# echo "inside container"
inside container
root@f375ae595e47:/# 
root@f375ae595e47:/# #
root@f375ae595e47:/# exit
exit
keytest1591@c3r1s7 E1-1 % 
keytest1591@c3r1s7 E1-1 % docker ps -a
CONTAINER ID   IMAGE         COMMAND    CREATED              STATUS                      PORTS     NAMES
f375ae595e47   ubuntu        "bash"     About a minute ago   Exited (0) 21 seconds ago             ubuntu-test
849e87b44b28   hello-world   "/hello"   18 minutes ago       Exited (0) 18 minutes ago             hello-test
keytest1591@c3r1s7 E1-1 % 

```

간단 정리:
* docker run -it : 입력도 받고 (-i) 터미널 화면도 제대로 보임 (-t)


## 6. Dockerfile 기반 커스텀 이미지 제작

실습 전 준비:

* 현재 오류 원인: `docker build -t my-web:1.0 .` 를 실행한 폴더에 `Dockerfile`이 없어서 빌드가 실패할 수 있다.
* 따라서 `Dockerfile`과 웹 테스트용 `index.html`을 만든 뒤 빌드를 진행한다.

실습 후 작성:

* 베이스 이미지: `nginx:alpine`
* 선택 이유: `가볍고 정적 웹 페이지 테스트에 적합함`
* 커스텀 포인트: `기본 nginx 웹 루트에 index.html 복사`
* 목적: `Dockerfile 빌드, 이미지 생성, 컨테이너 실행, 포트 매핑 확인`

실습할 파일 준비:

`Dockerfile`

```Dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
```

`index.html`

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <title>my-web</title>
</head>
<body>
  <h1>Hello Docker</h1>
  <p>custom nginx container is running</p>
</body>
</html>
```

파일 생성 실습 명령:

```bash
cat > Dockerfile <<'EOF'
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
EOF

cat > index.html <<'EOF'
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <title>my-web</title>
</head>
<body>
  <h1>Hello Docker</h1>
  <p>custom nginx container is running</p>
</body>
</html>
EOF

ls -la
cat Dockerfile
cat index.html
```

실습할 명령:

```bash
docker rm -f my-web 2>/dev/null || true
docker build -t my-web:1.0 .
docker run -d -p 8080:80 --name my-web my-web:1.0
docker ps
docker logs my-web
```

실습:

```bash
keytest1591@c3r1s7 E1-1 % 
keytest1591@c3r1s7 E1-1 % 
keytest1591@c3r1s7 E1-1 % docker rm -f my-web 2>/dev/null || true
docker build -t my-web:1.0 .
[+] Building 0.5s (1/1) FINISHED                                                                                   docker:orbstack
 => [internal] load build definition from Dockerfile                                                                          0.2s
 => => transferring dockerfile: 2B                                                                                            0.0s
ERROR: failed to build: failed to solve: failed to read dockerfile: open Dockerfile: no such file or directory
keytest1591@c3r1s7 E1-1 % 
keytest1591@c3r1s7 E1-1 % 
keytest1591@c3r1s7 E1-1 % pwd
ls -la
find . -maxdepth 2 -name Dockerfile
/Users/***/E1-1
total 88
drwxr-xr-x   6 keytest1591  keytest1591    192 Apr  1 15:29 .
drwxr-x---+ 24 keytest1591  keytest1591    768 Apr  1 14:20 ..
drwxr-xr-x  14 keytest1591  keytest1591    448 Apr  1 14:03 .git
-rw-r--r--   1 keytest1591  keytest1591  18921 Apr  1 15:29 README copy.md
-rw-r--r--   1 keytest1591  keytest1591  22674 Apr  1 15:36 README.md
drwxr-xr-x   3 keytest1591  keytest1591     96 Apr  1 13:59 요구사항
keytest1591@c3r1s7 E1-1 % cat > Dockerfile <<'EOF'
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
EOF

cat > index.html <<'EOF'
<h1>Hello Docker</h1>
EOF

keytest1591@c3r1s7 E1-1 % ls -la
total 104
drwxr-xr-x   8 keytest1591  keytest1591    256 Apr  1 15:47 .
drwxr-x---+ 24 keytest1591  keytest1591    768 Apr  1 14:20 ..
drwxr-xr-x  14 keytest1591  keytest1591    448 Apr  1 14:03 .git
-rw-r--r--   1 keytest1591  keytest1591     67 Apr  1 15:47 Dockerfile
-rw-r--r--   1 keytest1591  keytest1591  18921 Apr  1 15:29 README copy.md
-rw-r--r--   1 keytest1591  keytest1591  22674 Apr  1 15:36 README.md
-rw-r--r--   1 keytest1591  keytest1591     22 Apr  1 15:47 index.html
drwxr-xr-x   3 keytest1591  keytest1591     96 Apr  1 13:59 요구사항
keytest1591@c3r1s7 E1-1 % docker build -t my-web:1.0 .
[+] Building 8.2s (7/7) FINISHED                                                                                   docker:orbstack
 => [internal] load build definition from Dockerfile                                                                          0.1s
 => => transferring dockerfile: 104B                                                                                          0.0s
 => [internal] load metadata for docker.io/library/nginx:alpine                                                               2.7s
 => [internal] load .dockerignore                                                                                             0.2s
 => => transferring context: 2B                                                                                               0.0s
 => [internal] load build context                                                                                             0.3s
 => => transferring context: 59B                                                                                              0.0s
 => [1/2] FROM docker.io/library/nginx:alpine@sha256:e7257f1ef28ba17cf7c248cb8ccf6f0c6e0228ab9c315c152f9c203cd34cf6d1         4.3s
 => => resolve docker.io/library/nginx:alpine@sha256:e7257f1ef28ba17cf7c248cb8ccf6f0c6e0228ab9c315c152f9c203cd34cf6d1         0.3s
 => => sha256:7e89aa6cabfc80f566b1b77b981f4bb98413bd2d513ca9a30f63fe58b4af6903 2.50kB / 2.50kB                                0.0s
 => => sha256:91d1c9c22f2c631288354fadb2decc448ce151d7a197c167b206588e09dcd50a 626B / 626B                                    0.5s
 => => sha256:e7257f1ef28ba17cf7c248cb8ccf6f0c6e0228ab9c315c152f9c203cd34cf6d1 10.33kB / 10.33kB                              0.0s
 => => sha256:d5030d429039a823bef4164df2fad7a0defb8d00c98c1136aec06701871197c2 12.32kB / 12.32kB                              0.0s
 => => sha256:8892f80f46a05d59a4cde3bcbb1dd26ed2441d4214870a4a7b318eaa476a0a54 1.87MB / 1.87MB                                0.9s
 => => sha256:589002ba0eaed121a1dbf42f6648f29e5be55d5c8a6ee0f8eaa0285cc21ac153 3.86MB / 3.86MB                                0.8s
 => => sha256:cf1159c696ee2a72b85634360dbada071db61bceaad253db7fda65c45a58414c 953B / 953B                                    1.1s
 => => extracting sha256:589002ba0eaed121a1dbf42f6648f29e5be55d5c8a6ee0f8eaa0285cc21ac153                                     0.1s
 => => sha256:3f4ad4352d4f91018e2b4910b9db24c08e70192c3b75d0d6fff0120c838aa0bb 402B / 402B                                    1.3s
 => => extracting sha256:8892f80f46a05d59a4cde3bcbb1dd26ed2441d4214870a4a7b318eaa476a0a54                                     0.1s
 => => sha256:c2bd5ab177271dd59f19a46c214b1327f5c428cd075437ec0155ae71d0cdadc1 1.21kB / 1.21kB                                1.4s
 => => sha256:4d9d41f3822d171ccc5f2cdfd75ad846ac4c7ed1cd36fb998fe2c0ce4501647b 1.40kB / 1.40kB                                1.6s
 => => extracting sha256:91d1c9c22f2c631288354fadb2decc448ce151d7a197c167b206588e09dcd50a                                     0.0s
 => => extracting sha256:cf1159c696ee2a72b85634360dbada071db61bceaad253db7fda65c45a58414c                                     0.0s
 => => extracting sha256:3f4ad4352d4f91018e2b4910b9db24c08e70192c3b75d0d6fff0120c838aa0bb                                     0.0s
 => => sha256:3370263bc02adcf5c4f51831d2bf1d54dbf9a6a80b0bf32c5c9b9400630eaa08 20.25MB / 20.25MB                              2.4s
 => => extracting sha256:c2bd5ab177271dd59f19a46c214b1327f5c428cd075437ec0155ae71d0cdadc1                                     0.0s
 => => extracting sha256:4d9d41f3822d171ccc5f2cdfd75ad846ac4c7ed1cd36fb998fe2c0ce4501647b                                     0.0s
 => => extracting sha256:3370263bc02adcf5c4f51831d2bf1d54dbf9a6a80b0bf32c5c9b9400630eaa08                                     0.5s
 => [2/2] COPY index.html /usr/share/nginx/html/index.html                                                                    0.3s
 => exporting to image                                                                                                        0.2s
 => => exporting layers                                                                                                       0.1s
 => => writing image sha256:cef068316842e2722df2e73598590749dac25299aa2e8dd2fb62ab8b59dfea28                                  0.0s
 => => naming to docker.io/library/my-web:1.0                                                                                 0.0s
keytest1591@c3r1s7 E1-1 % 
keytest1591@c3r1s7 E1-1 % docker run -d -p 8080:80 --name my-web my-web:1.0
268883371e018f4f82fbf35a2a7c15ce3c02075e681efd712c27d57f01531141
keytest1591@c3r1s7 E1-1 % docker ps
CONTAINER ID   IMAGE        COMMAND                  CREATED          STATUS          PORTS                                     NAMES
268883371e01   my-web:1.0   "/docker-entrypoint.…"   13 seconds ago   Up 12 seconds   0.0.0.0:8080->80/tcp, [::]:8080->80/tcp   my-web
keytest1591@c3r1s7 E1-1 % docker logs my-web
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2026/04/01 06:48:47 [notice] 1#1: using the "epoll" event method
2026/04/01 06:48:47 [notice] 1#1: nginx/1.29.7
2026/04/01 06:48:47 [notice] 1#1: built by gcc 15.2.0 (Alpine 15.2.0) 
2026/04/01 06:48:47 [notice] 1#1: OS: Linux 6.17.8-orbstack-00308-g8f9c941121b1
2026/04/01 06:48:47 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 20480:1048576
2026/04/01 06:48:47 [notice] 1#1: start worker processes
2026/04/01 06:48:47 [notice] 1#1: start worker process 30
2026/04/01 06:48:47 [notice] 1#1: start worker process 31
2026/04/01 06:48:47 [notice] 1#1: start worker process 32
2026/04/01 06:48:47 [notice] 1#1: start worker process 33
2026/04/01 06:48:47 [notice] 1#1: start worker process 34
2026/04/01 06:48:47 [notice] 1#1: start worker process 35
keytest1591@c3r1s7 E1-1 % 

```

트러블슈팅:

### 사례 1. `Dockerfile: no such file or directory`

* 문제: `docker build -t my-web:1.0 .` 실행 시 `failed to read dockerfile: open Dockerfile: no such file or directory` 오류 발생
* 원인 가설: 현재 디렉토리에 `Dockerfile`이 없거나, `docker build`를 잘못된 위치에서 실행했을 가능성
* 확인:

```bash
pwd
ls -la
find . -maxdepth 2 -name Dockerfile
```

* 해결/대안:
  현재 디렉토리에서 빌드할 경우 `Dockerfile`을 직접 생성한 뒤 다시 빌드한다.

```bash
cat > Dockerfile <<'EOF'
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
EOF

cat > index.html <<'EOF'
<h1>Hello Docker</h1>
EOF

docker build -t my-web:1.0 .
```

## 7. 포트 매핑 검증

실습할 명령:

```bash
curl http://localhost:8080
```

실습:

```bash
keytest1591@c3r1s7 E1-1 % curl http://localhost:8080
<h1>Hello Docker</h1>
keytest1591@c3r1s7 E1-1 % 
```

확인 결과:

* 브라우저 증거를 사용할 경우 주소창과 포트 번호가 함께 보여야 한다.
* `docker run -d -p 8080:80 --name my-web my-web:1.0` 명령으로 호스트 `8080` 포트를 컨테이너 `80` 포트에 연결했다.
* `curl http://localhost:8080` 결과로 컨테이너 내부 `index.html` 응답을 확인했다.

## 8. Docker 볼륨 영속성 검증

실습할 명령:

```bash
docker volume create mydata
docker rm -f vol-test vol-test-2 2>/dev/null || true
docker run -d --name vol-test -v mydata:/data ubuntu sleep infinity
docker exec vol-test bash -lc "echo hi > /data/hello.txt && cat /data/hello.txt"
docker exec vol-test bash -lc "ls -l /data && cat /data/hello.txt"
docker rm -f vol-test
docker run -d --name vol-test-2 -v mydata:/data ubuntu sleep infinity
docker exec vol-test-2 bash -lc "ls -l /data && cat /data/hello.txt"
docker volume inspect mydata
docker rm -f vol-test-2
```

실습:

```bash
keytest1591@c3r1s7 E1-1 % 
keytest1591@c3r1s7 E1-1 % docker volume create mydata
mydata
keytest1591@c3r1s7 E1-1 % docker rm -f vol-test vol-test-2 2>/dev/null || true
vol-test
keytest1591@c3r1s7 E1-1 % docker run -d --name vol-test -v mydata:/data ubuntu sleep infinity
18258cafc03045e2f4e10538555f6b81a5f98a5bf063b4e40f33286b3358936d
keytest1591@c3r1s7 E1-1 % docker exec vol-test bash -lc "echo hi > /data/hello.txt && cat /data/hello.txt"
hi
keytest1591@c3r1s7 E1-1 % docker exec vol-test bash -lc "ls -l /data && cat /data/hello.txt"
total 4
-rw-r--r-- 1 root root 3 Apr  1 08:55 hello.txt
hi
keytest1591@c3r1s7 E1-1 % docker exec -it vol-test bash
root@18258cafc030:/# ls -la /data
total 4
drwxr-xr-x 1 root root 18 Apr  1 08:48 .
drwxr-xr-x 1 root root 14 Apr  1 08:55 ..
-rw-r--r-- 1 root root  3 Apr  1 08:55 hello.txt
root@18258cafc030:/# cat /data/hello.txt
hi
root@18258cafc030:/# exit
exit
keytest1591@c3r1s7 E1-1 % 
keytest1591@c3r1s7 E1-1 % 
keytest1591@c3r1s7 E1-1 % docker rm -f vol-test
vol-test
keytest1591@c3r1s7 E1-1 % docker run -d --name vol-test-2 -v mydata:/data ubuntu sleep infinity
b5e438d3856c3ba834fb1947d9143627ed8637112f70f5bf01bdc18b6af3a8ed
keytest1591@c3r1s7 E1-1 % docker exec vol-test-2 bash -lc "ls -l /data && cat /data/hello.txt"
total 4
-rw-r--r-- 1 root root 3 Apr  1 08:55 hello.txt
hi
keytest1591@c3r1s7 E1-1 % docker volume inspect mydata
[
    {
        "CreatedAt": "2026-04-01T17:46:27+09:00",
        "Driver": "local",
        "Labels": null,
        "Mountpoint": "/var/lib/docker/volumes/mydata/_data",
        "Name": "mydata",
        "Options": null,
        "Scope": "local"
    }
]
keytest1591@c3r1s7 E1-1 % docker rm -f vol-test-2
vol-test-2
keytest1591@c3r1s7 E1-1 % 


```

정리:
* 볼륨 생성 명령: `docker volume create mydata`
* 볼륨 연결 명령: `docker run -d --name vol-test -v mydata:/data ubuntu sleep infinity`
* 볼륨 검증 명령: `docker exec ... ls -l /data`, `docker exec ... cat /data/hello.txt`, `docker volume inspect mydata`
* 컨테이너 삭제 전 비교: `vol-test` 안에서 `/data/hello.txt`가 보이는지 확인
* 컨테이너 삭제 후 비교: `vol-test-2` 안에서도 같은 파일이 그대로 보이는지 확인
* `exec`는 실행 중인 컨테이너 안에서 새 명령을 여는 개념이다.
* 핵심 결론: 컨테이너를 삭제해도 볼륨 `mydata`가 유지되면 데이터는 사라지지 않는다.
  


## 9. Git 설정 및 GitHub/VSCode 연동

실습할 명령:

```bash
git config --global user.name
git config --global user.email
git config --global init.defaultBranch
git config --list | grep -E "user.name|user.email|remote.origin.url|branch.main"
git remote -v
```

실습:

```bash
***@*** E1-1 % git config --global user.name
zzxy72
***@*** E1-1 % git config --global user.email
k*****@naver.com
***@*** E1-1 % git config --global init.defaultBranch
***@*** E1-1 % git config --list | grep -E "user.name|user.email|remote.origin.url|branch.main"
user.name=zzxy72
user.email=k*****@naver.com
remote.origin.url=https://github.com/zzxy72/E1-1.git
branch.main.remote=origin
branch.main.merge=refs/heads/main
branch.main.vscode-merge-base=origin/main
***@*** E1-1 % git remote -v
origin  https://github.com/zzxy72/E1-1.git (fetch)
origin  https://github.com/zzxy72/E1-1.git (push)
```

확인 결과:

* Git 전역 사용자 정보는 `user.name`, `user.email` 값으로 확인했다.
* 현재 저장소는 `origin` 원격 저장소에 연결되어 있으며, 원격 주소는 `https://github.com/zzxy72/E1-1.git` 이다.
* VSCode 소스 제어 화면에서 `main` 브랜치와 `origin/main` 연결 상태를 추가로 확인했다.
* `git config --global init.defaultBranch` 는 별도 출력이 없었지만, 현재 저장소 기준 기본 작업 브랜치는 `main` 으로 확인된다.

## 10. 트러블슈팅

### 사례 1. `Dockerfile: no such file or directory`

* 문제: `docker build -t my-web:1.0 .` 실행 시 `failed to read dockerfile: open Dockerfile: no such file or directory` 오류가 발생했다.
* 원인 가설: 현재 디렉토리에 `Dockerfile` 이 없거나 잘못된 위치에서 빌드를 실행했을 가능성이 있었다.
* 확인 방법: `pwd`, `ls -la`, `find . -maxdepth 2 -name Dockerfile` 로 현재 위치와 파일 존재 여부를 점검했다.
* 해결 또는 대안: 현재 디렉토리에 `Dockerfile` 과 `index.html` 을 만든 뒤 다시 `docker build -t my-web:1.0 .` 를 실행해 이미지를 정상적으로 빌드했다.

### 사례 2. VSCode 커밋이 지연되는 것처럼 보인 경우

* 문제: VSCode에서 커밋 버튼을 눌렀는데 즉시 완료되지 않고 오래 걸리는 것처럼 보였다.
* 원인 가설: 커밋이 멈춘 것이 아니라 `.git/COMMIT_EDITMSG` 파일이 열리면서 커밋 메시지 입력을 기다리는 상태였다.
* 확인 방법: VSCode 편집 창에 `.git/COMMIT_EDITMSG` 탭이 열려 있고, 상단에 커밋 메시지를 입력하라는 안내 문구가 표시되는지 확인했다.
* 해결 또는 대안: 파일 첫 줄에 커밋 메시지를 입력한 뒤 저장하여 커밋을 완료했다. 이후에는 소스 제어 입력창에 메시지를 먼저 작성한 다음 `Commit` 버튼을 누르면 같은 상황을 줄일 수 있다.

## 11. 보안 점검

* 토큰, 비밀번호, 개인키, 인증 코드를 기록하지 않는다.
* 이메일 주소, 로컬 계정명, 호스트명은 필요 시 일부 마스킹해서 기록한다.
* 브라우저 캡처에는 주소창과 포트가 보이게 한다.
* 실제 실행한 로그만 기록한다.
