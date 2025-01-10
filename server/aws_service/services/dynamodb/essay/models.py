# aws_service/services/dynamodb/essay/models.py
from typing import TypedDict
from datetime import datetime
from ..common.enums import EssayStatus
from dataclasses import dataclass

@dataclass
class Essay(TypedDict):
    PK: str                # USER#<user_id>
    SK: str                # ESSAY#<essay_id>
    essay_id: str
    user_id: str
    essay_title: str
    company_id: Optional[str]
    post_id: Optional[str]
    status: EssayStatus
    created_at: datetime
    updated_at: datetime
    GSI1PK: str           # ESSAY#<status>
    GSI1SK: str           # <created_at>
    GSI2PK: str           # COMPANY#<company_id>
    GSI2SK: str           # ESSAY#<essay_id>

    @staticmethod
    def create_keys(user_id: str, essay_id: str, status: EssayStatus, company_id: Optional[str], created_at: datetime) -> dict:
        keys = {
            'PK': f'USER#{user_id}',
            'SK': f'ESSAY#{essay_id}',
            'GSI1PK': f'ESSAY#{status}',
            'GSI1SK': created_at.isoformat(),
        }
        if company_id:
            keys.update({
                'GSI2PK': f'COMPANY#{company_id}',
                'GSI2SK': f'ESSAY#{essay_id}'
            })
        return keys

@dataclass
class EssayContent(TypedDict):
    PK: str                # ESSAY#<essay_id>
    SK: str                # CONTENT#<version>
    essay_id: str
    content: str
    version: int
    created_at: datetime
    GSI1PK: str           # CONTENT#ALL
    GSI1SK: str           # <created_at>

    @staticmethod
    def create_keys(essay_id: str, version: int, created_at: datetime) -> dict:
        return {
            'PK': f'ESSAY#{essay_id}',
            'SK': f'CONTENT#{version}',
            'GSI1PK': 'CONTENT#ALL',
            'GSI1SK': created_at.isoformat()
        }