import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.routes.user_routes import router
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

load_dotenv()

app = FastAPI(
    title="User Service",
    description="유저 관리 서비스"
)

app.include_router(router, prefix="/api/v1", tags=["user"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",  host="0.0.0.0", port=8000, reload=True)