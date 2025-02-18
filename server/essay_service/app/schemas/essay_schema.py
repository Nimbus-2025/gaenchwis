from enum import Enum
from pydantic import BaseModel
from typing import List, Optional, TypedDict
from datetime import datetime

class EssayQuestion(BaseModel):
    essay_ask: str
    essay_content: Optional[str] = None

class EssayResponse(BaseModel):
    essay_id: str
    user_id: str
    essay_ask: str
    essay_content: Optional[str]
    created_at: datetime
    updated_at: datetime
    
class UpdateEssayRequest(BaseModel):
    essay_ask: Optional[str] = None
    essay_content: Optional[str] = None

class SortOrder(str, Enum):
    DESC = "desc"  # 최신순
    ASC = "asc"    # 오래된순

class EssayListItem(BaseModel):
    essay_id: str
    essay_ask: str
    created_at: str

class EssayListResponse(BaseModel):
    essays: List[EssayListItem]
    total_count: int
    current_page: int
    total_pages: int
    
class JobPosting(BaseModel):
    post_id: str
    company_name: str  
    post_name: str

class EssayDetailResponse(BaseModel):
    essay_id: str
    essay_ask: str
    essay_content: Optional[str]
    created_at: str
    updated_at: str
    related_job_postings: List[JobPosting]
    
class SearchType(str, Enum):
    QUESTION = "question"  # 문항 기반 검색
    CONTENT = "content"    # 내용 기반 검색

# DynamoDB 용 TypedDict 추가
class EssayJobPosting(TypedDict):
    PK: str               # ESSAY#<essay_id>
    SK: str               # POST#<post_id>
    essay_id: str         
    post_id: str         
    company_id: str       # 추가
    created_at: str       
    GSI1PK: str          
    GSI1SK: str          

class JobPostingLink(BaseModel):
    post_id: str
    company_id: str
    
class JobPostingInfo(BaseModel):
    post_id: str
    company_id: str
    
class CreateEssaysRequest(BaseModel):
    questions: List[EssayQuestion]
    job_postings: Optional[List[JobPostingInfo]] = None