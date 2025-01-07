FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# Chrome 관련 설치
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    chromium-driver \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 전체 소스코드 복사
COPY . .

# requirements.txt 경로 확인 후 패키지 설치
RUN ls -la /app/crawler/  # 디버깅을 위한 파일 목록 출력
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/crawler/requirements.txt  # 전체 경로 지정

# 환경 변수 설정
ENV PORT=8000
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV FLASK_APP=crawler/main.py
ENV PYTHONUNBUFFERED=1
ENV DOCKER_CONTAINER=true
ENV CHROMEDRIVER_DIR=/usr/local/bin/chromedriver
ENV CHROME_PATH=/usr/bin/google-chrome

# 볼륨 마운트를 위한 디렉토리 생성 및 권한 설정
RUN mkdir -p /app/crawler/output && chmod -R 755 /app
VOLUME ["/app/crawler/output"]

# 포트 설정
EXPOSE ${PORT}

# 컨테이너 실행 시 서버 모드로 실행 
WORKDIR /app/crawler
ENTRYPOINT ["python", "main.py", "--server"]