# Minecraft RCON Web Controller

이 웹 애플리케이션은 Flask를 기반으로 하여 마인크래프트 서버에 RCON 명령을 보내고 웹 인터페이스에서 응답을 확인할 수 있게 해줍니다. 애플리케이션은 사용자 인증을 지원하여 권한이 있는 사용자만 서버에 명령을 보낼 수 있도록 합니다.

## 기능

- 해시된 비밀번호를 사용한 사용자 인증
- 마인크래프트 서버에 RCON 명령 전송
- 마인크래프트 형식을 HTML로 변환하여 응답 보기
- 간단하고 직관적인 웹 인터페이스

## 요구 사항

- Python 3.6+
- Flask
- python-dotenv
- werkzeug
- mcrcon

## 설치

1. 저장소를 클론합니다:
    ```sh
    git clone https://github.com/suzukaotto/minecraft-rcon-web-controller.git
    cd minecraft-rcon-web-controller
    ```

2. 필요한 Python 패키지를 설치합니다:
    ```sh
    pip install -r requirements.txt
    ```

3. 프로젝트의 루트 디렉토리에 `.env` 파일을 생성하고 다음 환경 변수를 추가합니다:
    ```env
    SERVER_IP=127.0.0.1
    SERVER_PORT=5000
    RCON_IP=127.0.0.1
    RCON_PORT=25575
    RCON_PASSWORD=your_rcon_password
    ADMIN_USERNAME=admin
    ADMIN_PASSWORD_HASH=your_admin_password
    ```

4. 애플리케이션을 실행합니다:
    ```sh
    python app.py
    ```

## 사용법

1. 웹 브라우저를 열고 `http://<SERVER_IP>:<SERVER_PORT>/login`으로 이동합니다.
2. `.env` 파일에 지정된 자격 증명을 사용하여 로그인합니다.
3. 로그인 후, 마인크래프트 서버에 RCON 명령을 보낼 수 있는 메인 페이지로 리디렉션됩니다.
4. 입력 필드에 명령을 입력하고 "Send" 버튼을 클릭합니다. 서버로부터의 응답이 입력 필드 아래에 표시됩니다.

## 코드 개요

### 주요 구성 요소

- `app.py`: Flask 앱, 라우트 및 기능을 설정하는 메인 애플리케이션 파일.
- `templates/`: 로그인 및 메인 페이지에 대한 HTML 템플릿을 포함하는 디렉토리.
- `static/`: CSS 및 JavaScript와 같은 정적 파일을 위한 디렉토리.

### 주요 함수

- `minecraft_to_html(text)`: 마인크래프트 형식 코드를 HTML 스타일로 변환합니다.
- `send_rcon_command(command)`: 마인크래프트 서버에 RCON 명령을 보내고 응답을 반환합니다.
- `login_required(f)`: 라우트가 로그인된 사용자만 접근할 수 있도록 하는 데코레이터.

### 라우트

- `/login`: 사용자 로그인을 처리합니다. GET 및 POST 메서드를 지원합니다.
- `/logout`: 사용자를 로그아웃하고 로그인 페이지로 리디렉션합니다.
- `/`: 사용자가 RCON 명령을 보낼 수 있는 메인 페이지입니다. GET 및 POST 메서드를 지원합니다.

## 라이선스

이 프로젝트는 MIT 라이선스에 따라 라이선스가 부여됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하십시오.
