FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app/crawler

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

# 필요한 디렉토리 생성
RUN mkdir -p output logs

# requirements.txt 먼저 복사
COPY requirements.txt .

# requirements.txt 경로 확인 후 패키지 설치
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt  

# 전체 소스코드 복사
COPY . .

# Python 패키지 구조 설정
RUN touch __init__.py \
    && mkdir -p base crawlers common \
    && touch base/__init__.py crawlers/__init__.py common/__init__.py

# 환경 변수 설정
ENV PORT=8000
ENV FLASK_ENV=production
ENV PYTHONPATH=/app/crawler
ENV FLASK_APP=main.py
ENV AWS_REGION=ap-northeast-2
ENV PYTHONUNBUFFERED=1
ENV DOCKER_CONTAINER=true
ENV CHROMEDRIVER_DIR=/usr/local/bin/chromedriver
ENV CHROME_PATH=/usr/bin/google-chrome

# 볼륨 마운트를 위한 디렉토리 생성 및 권한 설정
RUN chmod -R 755 /app
VOLUME ["/app/crawler/output", "/app/crawler/logs"]

# 포트 설정
EXPOSE ${PORT}

# 컨테이너 실행 시 서버 모드로 실행 
ENTRYPOINT ["python", "main.py", "--server"]