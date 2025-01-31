from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime
from enum import Enum

# 일정 생성을 위한 스키마 (유지)
class GeneralScheduleCreate(BaseModel):
    title: str
    date: str  # YYYY-MM-DD 형식
    content: Optional[str] = None

    @validator('date')
    def validate_date_format(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v.replace('-', '')  # YYYYMMDD 형식으로 변환
        except ValueError:
            raise ValueError('날짜는 YYYY-MM-DD 형식이어야 합니다')

    class Config:
        json_schema_extra = {
            "example": {
                "title": "팀 미팅",
                "date": "2024-03-15",
                "content": "프로젝트 진행 상황 공유"
            }
        }

# 일정 조회를 위한 새로운 스키마 (추가)
class ScheduleType(str, Enum):
    ALL = "all"          # 모든 일정
    GENERAL = "general"  # 일반 일정
    APPLY = "apply"      # 취업 일정

class ScheduleResponse(BaseModel):
    schedule_type: Optional[str]
    schedule_id: str
    schedule_title: str
    schedule_date: Optional[str]
    schedule_content: Optional[str]
    is_completed: bool = False  # 완료 상태 필드 추가
    schedule_deadline: Optional[str]
    document_result_date: Optional[str]
    interview_date: Optional[str]
    final_date: Optional[str]

# 일정 상세 조회 응답을 위한 스키마 추가
class ScheduleDetailResponse(BaseModel):
    title: str
    date: str
    content: Optional[str] = None 
    schedule_type: str
    is_completed: bool = False
    # 공고 일정일 경우 추가 필드
    company_name: Optional[str] = None
    position_name: Optional[str] = None  # 공고명
    memo: Optional[str] = None  # 기타 내용(메모)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "팀 미팅",
                "date": "20240315",
                "content": "프로젝트 진행 상황 공유"
            }
        }

class GeneralScheduleUpdate(BaseModel):
    type: Optional[str] = None 
    title: str
    date: Optional[str] = None 
    content: Optional[str] = None 
    company: Optional[str] = None 
    deadlineDate: Optional[str] = None 
    interviewDate: Optional[str] = None 
    documentResultDate: Optional[str] = None 
    finalDate: Optional[str] = None 
