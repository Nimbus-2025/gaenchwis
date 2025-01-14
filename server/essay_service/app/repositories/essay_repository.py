from typing import Optional, TypedDict
from datetime import datetime
import uuid

from botocore.exceptions import ClientError

from app.core.aws_client import AWSClient
from app.core.constants import TableNames
from app.core.enums import EssayStatus
from app.schemas.essay_schema import CreateEssayRequest, EssayResponse


class EssayItem(TypedDict):
    PK: str
    SK: str
    GSI1PK: str
    GSI1SK: str
    essay_id: str
    user_id: str
    essay_ask: str
    essay_content: Optional[str]
    status: str
    created_at: str
    updated_at: str
    
    
class EssayRepository:
    def __init__(self):
        self.dynamodb = AWSClient.get_client('dynamodb')
        self.table = self.dynamodb.Table(TableNames.ESSAYS)
        
    async def create_essay(self, request: CreateEssayRequest) -> str:
        try: 
            essay_id = str(uuid.uuid4())
            current_time = datetime.now().isoformat()
                
            essay_item: EssayItem = {
                'PK': f"USER#{request.user_id}",
                'SK': f"ESSAY#{essay_id}",
                'essay_id': essay_id,
                'user_id': request.user_id,
                'essay_ask': request.essay_ask,
                'essay_content': request.essay_content,
                'status': EssayStatus.DRAFT.value,
                'created_at': current_time,
                'updated_at': current_time,
                'GSI1PK': "ESSAY#ALL",
                'GSI1SK': current_time
            }
                
            self.table.put_item(Item=essay_item)
            return essay_id
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            raise Exception(f"Failed to create essay: {error_code} - {error_message}")