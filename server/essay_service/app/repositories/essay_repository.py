from typing import Optional, TypedDict, List
from datetime import datetime
import uuid
import logging
from botocore.exceptions import ClientError

from app.core.aws_client import AWSClient
from app.core.constants import TableNames
from app.schemas.essay_schema import SortOrder, SearchType, EssayJobPosting

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
            self.dynamodb = AWSClient.get_client('dynamodb')
            self.table = self.dynamodb.Table(TableNames.ESSAYS)
            self.applies_table = self.dynamodb.Table(TableNames.APPLIES)
            self.essay_job_postings_table = self.dynamodb.Table(TableNames.ESSAY_JOB_POSTINGS)
            self.job_postings_table = self.dynamodb.Table(TableNames.JOB_POSTINGS)
        except Exception as e:
            logging.error(f"Error initializing repository: {str(e)}")
            raise

    def get_user_applied_jobs(self, user_id: str) -> List[dict]:
        try:
            response = self.applies_table.query(
                KeyConditionExpression="PK = :PK",
                ExpressionAttributeValues={
                    ':PK': f"USER#{user_id}"
                }
            )
            return response.get('Items', [])
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            raise Exception(f"Failed to create essay: {error_code} - {error_message}")

    def create_essays_and_links(
        self, 
        user_id: str, 
        questions: List[dict], 
        job_postings: List[dict] = None,
    ) -> List[str]:
        try: 
            essay_ids = []
            current_time = datetime.now().isoformat()
                    
            # 1. Essays 생성
            for question in questions:
                essay_id = str(uuid.uuid4())
                essay_item: EssayItem = {
                    'PK': f"USER#{user_id}",
                    'SK': f"ESSAY#{essay_id}",
                    'essay_id': essay_id,
                    'user_id': user_id,
                    'essay_ask': question['essay_ask'],
                    'essay_content': question.get('essay_content', ''),
                    'created_at': current_time,
                    'updated_at': current_time,
                    'GSI1PK': "ESSAY#ALL",
                    'GSI1SK': current_time
                }
                
                self.table.put_item(Item=essay_item)
                essay_ids.append(essay_id)
                
            # 채용공고 연결
            if job_postings:
                for essay_id in essay_ids:
                    for posting in job_postings:
                        link_item: EssayJobPosting = {
                            'PK': f"ESSAY#{essay_id}",
                            'SK': f"POST#{posting['post_id']}",  # dictionary 접근으로 수정
                            'essay_id': essay_id,
                            'post_id': posting['post_id'],
                            'company_id': posting['company_id'],
                            'created_at': current_time,                            
                            'GSI1PK': f"POST#{posting['post_id']}",  # dictionary 접근으로 수정
                            'GSI1SK': f"ESSAY#{essay_id}"
                        }
                        self.essay_job_postings_table.put_item(Item=link_item)
            return essay_ids
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            raise Exception(f"Failed to create essay: {error_code} - {error_message}")
    
    def update_essay(
        self, 
        user_id: str,
        essay_id: str, 
        update_data: dict
    ) -> bool:
        try: 
            # 1. 먼저 에세이가 존재하는지 확인
            response = self.table.get_item(
                Key={
                    'PK': f"USER#{user_id}",
                    'SK': f"ESSAY#{essay_id}"
                }
            )
            
            if 'Item' not in response:
                raise ValueError("Essay not found")
                
            # 2. 업데이트할 필드 구성
            update_expr_parts = []
            expr_values = {}
            expr_names = {}
            
            if 'essay_ask' in update_data:
                update_expr_parts.append('#essay_ask = :essay_ask')
                expr_values[':essay_ask'] = update_data['essay_ask']
                expr_names['#essay_ask'] = 'essay_ask'
                
            if 'essay_content' in update_data:
                update_expr_parts.append('#essay_content = :essay_content')
                expr_values[':essay_content'] = update_data['essay_content']
                expr_names['#essay_content'] = 'essay_content'
                
            # 업데이트 시간 추가
            current_time = datetime.now().isoformat()
            update_expr_parts.append('updated_at = :updated_at')
            expr_values[':updated_at'] = current_time
            
            # 3. 업데이트 실행
            update_expression = 'SET ' + ', '.join(update_expr_parts)
            
            self.table.update_item(
                Key={
                    'PK': f"USER#{user_id}",
                    'SK': f"ESSAY#{essay_id}"
                },
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expr_values,
                ExpressionAttributeNames=expr_names if expr_names else None,
                ReturnValues='UPDATED_NEW'
            )
            
            return True
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            raise Exception(f"Failed to update essay: {error_code} - {error_message}")

    def delete_essay(
        self,
        user_id: str,
        essay_id: str
    ) -> bool:
        try:
            # 1. 먼저 에세이가 존재하는지 확인
            response = self.table.get_item(
                Key={
                    'PK': f"USER#{user_id}",
                    'SK': f"ESSAY#{essay_id}"
                }
            )
            
            if 'Item' not in response:
                raise ValueError("Essay not found")
                
            # 2. 연결된 채용공고 링크 삭제
            # 2-1. 해당 에세이의 모든 채용공고 링크 조회
            links_response = self.essay_job_postings_table.query(
                KeyConditionExpression="PK = :pk",
                ExpressionAttributeValues={
                    ':pk': f"ESSAY#{essay_id}"
                }
            )
            
            # 2-2. 모든 링크 삭제
            for link in links_response.get('Items', []):
                self.essay_job_postings_table.delete_item(
                    Key={
                        'PK': link['PK'],
                        'SK': link['SK']
                    }
                )
                
            # 3. 에세이 삭제
            self.table.delete_item(
                Key={
                    'PK': f"USER#{user_id}",
                    'SK': f"ESSAY#{essay_id}"
                }
            )
            
            return True
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            raise Exception(f"Failed to delete essay: {error_code} - {error_message}")

    def get_essay_detail(
        self,
        user_id: str,
        essay_id: str
    ) -> dict:
        try:
            # 1. 에세이 기본 정보 조회
            response = self.table.get_item(
                Key={
                    'PK': f"USER#{user_id}",
                    'SK': f"ESSAY#{essay_id}"
                }
            )
            
            if 'Item' not in response:
                raise ValueError("Essay not found")
                    
            essay_item = response['Item']
            
            # 2. 연관된 공고 ID들 조회 
            links_response = self.essay_job_postings_table.query(
                KeyConditionExpression="PK = :pk",
                ExpressionAttributeValues={
                    ':pk': f"ESSAY#{essay_id}"
                }
            )
            
            links = links_response.get('Items', [])
            print(f"Found {len(links)} job posting links: {links}")
            
            # 3. 연관된 공고 정보 조회
            job_postings = []
            for link in links:
                try:
                    post_id = link['SK'].split('#')[1]
                    company_id = link['company_id']
                    
                    # 정확한 복합키로 직접 조회
                    job_posting_response = self.job_postings_table.get_item(
                        Key={
                            'PK': f"COMPANY#{company_id}",
                            'SK': f"JOB#{post_id}"
                        }
                    )
                    
                    if 'Item' in job_posting_response:
                        job_posting = job_posting_response['Item']
                        job_postings.append({
                            'post_id': post_id,
                            'company_name': job_posting.get('company_name', '회사명 없음'),
                            'post_name': job_posting.get('post_name', '공고명 없음')
                        })
                        print(f"Successfully fetched job posting: {job_posting}")
                    else:
                        print(f"Job posting not found for company_id={company_id}, post_id={post_id}")
                        job_postings.append({
                            'post_id': post_id,
                            'company_name': '삭제된 회사',
                            'post_name': '삭제된 공고'
                        })
                        
                except Exception as e:
                    print(f"Error fetching job posting {post_id}: {str(e)}")
                    job_postings.append({
                        'post_id': post_id,
                        'company_name': '에러 발생',
                        'post_name': f'공고 조회 실패: {str(e)}'
                    })
            
            result = {
                'essay_id': essay_id,
                'essay_ask': essay_item['essay_ask'],
                'essay_content': essay_item.get('essay_content', ''),
                'created_at': essay_item['created_at'],
                'updated_at': essay_item['updated_at'],
                'related_job_postings': job_postings
            }
            
            return result
                
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            raise Exception(f"Failed to get essay detail: {error_code} - {error_message}")

    def search_essays(
        self,
        user_id: str,
        search_type: SearchType,
        keyword: str,
        sort_order: SortOrder = SortOrder.DESC,
        page: int = 1,
        page_size: int = 10
    ) -> dict:
        try:
            print(f"Searching with type: {search_type}, keyword: {keyword}")
            if search_type == SearchType.QUESTION:
                filter_expression = 'contains(essay_ask, :keyword)'
            else:
                filter_expression = 'contains(essay_content, :keyword)'
            
            # 로그 추가    
            print(f"Filter expression: {filter_expression}")
            # 1. 먼저 모든 에세이를 가져옵니다
            response = self.table.query(
                KeyConditionExpression='PK = :pk',
                ExpressionAttributeValues={
                    ':pk': f"USER#{user_id}"
                },
                ScanIndexForward=sort_order == SortOrder.ASC
            )
            
            items = response.get('Items', [])
            
            print(f"Found items: {len(items)}")
            print("First few items:", items[:2]) 
            
            # 2. Python 단에서 검색을 수행합니다
            filtered_items = []
            for item in items:
                if search_type == SearchType.QUESTION:
                    if keyword.lower() in item['essay_ask'].lower():
                        filtered_items.append(item)
                else:  # SearchType.CONTENT
                    if 'essay_content' in item and item['essay_content']:
                        if keyword.lower() in item['essay_content'].lower():
                            filtered_items.append(item)
            
            # 3. 페이지네이션 처리
            total_count = len(filtered_items)
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            paged_items = filtered_items[start_idx:end_idx] if start_idx < total_count else []
            
            essays = [
                {
                    'essay_id': item['SK'].split('#')[1],
                    'essay_ask': item['essay_ask'],
                    'created_at': item['created_at']
                }
                for item in paged_items
            ]
            
            return {
                'essays': essays,
                'total_count': total_count,
                'current_page': page,
                'total_pages': (total_count + page_size - 1) // page_size
            }
                
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            raise Exception(f"Failed to search essays: {error_code} - {error_message}")
        
    def get_essay_list(
        self,
        user_id: str,
        sort_order: SortOrder = SortOrder.DESC,
        page: int = 1,
        page_size: int = 10
    ) -> dict:
        try:
            # 자기소개서 목록 조회
            response = self.table.query(
                KeyConditionExpression='PK = :pk',
                ExpressionAttributeValues={
                    ':pk': f"USER#{user_id}",
                },
                ScanIndexForward=sort_order == SortOrder.ASC,  # DESC면 False, ASC면 True
            )
            
            items = response.get('Items', [])
            total_count = len(items)
            
            # 페이지네이션 처리
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            paged_items = items[start_idx:end_idx] if start_idx < total_count else []
            
            # EssayListItem 스키마에 맞게 응답 구성
            essays = []
            for item in paged_items:
                essay_id = item['SK'].split('#')[1]  # "ESSAY#uuid" 형태에서 uuid 추출
                essays.append({
                    'essay_id': essay_id,
                    'essay_ask': item['essay_ask'],
                    'created_at': item['created_at']  # ISO 형식의 날짜 문자열
                })
            
            # EssayListResponse 스키마에 맞게 최종 응답 구성
            return {
                'essays': essays,
                'total_count': total_count,
                'current_page': page,
                'total_pages': (total_count + page_size - 1) // page_size
            }
                
        except ClientError as e:
            self.logger.error(f"Error in get_essay_list: {str(e)}")
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            raise Exception(f"Failed to get essay list: {error_code} - {error_message}")
        except Exception as e:
            self.logger.error(f"Unexpected error in get_essay_list: {str(e)}")
            raise Exception(f"Failed to get essay list: {str(e)}")