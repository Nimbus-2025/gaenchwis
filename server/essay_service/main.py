import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.routes.essay_routes import router

load_dotenv()

app = FastAPI(
    title="Essay Service",
    description="자기소개서 관리 서비스"
)

app.include_router(router, prefix="/api/v1", tags=["essays"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)