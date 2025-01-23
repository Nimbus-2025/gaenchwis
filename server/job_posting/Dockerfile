# Python 3.9 이미지를 베이스로 사용
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치
COPY requirements.txt .
COPY .env /app/.env
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 복사
COPY . .

# Flask 애플리케이션 실행
CMD ["python", "fetch_jobs.py"]