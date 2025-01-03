from typing import List, Dict, Optional
from datetime import datetime
from ...base import AWSBaseService
from ...exceptions import AWSServiceException
from .models import JobPosting

class JobPostingRepository(AWSBaseService):
    def __init__(self):
        super().__init__('dynamodb')
        self.table = self.resource.Table('job_postings')
        
    def save_job_postings(self, jobs: List[JobPosting]) -> bool:
        try: 
            with self.table.batch_writer() as batch:
                for job in jobs:
                    batch.put_item(Item=job.to_dict())
            return True
        except Exception as e:
            raise AWSServiceException(f"DynamoDB 저장 실패: {str(e)}")
        
    def get_job_postings(self, 
                        source: Optional[str] = None, 
                        status: str = 'active') -> List[JobPosting]:
        try:
            if source:
                response = self.table.query(
                    IndexName='source-index',
                    KeyConditionExpression='source = :source',
                    FilterExpression='status = :status',
                    ExpressionAttributeValues={
                        ':source': source,
                        ':status': status
                    }
                )
            else:
                response = self.table.scan(
                    FilterExpression='status = :status',
                    ExpressionAttributeValues={':status': status}
                )
            
            return [JobPosting.from_dict(item) for item in response['Items']]
        except Exception as e:
            raise AWSServiceException(f"DynamoDB 조회 실패: {str(e)}")
        
    def health_check(self) -> bool:
        try: 
            self.table.scan(Limit=1)
            return True
        except Exception:
            return False