import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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

required_env_vars = [
    'AWS_REGION',
    'COGNITO_USER_POOL_ID',
    'COGNITO_APP_CLIENT_ID',
    'AWS_ACCESS_KEY_ID',
    'AWS_SECRET_ACCESS_KEY'
]

missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    logger.error(f"Missing required environment variables: {missing_vars}")
    raise RuntimeError(f"Missing required environment variables: {missing_vars}")

logger.info("All required environment variables are present")

app = FastAPI(
    title="User Service",
    description="유저 관리 서비스"
)

# 에러 핸들러 등록
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "detail": exc.detail
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"General Exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "detail": "Internal server error",
            "message": str(exc) if os.getenv('DEBUG') == 'True' else "An unexpected error occurred"
        }
    )

# 프로덕션 환경에서는 구체적인 origin 지정
# origins = [
#     "http://localhost:3000",
#     "https://gaenchwis.com"
# ]

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "access_token",
        "id_token",
        "user_id"
    ]
)

app.include_router(router, prefix="/api/v1", tags=["user"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",  host="0.0.0.0", port=8000, reload=True, log_level="info")