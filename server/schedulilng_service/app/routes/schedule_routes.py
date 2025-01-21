from fastapi import APIRouter, Header, Depends, HTTPException, Body, Query
from typing import List, Dict, Optional
from pydantic import BaseModel
import logging
from ..schemas.scheduling_schema import GeneralScheduleCreate, ScheduleResponse, ScheduleType, ScheduleDetailResponse, GeneralScheduleUpdate
from ..repositories.schedule_repository import ScheduleRepository
from datetime import datetime

router = APIRouter()
schedule_repository = ScheduleRepository()

class ScheduleCreateResponse(BaseModel):
    message: str
    schedule_id: str

def get_user_tokens(
    access_token: Optional[str] = Header(None, alias="access_token", convert_underscores=False),
    id_token: Optional[str] = Header(None, alias="id_token", convert_underscores=False),
    user_id: Optional[str] = Header(None, alias="user_id", convert_underscores=False)
) -> Dict[str, str]:
    if not access_token or not id_token or not user_id:
        raise HTTPException(status_code=401, detail="Authentication tokens required")
    logging.info("토큰 검증 완료")
    return {"access_token": access_token, "id_token": id_token, "user_id": user_id}

@router.post("/schedules", response_model=ScheduleCreateResponse)
def create_schedule(
    request: GeneralScheduleCreate,
    tokens: Dict = Depends(get_user_tokens)
):
    try:
        schedule_id = schedule_repository.create_general_schedule(tokens["user_id"], request)
        return ScheduleCreateResponse(
            message="일정이 성공적으로 저장되었습니다",
            schedule_id=schedule_id
        )
    except Exception as e:
        logging.error(f"Error creating schedule: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/schedules", response_model=List[ScheduleResponse])
def get_schedules(
    schedule_type: str = Query("all", description="조회할 일정 유형 (all/general/apply)"),
    year_month: str = Query(
        default=datetime.now().strftime("%Y-%m"),
        description="조회할 연월 (YYYY-MM)"
    ),
    tokens: Dict = Depends(get_user_tokens)
):
    """
    일정을 조회합니다.
    - all: 모든 일정
    - general: 일반 일정만
    - apply: 취업 일정만
    """
    try:
        user_id = tokens["user_id"]
        print(f"user_id: {user_id}")
        logging.info(f"Requesting schedules for user {user_id} with type {schedule_type} for {year_month}")
        
        if schedule_type not in ["all", "general", "apply"]:
            raise HTTPException(status_code=400, detail="Invalid schedule type")
        
        print(f"before get_schedules: {schedule_type}, {year_month}")
            
        schedules = schedule_repository.get_schedules(user_id, schedule_type, year_month)
        return schedules
            
    except Exception as e:
        logging.error(f"Error getting schedules: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# TODO: 일정 상세 조회 API 구현 예정
@router.get("/schedules/{schedule_id}", response_model=ScheduleDetailResponse)
def get_schedule_detail(
    schedule_id: str,
    tokens: Dict = Depends(get_user_tokens)
):
    """
    특정 일정의 상세 정보를 조회합니다.
    """
    try:
        schedule = schedule_repository.get_schedule_detail(
            user_id=tokens["user_id"],
            schedule_id=schedule_id
        )
        return schedule
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Error getting schedule detail: {str(e)}")
        raise HTTPException(status_code=500, detail="일정 조회 중 오류가 발생했습니다")

@router.put("/schedules/{schedule_id}", response_model=Dict)
def update_schedule(
    schedule_id: str,
    request: GeneralScheduleUpdate,
    tokens: Dict = Depends(get_user_tokens)
):
    """일정을 수정합니다."""
    try:
        success = schedule_repository.update_general_schedule(
            user_id=tokens["user_id"],
            schedule_id=schedule_id,
            request=request.dict()
        )
        
        if success:
            return {"message": "일정이 성공적으로 수정되었습니다"}
        else:
            raise HTTPException(status_code=404, detail="일정을 찾을 수 없습니다")
            
    except Exception as e:
        logging.error(f"Error updating schedule: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/schedules/{schedule_id}", response_model=Dict)
def delete_schedule(
    schedule_id: str,
    tokens: Dict = Depends(get_user_tokens)
):
    """일반 일정을 삭제합니다."""
    try:
        success = schedule_repository.delete_general_schedule(
            user_id=tokens["user_id"],
            schedule_id=schedule_id
        )
        
        if success:
            return {"message": "일정이 성공적으로 삭제되었습니다"}
            
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Error deleting schedule: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/schedules/{schedule_id}/toggle-completion", response_model=Dict)
def toggle_schedule_completion(
    schedule_id: str,
    tokens: Dict = Depends(get_user_tokens)
):
    """일정의 완료 상태를 토글합니다."""
    try:
        is_completed = schedule_repository.toggle_schedule_completion(
            user_id=tokens["user_id"],
            schedule_id=schedule_id
        )
        
        return {
            "message": "일정 완료 상태가 변경되었습니다",
            "is_completed": is_completed
        }
            
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Error toggling schedule completion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))