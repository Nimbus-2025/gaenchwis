from datetime import datetime
from typing import Optional, TypedDict, List
from uuid import uuid4
import logging
from botocore.exceptions import ClientError

from app.core.aws_client import AWSClient
from app.core.constants import TableNames, IndexNames
from app.schemas.user_schemas import ApplyCreate, ApplyUpdate, BookmarkCreate, InterestCompanyCreate

class UserRepository:
    def __init__(self):
        # 로거 설정
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # 핸들러가 없는 경우에만 추가
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            
        try: 
            logging.info("Initializing DynamoDB client...")
            self.dynamodb = AWSClient.get_client('dynamodb')
            logging.info("DynamoDB client initialized successfully")
            
            logging.info(f"Connecting to table: {TableNames.APPLIES}")
            self.table = self.dynamodb.Table(TableNames.APPLIES)
            
            logging.info(f"Connecting to table: {TableNames.BOOKMARKS}")
            self.bookmarks_table = self.dynamodb.Table(TableNames.BOOKMARKS)
            
            logging.info(f"Connecting to table: {TableNames.INTEREST_COMPANIES}")
            self.interest_companies_table = self.dynamodb.Table(TableNames.INTEREST_COMPANIES)
            
            logging.info("All tables connected successfully")
        except Exception as e:
            logging.error(f"Error initializing repository: {str(e)}")
            raise

    def create_apply(self, user_id: str, apply_data: ApplyCreate) -> dict:
        apply_id = str(uuid4())
        now = datetime.utcnow().isoformat()
            
        item = {
            'PK': f"USER#{user_id}",
            'SK': f"APPLY#{apply_data.post_id}",
            'GSI1PK': f"POST#{apply_data.post_id}",
            'GSI1SK': apply_id,
            'user_id': user_id,
            'post_id': apply_data.post_id,
            'post_name': apply_data.post_name,
            'apply_date': now,
            'deadline_date': None,
            'document_result_date': None,
            'interview_date': None,
            'final_date': None,
            'memo': None,
            'is_resulted': False,
            'created_at': now,
            'updated_at': now
        }
            
        self.table.put_item(Item=item)
        return item
        
    def get_apply(self, user_id: str, post_id: str) -> Optional[dict]:
        response = self.table.get_item(
            Key={
                'PK': f"USER#{user_id}",
                'SK': f"APPLY#{post_id}"
            }
        )
        return response.get('Item')
    
    def delete_apply(self, user_id: str, post_id: str) -> bool:
        try: 
            self.table.delete_item(
                Key={
                    'PK': f"USER#{user_id}",
                    'SK': f"APPLY#{post_id}"
                }
            )
            return True
        except ClientError as e:
            logging.error(f"Error deleting apply: {str(e)}")
            return False
        
    def update_apply(self, user_id: str, post_id: str, apply_data: ApplyUpdate) -> Optional[dict]:
        try:
            update_expr_parts = []
            attr_names = {}
            attr_values = {}
            
            # 수정 가능한 필드만 포함
            update_fields = {
                'document_result_date': 'document_result_date',
                'interview_date': 'interview_date',
                'final_date': 'final_date',
                'memo': 'memo'
            }
            
            for field, db_field in update_fields.items():
                value = getattr(apply_data, field)
                if value is not None:  # None이 아닌 값만 업데이트
                    update_expr_parts.append(f"#{field} = :{field}")
                    attr_names[f"#{field}"] = db_field
                    if isinstance(value, datetime):
                        attr_values[f":{field}"] = value.isoformat()
                    else:
                        attr_values[f":{field}"] = value

            # updated_at 자동 업데이트
            update_expr_parts.append("#updated_at = :updated_at")
            attr_names["#updated_at"] = "updated_at"
            attr_values[":updated_at"] = datetime.utcnow().isoformat()

            response = self.table.update_item(
                Key={
                    'PK': f"USER#{user_id}",
                    'SK': f"APPLY#{post_id}"
                },
                UpdateExpression="SET " + ", ".join(update_expr_parts),
                ExpressionAttributeNames=attr_names,
                ExpressionAttributeValues=attr_values,
                ReturnValues="ALL_NEW"
            )
            return response.get('Attributes')
            
        except ClientError as e:
            logging.error(f"Error updating apply: {str(e)}")
            return None
        
    def get_apply_detail(self, user_id: str, post_id: str) -> Optional[dict]:
        try:
            logging.info(f"Querying with PK: USER#{user_id}, SK: APPLY#{post_id}")
            
            # get_apply() 결과와 비교
            apply = self.get_apply(user_id, post_id)
            logging.info(f"get_apply() result: {apply}")

            response = self.table.get_item(
                Key={
                    'PK': f"USER#{user_id}",
                    'SK': f"APPLY#{post_id}"
                }
            )
            
            logging.info(f"get_apply_detail() response: {response}")
            item = response.get('Item')
            
            if item:
                # 응답 스키마에 맞게 필드를 매핑
                return {
                    'post_name': item.get('post_name'),
                    'apply_date': item.get('apply_date'),
                    'deadline_date': item.get('deadline_date'),
                    'document_result_date': item.get('document_result_date'),
                    'interview_date': item.get('interview_date'),
                    'final_date': item.get('final_date'),
                    'memo': item.get('memo')
                }
            
            return None
            
        except ClientError as e:
            logging.error(f"Error getting apply detail: {str(e)}")
            return None

    def get_essays_by_post(self, user_id: str, post_id: str) -> list[dict]:
        try:
            # 1. 먼저 EssayJobPosting 테이블에서 post_id에 해당하는 essay_id들을 조회
            essay_job_table = self.dynamodb.Table(TableNames.ESSAY_JOB_POSTINGS)
            response = essay_job_table.query(
                IndexName=IndexNames.POST_ESSAY_GSI,  # 'GSI1' 대신 정의된 상수 사용
                KeyConditionExpression='GSI1PK = :gsi1pk',
                ExpressionAttributeValues={
                    ':gsi1pk': f"JOB#{post_id}"
                }
            )
            
            # 디버깅을 위한 로그 추가
            logging.info(f"Found essay links: {response.get('Items')}")
            
            if not response.get('Items'):
                return []
                
            # 2. 찾은 essay_id들로 Essay 테이블에서 실제 에세이 데이터 조회
            essay_table = self.dynamodb.Table(TableNames.ESSAYS)
            essays = []
            
            for item in response['Items']:
                essay_id = item['GSI1SK'].split('#')[1] 
                logging.info(f"Fetching essay with ID: {essay_id}")
                
                essay_response = essay_table.get_item(
                    Key={
                        'PK': f"USER#{user_id}",
                        'SK': f"ESSAY#{essay_id}"
                    }
                )
                
                if essay_response.get('Item'):
                    essays.append(essay_response['Item'])
            
            return essays
            
        except ClientError as e:
            logging.error(f"Error getting essays by post: {str(e)}")
            return []
        
    def create_bookmark(self, user_id: str, bookmark_data: BookmarkCreate) -> dict:
        now = datetime.utcnow().isoformat()
        
        item = {
            'PK': f"USER#{user_id}",
            'SK': f"BOOKMARK#{bookmark_data.post_id}",
            'GSI1PK': f"POST#{bookmark_data.post_id}",
            'GSI1SK': now,
            'user_id': user_id,
            'post_id': bookmark_data.post_id,
            'post_name': bookmark_data.post_name,
            'created_at': now,
            'updated_at': now
        }
        
        self.bookmarks_table.put_item(Item=item)
        return item
    
    def get_bookmark(self, user_id: str, post_id: str) -> Optional[dict]:
        response = self.bookmarks_table.get_item(
            Key={
                'PK': f"USER#{user_id}",
                'SK': f"BOOKMARK#{post_id}"
            }
        )
        return response.get('Item')
    
    def delete_bookmark(self, user_id: str, post_id: str) -> bool:
        try:
            self.bookmarks_table.delete_item(
                Key={
                    'PK': f"USER#{user_id}",
                    'SK': f"BOOKMARK#{post_id}"
                }
            )
            return True
        except ClientError as e:
            logging.error(f"Error deleting bookmark: {str(e)}")
            return False
        
    def get_user_bookmarks(self, user_id: str) -> list[dict]:
        try:
            response = self.bookmarks_table.query(
                KeyConditionExpression='PK = :pk AND begins_with(SK, :sk)',
                ExpressionAttributeValues={
                    ':pk': f"USER#{user_id}",
                    ':sk': "BOOKMARK#"
                }
            )
            return response.get('Items', [])
        except ClientError as e:
            logging.error(f"Error getting user bookmarks: {str(e)}")
            return []
        
    def create_interest_company(self, user_id: str, company_data: InterestCompanyCreate) -> dict:
        now = datetime.utcnow().isoformat()
        
        item = {
            'PK': f"USER#{user_id}",
            'SK': f"COMPANY#{company_data.company_id}",
            'GSI1PK': f"COMPANY#{company_data.company_id}",
            'GSI1SK': now,
            'user_id': user_id,
            'company_id': company_data.company_id,
            'company_name': company_data.company_name,
            'created_at': now,
            'updated_at': now
        }
        
        self.interest_companies_table.put_item(Item=item)
        return item

    def delete_interest_company(self, user_id: str, company_id: str) -> bool:
        try:
            self.interest_companies_table.delete_item(
                Key={
                    'PK': f"USER#{user_id}",
                    'SK': f"COMPANY#{company_id}"
                }
            )
            return True
        except ClientError as e:
            logging.error(f"Error deleting interest company: {str(e)}")
            return False
        
    def get_interest_company(self, user_id: str, company_id: str) -> Optional[dict]:
        response = self.interest_companies_table.get_item(
            Key={
                'PK': f"USER#{user_id}",
                'SK': f"COMPANY#{company_id}"
            }
        )
        return response.get('Item')
    
    def get_user_interest_companies(self, user_id: str) -> list[dict]:
        try:
            response = self.interest_companies_table.query(
                KeyConditionExpression='PK = :pk AND begins_with(SK, :sk)',
                ExpressionAttributeValues={
                    ':pk': f"USER#{user_id}",
                    ':sk': "COMPANY#"
                }
            )
            return response.get('Items', [])
        except ClientError as e:
            logging.error(f"Error getting user interest companies: {str(e)}")
            return []
