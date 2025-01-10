# aws_service/services/dynamodb/user/models.py
from typing import TypedDict, Optional
from datetime import datetime
from dataclasses import dataclass

@dataclass
class User(TypedDict):
    PK: str                # USER#<user_id>
    SK: str                # METADATA#<user_id>
    user_id: str
    user_sns: int
    user_name: str
    user_phone: Optional[str]
    user_email: Optional[str]
    created_at: datetime
    updated_at: datetime
    GSI1PK: str           # USER#ALL
    GSI1SK: str           # <user_name>

    @staticmethod
    def create_keys(user_id: str, user_name: str) -> dict:
        return {
            'PK': f'USER#{user_id}',
            'SK': f'METADATA#{user_id}',
            'GSI1PK': 'USER#ALL',
            'GSI1SK': user_name
        }

@dataclass
class UserImage(TypedDict):
    PK: str                # USER#<user_id>
    SK: str                # IMAGE#<image_id>
    image_id: str
    user_id: str
    image_name: str
    image_path: str
    created_at: datetime
    GSI1PK: str           # IMAGE#ALL
    GSI1SK: str           # <created_at>

    @staticmethod
    def create_keys(user_id: str, image_id: str, created_at: datetime) -> dict:
        return {
            'PK': f'USER#{user_id}',
            'SK': f'IMAGE#{image_id}',
            'GSI1PK': 'IMAGE#ALL',
            'GSI1SK': created_at.isoformat()
        }