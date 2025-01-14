from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreateEssayRequest(BaseModel):
    user_id: str
    essay_ask: str
    essay_content: Optional[str] = None
    
class EssayResponse(BaseModel):
    essay_id: str
    user_id: str
    essay_ask: str
    essay_content: Optional[str]
    created_at: datetime
    updated_at: datetime