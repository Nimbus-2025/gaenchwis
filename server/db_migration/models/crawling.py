from typing import TypedDict, Optional
from typing import TypedDict, Optional
from datetime import datetime
from constants.status import JobStatus
from constants.category import TagCategory

class Company(TypedDict):
    # Primary Key
    PK: str                # COMPANY#<company_id>
    SK: str                # METADATA#<company_id>
    
    # Attributes
    company_id: str         # company_id
    company_name: str       # 회사명
    company_id: str         # company_id
    company_name: str       # 회사명
    created_at: datetime  
    updated_at: datetime       
    
    # GSI Keys: CompanyNameIndex
    GSI1PK: str           # COMPANY#ALL
    GSI1SK: str           # <company_name>

class JobPosting(TypedDict):
    # Primary Key
    PK: str               # COMPANY#<company_id>
    SK: str               # JOB#<post_id>
    
    # Attributes
    post_id: str          # post_id
    post_name: str        # 공고명
    company_id: str       # company_id 
    company_name: str     # 회사명
    deadline: datetime    # 공고 마감일  
    post_url: str         # 공고 URL
    rec_idx: str           # 공고 URL의 식별 값
    status: JobStatus     # 공고 상태 (active / inactive)
    post_id: str          # post_id
    post_name: str        # 공고명
    company_id: str       # company_id 
    company_name: str     # 회사명
    deadline: datetime    # 공고 마감일  
    post_url: str         # 공고 URL
    rec_idx: str           # 공고 URL의 식별 값
    status: JobStatus     # 공고 상태 (active / inactive)
    created_at: datetime  
    updated_at: datetime  
    
    # GSI Keys: StatusIndex
    GSI1PK: str          # STATUS#<status>
    GSI1SK: str          # <created_at>
    GSI2PK: str          # JOB#ALL
    GSI2SK: str          # <updated_at>
    # RecIdx
    rec_idx: str         # rec_idx for PostId GSI
    # JobPostId
    post_id: str         # post_id for JobPostId GSI
    
class Tag(TypedDict):
    # Primary Key
    PK: str               # TAG#<tag_id>       # tag_id가 PK
    SK: str               # TAG#<category>      # category가 SK 
    
    # Attributes
    tag_id: str                 # tag_id
    tag_category: TagCategory   # 태그 카테고리 (location, skill, position, education)
    tag_name: str               # 태그명
    parent_id: Optional[str]    # 지역 레벨 1의 id값 
    tag_level: int              # 지역 레벨 (1-전체구역, 2-시/군/구)
    created_at: datetime  
    updated_at: datetime  
    
    # GSI Keys: TagCategoryNameIndex
    GSI1PK: str          # TAG#<category> # 예: TAG#position
    GSI1SK: str          # <tag_name>     # 예: 신입 

class JobTag(TypedDict):
    # Primary Key
    PK: str               # JOB#<job_id>
    SK: str               # TAG#<tag_id>
    
    # Attributes
    job_tag_id: str       
    job_id: str           
    tag_id: str           
    created_at: datetime  
    
    # GSI Keys: JobTagInverseIndex
    GSI1PK: str          # TAG#<tag_id>
    GSI1SK: str          # JOB#<job_id>