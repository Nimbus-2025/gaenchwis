from fastapi import APIRouter, HTTPException
import logging
from ..schemas.essay_schema import CreateScheduleRequest, ScheduleResponse
from ..repositories.schedule_repository import ScheduleRepository
from typing import List

router = APIRouter()
schedule_repository = ScheduleRepository()

@router.get("/healthcheck")
async def healthcheck():
    return {"status": "healthy"}

@router.get("/schedules/{user_id}", response_model=List[ScheduleResponse])
async def get_schedules(user_id: str):
    try:
        schedules = await schedule_repository.get_schedules_by_user(user_id)
        return schedules
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get schedules: {str(e)}"
        )

@router.post("/schedules", response_model=dict)
async def create_schedule(request: CreateScheduleRequest):
    try:
        schedule_id = await schedule_repository.create_schedule(request)
        return {
            "message": "일정이 성공적으로 저장되었습니다",
            "schedule_id": schedule_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create schedule: {str(e)}"
        )