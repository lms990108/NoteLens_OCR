# 베이스 이미지 지정
FROM python:3.8-slim

# 작업 디렉토리 설정
WORKDIR /app

# 현재 디렉토리의 모든 파일을 컨테이너의 /app으로 복사
COPY . /app

# 스크립트 파일에 실행 권한 부여
RUN chmod +x run_server.sh

# 필요한 파이썬 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 외부로 노출할 포트 지정
EXPOSE 8000

# 컨테이너 실행 시 기본 명령 지정
CMD ["/bin/bash", "./run_server.sh"]
