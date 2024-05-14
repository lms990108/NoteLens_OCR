# 베이스 이미지 지정
FROM python:3.8-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필수 패키지 설치 및 제거
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && pip install paddlepaddle==2.6.1 -i https://mirror.baidu.com/pypi/simple \
    && pip install "paddleocr>=2.0.1" fastapi "uvicorn[standard]" \
    && apt-get remove -y gcc python3-dev \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 현재 디렉토리의 모든 파일을 컨테이너의 /app으로 복사
COPY . /app

# 스크립트 파일에 실행 권한 부여
RUN chmod +x run_prod_server.sh

# 외부로 노출할 포트 지정
EXPOSE 8000

# 컨테이너 실행 시 기본 명령 지정
CMD ["/bin/bash", "./run_prod_server.sh"]
