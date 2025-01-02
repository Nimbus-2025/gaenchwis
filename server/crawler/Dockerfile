# Python 3.9 이미지를 기반으로 설정
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# Chrome 설치 전에 필요한 패키지  추가 
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

# # Chrome 설치 부분 수정
# RUN apt-get update && apt-get install -y \
#     wget \
#     gnupg \
#     unzip \
#     curl \
#     && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
#     && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
#     && apt-get update \
#     && apt-get install -y ${CHROME_VERSION} \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*
    
# # Chrome WebDriver 설치 
# RUN CHROME_DRIVER_VERSION=$(curl -sS "https://chromedriver.storage.googleapis.com/LATEST_RELEASE") \
#     && wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip" \
#     && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
#     && rm /tmp/chromedriver.zip \ 
#     && chmod +x /usr/local/bin/chromedriver

# 필요한 Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 환경 변수 설정
ENV PORT=8000
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV FLASK_APP=main.py
ENV PYTHONUNBUFFERED=1
ENV DOCKER_CONTAINER=true
ENV CHROMEDRIVER_DIR=/usr/local/bin/chromedriver
ENV CHROME_PATH=/usr/bin/google-chrome
# ENV CHROME_VERSION="google-chrome-stable"

# 볼륨 마운트를 위한 디렉토리 생성 및 권한 설정
RUN mkdir -p /app/output && chmod -R 755 /app
VOLUME ["/app/output"]

# 포트 설정
EXPOSE ${PORT}

# 컨테이너 실행 시 서버 모드로 실행 
ENTRYPOINT ["python", "main.py", "--server"]