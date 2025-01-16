from typing import Optional, TypedDict
from datetime import datetime
import uuid

from botocore.exceptions import ClientError

from app.core.aws_client import AWSClient
from app.core.constants import TableNames
from app.core.enums import ScheduleStatus
from app.schemas.essay_schema import CreateEssayRequest, ScheduleResponse


class ScheduleItem(TypedDict):
    PK: str
    SK: str
    GSI1PK: str
    GSI1SK: str
    schedule_id: str
    user_id: str
    title: str
    company: Optional[str]
    date: str
    content: Optional[str]
    type: str
    tag: Optional[str]
    background_color: str
    completed: bool
    created_at: str
    updated_at: str
    
    
class EssayRepository:
    def __init__(self):
        self.dynamodb = AWSClient.get_client('dynamodb')
        self.table = self.dynamodb.Table(TableNames.Scuedlues)
        
    async def create_schedule(self, request: CreateScheduleRequest) -> str:
        try: 
            essay_id = str(uuid.uuid4())
            current_time = datetime.now().isoformat()
                
            schedule_item: ScheduleItem = {
                'PK': f"USER#{request.user_id}",
                'SK': f"Schedule#{essay_id}",
                'schedule_id': essay_id,
                'user_id': request.user_id,
                'schedule_ask': request.schedule_ask,
                'schedule_content': request.schedule_content,
                'status': ScheudleStatus.DRAFT.value,
                'created_at': current_time,
                'updated_at': current_time,
                'GSI1PK': "Schedule#ALL",
                'GSI1SK': current_time
            }
                
            self.table.put_item(Item=schedule_item)
            return schedule_id
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            raise Exception(f"Failed to create schedule: {error_code} - {error_message}")