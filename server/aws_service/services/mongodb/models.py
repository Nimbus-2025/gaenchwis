from typing import TypedDict, List, Optional
from datetime import datetime
from ..common.enums import JobStatus, TagCategory

class Company(TypedDict):
    # 기업 정보
    company_id: str         # 기업 고유 ID
    company_name: str       # 기업명
    created_at: datetime    # 생성일
    updated_at: datetime    # 수정일
    
class JobPosting(TypedDict):
    # 채용 공고 정보
    post_id: str            # 공고 고유 ID
    post_name: str          # 공고 제목
    company_id: str         # 기업 ID
    company_name: str       # 기업명   
    is_closed: datetime     # 마감일
    post_url: str           # 공고 URL
    status: JobStatus       # 상태 (active/inactive) 
    created_at: datetime    # 생성일
    updated_at: datetime    # 수정일
    tags: List[str]         # 태그 목록 
    
class Tag(TypedDict):
    # 태그 정보
    tag_id: str             # 태그 고유 ID
    category: TagCategory   # 태그 카테고리 
    name: str               # 태그명
    parent_id: Optional[str]    # 지역  태그의 경우 상위 지역 태그 ID
    level: int              # 계층 레벨 (시/도: 1, 구: 2)
    count: int              # 사용 횟수
    created_at: datetime    # 생성일 
    updated_at: datetime    # 수정일  
    
class JobTag(TypedDict):
    # 공고-태그 매핑
    job_tag_id: str         # 복합키(job_id#tag_id)  
    job_id: str             # 공고 ID
    tag_id: str             # 태그 ID
    created_at: datetime    # 생성일 