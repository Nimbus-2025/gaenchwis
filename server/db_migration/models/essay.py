from typing import TypedDict, Optional
from datetime import datetime

class Essay(TypedDict):
    # Primary Key
    PK: str               # USER#<user_id>
    SK: str               # ESSAY#<essay_id>
    
    # Attributes
    essay_id: str         # essay_id
    user_id: str          # user_id(에세이 작성자)
    essay_ask: str        # 자소서 질문 
    essay_content: str    # 자소서 내용 
    created_at: datetime
    updated_at: datetime
    
    # GSI Keys: EssayDateIndex
    GSI1PK: str          # ESSAY#ALL
    GSI1SK: str          # <created_at>

class EssayJobPosting(TypedDict):
    # Primary Key
    PK: str               # ESSAY#<essay_id>
    SK: str               # POST#<post_id>
    
    # Attributes
    essay_id: str           # essay_id
    post_id: Optional[str]  # post_id(자소서와 연결된 공고 id)
    created_at: datetime
    
    # GSI Keys: EssayPostInverseIndex
    GSI1PK: str          # POST#<post_id>
    GSI1SK: str          # ESSAY#<essay_id>