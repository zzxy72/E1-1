# AI/SW 개발 워크스테이션 구축

## 프로젝트 개요

이 문서는 터미널, Docker, Git/GitHub를 이용해 개발 워크스테이션을 구축하고 검증한 결과를 정리한 README다.  
과제 요구사항에 맞춰 필요한 실습만 기록하며, `실습 후 교체` 구간은 실제 실행 로그로 바꿔 작성한다.

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
| GitHub 연동 방식 | `HTTPS 또는 SSH로 실습 후 교체` |

실습 후 교체:

```bash
sw_vers
echo $SHELL
echo $TERM_PROGRAM
docker --version
git --version
```

## 수행 체크리스트

* [x] 터미널 기본 조작 수행
* [ ] 파일 권한 변경 실습
* [ ] 디렉토리 권한 변경 실습
* [ ] Docker 설치 및 점검
* [ ] Docker 기본 운영 명령 수행
* [ ] `hello-world` 실행
* [ ] `ubuntu` 컨테이너 내부 진입
* [ ] Dockerfile 기반 커스텀 이미지 빌드 및 실행
* [ ] 포트 매핑 접속 확인
* [ ] Docker 볼륨 영속성 검증
* [ ] Git 설정 및 GitHub 연동
* [ ] 트러블슈팅 2건 이상 정리

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

실습 후 교체:

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

실습 후 교체:

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

해설:

* 파일 1개와 디렉토리 1개 모두 전후 비교가 보여야 한다.
* `755`는 디렉토리 예시, `644`는 파일 예시로 쓰기 좋다.

## 3. Docker 설치 및 점검

실습할 명령:

```bash
docker --version
docker info
```

실습 후 교체:

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

실습 후 교체:

```bash
# 여기에 실제 명령과 출력 결과를 붙여넣는다.
```

해설:

* `hello-world`는 Docker 공식 테스트용 이미지다.
* `docker ps`는 실행 중 컨테이너만 보여준다.
* `hello-world`는 실행 후 바로 종료되므로 `docker ps`에는 안 보일 수 있다.
* 종료된 컨테이너는 `docker ps -a`에서, 출력 내용은 `docker logs hello-test`에서 확인한다.

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

실습 후 교체:

```bash
# 여기에 실제 로그를 붙여넣는다.
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

실습 후 교체:

```bash
# 여기에 실제 로그를 붙여넣는다.
```

간단 정리:

* `attach`는 메인 프로세스에 연결하는 개념이다.
* `exec`는 실행 중인 컨테이너 안에서 새 명령을 여는 개념이다.

## 6. Dockerfile 기반 커스텀 이미지 제작

실습 후 작성:

* 베이스 이미지: `실습 후 교체`
* 선택 이유: `실습 후 교체`
* 커스텀 포인트: `실습 후 교체`
* 목적: `실습 후 교체`

실습할 명령:

```bash
docker rm -f my-web 2>/dev/null || true
docker build -t my-web:1.0 .
docker run -d -p 8080:80 --name my-web my-web:1.0
docker ps
docker logs my-web
```

실습 후 교체:

```bash
# 여기에 실제 빌드/실행 로그를 붙여넣는다.
```

## 7. 포트 매핑 검증

실습할 명령:

```bash
curl http://localhost:8080
```

실습 후 교체:

```bash
# 여기에 curl 응답 또는 브라우저 접속 증거 설명을 붙여넣는다.
```

해설:

* 브라우저 증거를 사용할 경우 주소창과 포트 번호가 함께 보여야 한다.

## 8. Docker 볼륨 영속성 검증

실습할 명령:

```bash
docker volume create mydata
docker rm -f vol-test vol-test-2 2>/dev/null || true
docker run -d --name vol-test -v mydata:/data ubuntu sleep infinity
docker exec vol-test bash -lc "echo hi > /data/hello.txt && cat /data/hello.txt"
docker rm -f vol-test
docker run -d --name vol-test-2 -v mydata:/data ubuntu sleep infinity
docker exec vol-test-2 bash -lc "cat /data/hello.txt"
```

실습 후 교체:

```bash
# 여기에 실제 영속성 검증 로그를 붙여넣는다.
```

## 9. Git 설정 및 GitHub 연동

실습할 명령:

```bash
git config --global user.name
git config --global user.email
git config --global init.defaultBranch
git config --list
git remote -v
```

실습 후 교체:

```bash
# 여기에 실제 출력 결과를 붙여넣는다.
# 민감정보가 있다면 마스킹한다.
```

추가 첨부:

* VSCode GitHub 로그인 화면 또는 저장소 연동 화면

## 10. 트러블슈팅

### 사례 1

* 문제: `실습 후 교체`
* 원인 가설: `실습 후 교체`
* 확인 방법: `실습 후 교체`
* 해결 또는 대안: `실습 후 교체`

### 사례 2

* 문제: `실습 후 교체`
* 원인 가설: `실습 후 교체`
* 확인 방법: `실습 후 교체`
* 해결 또는 대안: `실습 후 교체`

## 11. 보안 점검

* 토큰, 비밀번호, 개인키, 인증 코드를 기록하지 않는다.
* 브라우저 캡처에는 주소창과 포트가 보이게 한다.
* 실제 실행한 로그만 기록한다.
