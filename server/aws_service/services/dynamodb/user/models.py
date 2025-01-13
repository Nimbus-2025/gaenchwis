from typing import TypedDict, Optional
from datetime import datetime

class User(TypedDict):
    # Primary Key
    PK: str               # USER#<user_id>
    SK: str               # METADATA#<user_id>
    
    # Attributes
    user_id: str
    user_sns: Optional[str]
    user_name: str
    user_phone: str
    user_email: str
    created_at: datetime
    updated_at: datetime
    
    # GSI Keys
    GSI1PK: str          # USER#ALL
    GSI1SK: str          # <created_at>

class UserImage(TypedDict):
    # Primary Key
    PK: str               # USER#<user_id>
    SK: str               # IMAGE#<image_id>
    
    # Attributes
    image_id: str
    user_id: str
    image_name: str
    image_path: str
    created_at: datetime
    updated_at: datetime
    
    # GSI Keys
    GSI1PK: str          # IMAGE#ALL
    GSI1SK: str          # <created_at>

class UserTag(TypedDict):
    # Primary Key
    PK: str               # USER#<user_id>
    SK: str               # TAG#<tag_id>
    
    # Attributes
    user_id: str
    tag_id: str
    created_at: datetime
    
    # GSI Keys
    GSI1PK: str          # TAG#<tag_id>
    GSI1SK: str          # USER#<user_id>

class InterestCompany(TypedDict):
    # Primary Key
    PK: str               # USER#<user_id>
    SK: str               # COMPANY#<company_id>
    
    # Attributes
    user_id: str
    company_id: str
    created_at: datetime
    
    # GSI Keys
    GSI1PK: str          # COMPANY#<company_id>
    GSI1SK: str          # USER#<user_id>

class Schedule(TypedDict):
    # Primary Key
    PK: str               # USER#<user_id>
    SK: str               # SCHEDULE#<schedule_id>
    
    # Attributes
    schedule_id: str
    user_id: str
    schedule_date: datetime
    schedule_title: str
    schedule_content: str
    created_at: datetime
    updated_at: datetime
    
    # GSI Keys
    GSI1PK: str          # SCHEDULE#ALL
    GSI1SK: str          # <schedule_date>

class Bookmark(TypedDict):
    # Primary Key
    PK: str               # USER#<user_id>
    SK: str               # POST#<post_id>
    
    # Attributes
    user_id: str
    post_id: str
    created_at: datetime
    
    # GSI Keys
    GSI1PK: str          # POST#<post_id>
    GSI1SK: str          # USER#<user_id>

class JobApply(TypedDict):
    # Primary Key
    PK: str               # USER#<user_id>
    SK: str               # APPLY#<post_id>
    
    # Attributes
    user_id: str
    post_id: str
    apply_date: datetime
    interview_date: Optional[datetime]
    final_date: Optional[datetime]
    is_resulted: bool
    created_at: datetime
    updated_at: datetime
    
    # GSI Keys
    GSI1PK: str          # POST#<post_id>
    GSI1SK: str          # <apply_date>