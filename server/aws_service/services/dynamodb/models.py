from typing import TypedDict, List, Optional
from datetime import datetime
from ..common.enums import JobStatus, TagCategory

class Company(TypedDict):
    # Primary Key
    PK: str                # COMPANY#<company_id>
    SK: str                # METADATA#<company_id>
    
    # Attributes
    company_id: str        
    company_name: str
    created_at: datetime  
    updated_at: datetime       
    
    # GSI Keys
    GSI1PK: str           # COMPANY#ALL
    GSI1SK: str           # <company_name>

class JobPosting(TypedDict):
    # Primary Key
    PK: str               # COMPANY#<company_id>
    SK: str               # JOB#<post_id>
    
    # Attributes
    post_id: str          
    post_name: str        
    company_id: str       
    company_name: str     
    is_closed: datetime   
    post_url: str         
    status: JobStatus           
    created_at: datetime  
    updated_at: datetime  
    
    # GSI Keys
    GSI1PK: str          # STATUS#<status>
    GSI1SK: str          # <created_at>
    GSI2PK: str          # JOB#ALL
    GSI2SK: str          # <updated_at>
    
class Tag(TypedDict):
    # Primary Key
    PK: str               # TAG#<category>
    SK: str               # TAG#<tag_id>
    
    # Attributes
    tag_id: str           
    category: TagCategory         
    name: str             
    parent_id: Optional[str]
    level: int            
    count: int            
    created_at: datetime  
    updated_at: datetime  
    
    # GSI Keys
    GSI1PK: str          # TAG#ALL
    GSI1SK: str          # <count>#<tag_id>

class JobTag(TypedDict):
    # Primary Key
    PK: str               # JOB#<job_id>
    SK: str               # TAG#<tag_id>
    
    # Attributes
    job_tag_id: str       
    job_id: str           
    tag_id: str           
    created_at: datetime  
    
    # GSI Keys
    GSI1PK: str          # TAG#<tag_id>
    GSI1SK: str          # JOB#<job_id>