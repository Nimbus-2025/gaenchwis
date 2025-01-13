from typing import TypedDict, Optional
from datetime import datetime

class Essay(TypedDict):
    # Primary Key
    PK: str               # USER#<user_id>
    SK: str               # ESSAY#<essay_id>
    
    # Attributes
    essay_id: str
    user_id: str
    essay_ask: str
    created_at: datetime
    updated_at: datetime
    
    # GSI Keys
    GSI1PK: str          # ESSAY#ALL
    GSI1SK: str          # <created_at>

class EssayContent(TypedDict):
    # Primary Key
    PK: str               # ESSAY#<essay_id>
    SK: str               # CONTENT#<version>
    
    # Attributes
    essay_id: str
    essay_content: str
    version: int
    created_at: datetime
    updated_at: datetime
    
    # GSI Keys
    GSI1PK: str          # CONTENT#ALL
    GSI1SK: str          # <created_at>

class EssayJobPosting(TypedDict):
    # Primary Key
    PK: str               # ESSAY#<essay_id>
    SK: str               # POST#<post_id>
    
    # Attributes
    essay_id: str
    post_id: str
    created_at: datetime
    
    # GSI Keys
    GSI1PK: str          # POST#<post_id>
    GSI1SK: str          # ESSAY#<essay_id>