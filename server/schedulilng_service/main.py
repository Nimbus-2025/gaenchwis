import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.routes.schedule_routes import router

load_dotenv()

app = FastAPI(
    title="scheduling Service",
    description="일정 관리 서비스"
)

app.include_router(router, prefix="/api/v1", tags=["schedules"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)