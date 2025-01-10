from typing import TypedDict, List, Optional
from datetime import datetime
from ..common.enums import JobStatus, TagCategory
from dataclasses import dataclass

@dataclass
class Company(TypedDict):
    PK: str                # COMPANY#<company_id>
    SK: str                # METADATA#<company_id>
    company_id: str        
    company_name: str
    created_at: datetime  
    updated_at: datetime       
    GSI1PK: str           # COMPANY#ALL
    GSI1SK: str           # <company_name>
    
    @staticmethod
    def create_keys(company_id: str, company_name: str) -> dict:
        return {
            'PK': f'COMPANY#{company_id}',
            'SK': f'METADATA#{company_id}',
            'GSI1PK': 'COMPANY#ALL',
            'GSI1SK': company_name
        }

class JobPosting(TypedDict):
    PK: str               # COMPANY#<company_id>
    SK: str               # JOB#<post_id>
    post_id: str          
    post_name: str        
    company_id: str       
    company_name: str     
    post_end: datetime   
    post_url: str         
    rec_id: str
    status: JobStatus           
    created_at: datetime  
    updated_at: datetime  
    GSI1PK: str          # STATUS#<status>
    GSI1SK: str          # <created_at>
    GSI2PK: str          # JOB#ALL
    GSI2SK: str          # <updated_at>
    
    @staticmethod
    def create_keys(company_id: str, post_id: str, status: JobStatus, created_at: datetime) -> dict:
        created_month = created_at.strftime("%Y%m")
        return {
            'PK': f'COMPANY#{company_id}',
            'SK': f'JOB#{post_id}',
            'GSI1PK': f'STATUS#{status}',
            'GSI1SK': created_at.isoformat(),
            'GSI2PK': f'DATE#{created_month}',
            'GSI2SK': post_id
        }

@dataclass
class Tag(TypedDict):
    PK: str               # TAG#<category>
    SK: str               # TAG#<tag_id>
    tag_id: str           
    category: TagCategory         
    name: str             
    parent_id: Optional[str]
    level: int            
    count: int            
    created_at: datetime  
    updated_at: datetime  
    GSI1PK: str          # TAG#ALL
    GSI1SK: str          # <count>#<tag_id>
    GSI2PK: str          # TAG#PARENT#<parent_id>  
    GSI2SK: str          # <tag_id> 

    @staticmethod
    def create_keys(category: str, tag_id: str, count: int, parent_id: Optional[str] = None) -> dict:
        keys = {
            'PK': f'TAG#{category}',
            'SK': f'TAG#{tag_id}',
            'GSI1PK': 'TAG#ALL',
            'GSI1SK': f'{count:010d}#{tag_id}'  # count를 10자리 숫자로 패딩
        }
        if parent_id:
            keys.update({
                'GSI2PK': f'TAG#PARENT#{parent_id}',
                'GSI2SK': tag_id
            })
        return keys

@dataclass
class JobTag(TypedDict):
    PK: str               # JOB#<job_id>
    SK: str               # TAG#<tag_id>
    job_tag_id: str       
    job_id: str           
    tag_id: str           
    created_at: datetime  
    GSI1PK: str          # TAG#<tag_id>
    GSI1SK: str          # JOB#<job_id>

    @staticmethod
    def create_keys(job_id: str, tag_id: str, created_at: datetime) -> dict:
        created_month = created_at.strftime("%Y%m")
        return {
            'PK': f'JOB#{job_id}',
            'SK': f'TAG#{tag_id}',
            'GSI1PK': f'TAG#{tag_id}',
            'GSI1SK': f'JOB#{job_id}',
            'GSI2PK': f'DATE#{created_month}',
            'GSI2SK': f'TAG#{tag_id}'
        }