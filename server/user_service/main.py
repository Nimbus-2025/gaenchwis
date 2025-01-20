import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from app.routes.user_routes import router
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# .env 파일 로드
env_path = Path(__file__).parent.parent / '.env'
logger.info(f"Loading .env from: {env_path}")
logger.info(f"File exists: {env_path.exists()}")

load_dotenv(dotenv_path=env_path)

# 환경변수 로드 확인
logger.info(f"AWS_ACCESS_KEY_ID exists: {bool(os.getenv('AWS_ACCESS_KEY_ID'))}")
logger.info(f"AWS_REGION: {os.getenv('AWS_REGION')}")


app = FastAPI(
    title="User Service",
    description="유저 관리 서비스"
)

app.include_router(router, prefix="/api/v1", tags=["user"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",  host="0.0.0.0", port=8000, reload=True)