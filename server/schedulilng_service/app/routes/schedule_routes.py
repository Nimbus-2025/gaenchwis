from fastapi import APIRouter, Header, Depends, HTTPException, Body, Query
from typing import List, Dict
from pydantic import BaseModel
import logging
from ..schemas.scheduling_schema import GeneralScheduleCreate, ScheduleResponse, ScheduleType, ScheduleDetailResponse, GeneralScheduleUpdate
from ..repositories.schedule_repository import ScheduleRepository

router = APIRouter()
schedule_repository = ScheduleRepository()

class ScheduleCreateResponse(BaseModel):
    message: str
    schedule_id: str

def get_user_tokens(
    access_token: str | None = Header(None, alias="access_token", convert_underscores=False),
    id_token: str | None = Header(None, alias="id_token", convert_underscores=False),
    user_id: str | None = Header(None, alias="user_id", convert_underscores=False)
) -> Dict[str, str]:
    if not access_token or not id_token or not user_id:
        raise HTTPException(status_code=401, detail="Authentication tokens required")
    logging.info("토큰 검증 완료")
    return {"access_token": access_token, "id_token": id_token, "user_id": user_id}

@router.post("/schedules", response_model=ScheduleCreateResponse)
async def create_schedule(
    request: GeneralScheduleCreate,
    tokens: Dict = Depends(get_user_tokens)
):
    try:
        schedule_id = await schedule_repository.create_general_schedule(tokens["user_id"], request)
        return ScheduleCreateResponse(
            message="일정이 성공적으로 저장되었습니다",
            schedule_id=schedule_id
        )
    except Exception as e:
        logging.error(f"Error creating schedule: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/schedules", response_model=List[ScheduleResponse])
async def get_schedules(
    schedule_type: ScheduleType = Query(ScheduleType.ALL, description="조회할 일정 유형"),
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
        logging.info(f"Requesting schedules for user {user_id} with type {schedule_type}")
        
        # 현재는 일반 일정만 조회 가능
        if schedule_type == ScheduleType.GENERAL:
            schedules = await schedule_repository.get_general_schedules(user_id)
        else:
            # TODO: 다른 타입 조회는 나중에 구현
            schedules = []
            
        return schedules

        # TODO: 아래 코드는 나중에 구현 예정
        # if schedule_type == ScheduleType.ALL:
        #     schedules = await schedule_repository.get_all_schedules(user_id)
        # elif schedule_type == ScheduleType.GENERAL:
        #     schedules = await schedule_repository.get_general_schedules(user_id)
        # else:  # ScheduleType.APPLY
        #     schedules = await schedule_repository.apply_repository.get_apply_schedules(user_id)
            
        # return schedules
            
    except Exception as e:
        logging.error(f"Error getting schedules: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# TODO: 일정 상세 조회 API 구현 예정
@router.get("/schedules/{schedule_id}", response_model=ScheduleDetailResponse)
async def get_schedule_detail(
    schedule_id: str,
    tokens: Dict = Depends(get_user_tokens)
):
    """
    특정 일정의 상세 정보를 조회합니다.
    """
    try:
        schedule = await schedule_repository.get_schedule_detail(
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
async def update_schedule(
    schedule_id: str,
    request: GeneralScheduleUpdate,
    tokens: Dict = Depends(get_user_tokens)
):
    """일정을 수정합니다."""
    try:
        success = await schedule_repository.update_general_schedule(
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