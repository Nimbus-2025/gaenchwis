from enum import Enum
from datetime import datetime
from typing import Optional, TypedDict
from pydantic import BaseModel, Field

class ApplyCreate(BaseModel):
    post_id: str
    post_name: str
    
class ApplyResponse(BaseModel):
    user_id: str
    post_id: str
    post_name: str
    apply_date: datetime = Field(alias='GSI1SK')
    deadline_date: Optional[datetime] = None
    document_result_date: Optional[datetime] = None
    interview_date: Optional[datetime] = None
    final_date: Optional[datetime] = None
    memo: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True
        
class ApplyUpdate(BaseModel):
    document_result_date: Optional[datetime] = None
    interview_date: Optional[datetime] = None
    final_date: Optional[datetime] = None
    memo: Optional[str] = None
    
class ApplyDetailResponse(BaseModel):
    post_name: str
    apply_date: datetime = Field(alias='GSI1SK')
    deadline_date: Optional[datetime] = None
    document_result_date: Optional[datetime] = None
    interview_date: Optional[datetime] = None
    final_date: Optional[datetime] = None
    memo: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True
        
class EssayResponse(BaseModel):
    essay_id: str
    essay_ask: str
    essay_content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EssayJobPostingResponse(BaseModel):
    essays: list[EssayResponse]

    class Config:
        from_attributes = True
        
class BookmarkCreate(BaseModel):
    post_id: str
    post_name: str

class BookmarkCreateResponse(BaseModel):
    user_id: str
    post_id: str
    post_name: str
    created_at: datetime

    class Config:
        from_attributes = True

class BookmarkResponse(BaseModel):
    user_id: str
    post_id: str
    post_name: str
    company_name: str 
    tags: list[str] 
    created_at: datetime
    post_url: str

    class Config:
        from_attributes = True
        
class InterestCompanyCreate(BaseModel):
    company_id: str
    company_name: str

class InterestCompanyCreateResponse(BaseModel):
    user_id: str
    company_id: str
    company_name: str
    created_at: datetime

    class Config:
        from_attributes = True

class JobPostingInfo(BaseModel):
    post_id: str
    title: str
    deadline: str
    tags: list[str]
    post_url: str

class InterestCompanyResponse(BaseModel):
    user_id: str
    company_id: str
    company_name: str
    created_at: datetime
    job_postings: list[JobPostingInfo]
    has_active_postings: bool
    active_postings_count: int
    tags: list[str]

    class Config:
        from_attributes = True
        
class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

class SearchType(str, Enum):
    QUESTION = "question"
    CONTENT = "content"

class EssayJobPosting(TypedDict):
    PK: str
    SK: str
    GSI1PK: str
    GSI1SK: str
    essay_id: str
    post_id: str
    company_id: str
    created_at: str

class JobPostingLink(TypedDict):
    post_id: str
    company_id: str