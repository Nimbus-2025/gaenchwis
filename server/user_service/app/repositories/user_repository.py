from datetime import datetime
from typing import Optional, TypedDict, List
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
            self.dynamodb = AWSClient.get_client('dynamodb')
            self.table = self.dynamodb.Table(TableNames.APPLIES)
            self.bookmarks_table = self.dynamodb.Table(TableNames.BOOKMARKS)
            self.interest_companies_table = self.dynamodb.Table(TableNames.INTEREST_COMPANIES)
            self.essay_table = self.dynamodb.Table(TableNames.ESSAYS)
            self.essay_job_table = self.dynamodb.Table(TableNames.ESSAY_JOB_POSTINGS)
            self.job_posting_table = self.dynamodb.Table(TableNames.JOB_POSTINGS)
            self.tags_table = self.dynamodb.Table(TableNames.TAGS)
            self.job_tags_table = self.dynamodb.Table(TableNames.JOB_TAGS)

        except Exception as e:
            logging.error(f"Error initializing repository: {str(e)}")
            raise

    def create_apply(self, user_id: str, apply_data: ApplyCreate) -> dict:
        now = datetime.utcnow().isoformat()
            
        item = {
            'PK': f"USER#{user_id}",
            'SK': f"APPLY#{apply_data.post_id}",
            'GSI1PK': f"POST#{apply_data.post_id}",
            'GSI1SK': now,                          
            'user_id': user_id,
            'post_id': apply_data.post_id,
            'post_name': apply_data.post_name,
            'deadline_date': None,
            'document_result_date': None,
            'interview_date': None,
            'final_date': None,
            'memo': None,
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
                    'apply_date': item.get('GSI1SK'),
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
            response = self.essay_job_table.query(
                IndexName=IndexNames.ESSAY_POST_INVERSE_GSI,  
                KeyConditionExpression='GSI1PK = :gsi1pk',
                ExpressionAttributeValues={
                    ':gsi1pk': f"POST#{post_id}"
                }
            )
            
            # 디버깅을 위한 로그 추가
            logging.info(f"Found essay links: {response.get('Items')}")
            
            if not response.get('Items'):
                return []
                
            # 2. 찾은 essay_id들로 Essay 테이블에서 실제 에세이 데이터 조회
            essays = []
            
            for item in response['Items']:
                essay_id = item['GSI1SK'].split('#')[1] 
                logging.info(f"Fetching essay with ID: {essay_id}")
                
                essay_response = self.essay_table.get_item(
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
            'SK': f"POST#{bookmark_data.post_id}",  
            'GSI1PK': f"POST#{bookmark_data.post_id}",
            'GSI1SK': f"USER#{user_id}",
            'user_id': user_id,
            'post_id': bookmark_data.post_id,
            'post_name': bookmark_data.post_name,  # BookmarkCreate에서 전달받은 post_name 추가
            'created_at': now,
        }
        
        self.bookmarks_table.put_item(Item=item)
        return item
    
    def get_bookmark(self, user_id: str, post_id: str) -> Optional[dict]:
        response = self.bookmarks_table.get_item(
            Key={
                'PK': f"USER#{user_id}",
                'SK': f"POST#{post_id}"
            }
        )
        return response.get('Item')
    
    def delete_bookmark(self, user_id: str, post_id: str) -> bool:
        try:
            self.bookmarks_table.delete_item(
                Key={
                    'PK': f"USER#{user_id}",
                    'SK': f"POST#{post_id}"
                }
            )
            return True
        except ClientError as e:
            logging.error(f"Error deleting bookmark: {str(e)}")
            return False
        
    def get_user_bookmarks(self, user_id: str) -> list[dict]:
        try:
            # 1. 먼저 유저의 북마크 정보를 가져옵니다
            bookmarks = self.bookmarks_table.query(
                KeyConditionExpression='PK = :pk AND begins_with(SK, :sk)',
                ExpressionAttributeValues={
                    ':pk': f"USER#{user_id}",
                    ':sk': "POST#"
                }
            ).get('Items', [])

            # 디버깅을 위한 로그 추가
            logging.info(f"Found bookmarks: {bookmarks}")

            # 2. 각 북마크된 게시물에 대한 추가 정보를 가져옵니다
            for bookmark in bookmarks:
                post_id = bookmark['post_id']

                # 2-1. 게시물 정보 조회하여 company_name 가져오기
                # JobPosting 테이블의 모든 항목을 scan하여 post_id가 일치하는 항목 찾기
                scan_response = self.job_posting_table.query(
                    IndexName="JobPostId",
                    KeyConditionExpression='post_id = :post_id',
                    ExpressionAttributeValues={
                        ':post_id': post_id
                    }
                )

                # 디버깅을 위한 로그 추가
                logging.info(f"Found job posting for post_id {post_id}: {scan_response.get('Items')}")

                job_posting_items = scan_response.get('Items', [])
                if job_posting_items:
                    job_posting = job_posting_items[0]
                    bookmark['company_name'] = job_posting.get('company_name', '')
                    bookmark['post_url'] = job_posting.get('post_url', '')
                else:
                    bookmark['company_name'] = ''

                # 2-2. 태그 정보 조회
                bookmark['tags'] = []
                job_tags_response = self.job_tags_table.query(
                    KeyConditionExpression='PK = :pk',
                    ExpressionAttributeValues={
                        ':pk': f"JOB#{post_id}"
                    }
                )

                # 디버깅을 위한 로그 추가
                logging.info(f"Found job tags for post_id {post_id}: {job_tags_response.get('Items')}")

                job_tags = job_tags_response.get('Items', [])

                # 2-3. 태그 정보 처리
                for job_tag in job_tags:
                    tag_id = job_tag.get('tag_id')
                    if tag_id:
                        # 태그 정보 조회할 때 SK 부분을 제외하고 PK로만 조회
                        tag_response = self.tags_table.query(
                            KeyConditionExpression='PK = :pk',
                            ExpressionAttributeValues={
                                ':pk': f"TAG#{tag_id}"
                            }
                        )
                        
                        # 디버깅을 위한 로그 추가
                        logging.info(f"Found tag for tag_id {tag_id}: {tag_response.get('Items')}")

                        tags = tag_response.get('Items', [])
                        if tags:
                            bookmark['tags'].append(tags[0].get('tag_name', ''))
 
            return bookmarks

        except ClientError as e:
            logging.error(f"Error getting user bookmarks: {str(e)}")
            return []
        
    def create_interest_company(self, user_id: str, company_data: InterestCompanyCreate) -> dict:
        now = datetime.utcnow().isoformat()
        
        item = {
            'PK': f"USER#{user_id}",
            'SK': f"COMPANY#{company_data.company_id}",
            'user_id': user_id,
            'company_id': company_data.company_id,
            'company_name': company_data.company_name,
            'created_at': now,
            'GSI1PK': f"COMPANY#{company_data.company_id}",
            'GSI1SK': f"USER#{user_id}"  
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
            # 1. 먼저 유저의 관심 기업 정보를 가져옵니다
            companies = self.interest_companies_table.query(
                KeyConditionExpression='PK = :pk AND begins_with(SK, :sk)',
                ExpressionAttributeValues={
                    ':pk': f"USER#{user_id}",
                    ':sk': "COMPANY#"
                }
            ).get('Items', [])

            logging.info(f"Found interest companies: {companies}")

            # 2. 각 관심 기업에 대한 채용공고와 태그 정보를 가져옵니다
            for company in companies:
                company_id = company['SK']
                logging.info(f"Looking for job postings for company_id: {company_id}")

                # 2-1. 해당 기업의 채용공고 목록 가져오기
                job_postings_response = self.job_posting_table.query(
                    KeyConditionExpression='PK = :pk',
                    ExpressionAttributeValues={
                        ':pk': f"{company_id}"
                    }
                )

                postings = job_postings_response.get('Items', [])
                logging.info(f"Found {len(postings)} job postings for company {company_id}")
                
                # 채용공고 정보 추가
                company['job_postings'] = []
                company['has_active_postings'] = len(postings) > 0
                company['active_postings_count'] = len(postings)

                for posting in postings:
                    job_posting_info = {
                        'post_url': posting.get('post_url'),
                        'post_id': posting.get('post_id'),
                        'title': posting.get('post_name'),  # post_name을 title로 사용
                        'deadline': posting.get('deadline'),  # deadline은 string으로 유지
                        'tags': []
                    }
                    
                    logging.info(f"Processing posting: {job_posting_info}")

                    # 2-2. 각 채용공고의 태그 정보 가져오기
                    job_tags_response = self.job_tags_table.query(
                        KeyConditionExpression='PK = :pk',
                        ExpressionAttributeValues={
                            ':pk': f"JOB#{posting.get('post_id')}"
                        }
                    )

                    job_tags = job_tags_response.get('Items', [])
                    logging.info(f"Found {len(job_tags)} tags for post_id {posting.get('post_id')}")

                    # 태그 정보 처리
                    for job_tag in job_tags:
                        tag_id = job_tag.get('tag_id')
                        if tag_id:
                            tag_response = self.tags_table.query(
                                KeyConditionExpression='PK = :pk',
                                ExpressionAttributeValues={
                                    ':pk': f"TAG#{tag_id}"
                                }
                            )
                            
                            tags = tag_response.get('Items', [])
                            if tags:
                                job_posting_info['tags'].append(tags[0].get('tag_name', ''))

                    company['job_postings'].append(job_posting_info)
                    logging.info(f"Successfully added posting: {job_posting_info}")

                # 2-3. 기업 관련 태그들의 집합 생성
                all_tags = set()
                for posting in company['job_postings']:
                    all_tags.update(posting['tags'])
                company['tags'] = list(all_tags)

            return companies

        except ClientError as e:
            logging.error(f"Error getting user interest companies: {str(e)}")
            return []