from datetime import datetime
from typing import List, Dict
import logging
import uuid
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import re

from app.core.aws_client import AWSClient
from app.schemas.scheduling_schema import GeneralScheduleCreate
from app.core.config import config

class ScheduleRepository:
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
            self.table = self.dynamodb.Table('schedules')  # 일반 일정 테이블
            self.apply_table = self.dynamodb.Table('applies')  # 취업 일정 테이블
            self.job_postings = self.dynamodb.Table('job_postings')

        except Exception as e:
            logging.error(f"Error initializing repository: {str(e)}")
            raise

    def create_general_schedule(self, user_id: str, request: GeneralScheduleCreate) -> str:
        try:
            schedule_id = str(uuid.uuid4())
            current_time = datetime.now().isoformat()
            
            schedule_item = {
                'PK': f"USER#{user_id}",
                'SK': f"SCHEDULE#{schedule_id}",
                'GSI1PK': "SCHEDULE#ALL",
                'GSI1SK': request.date,
                'schedule_id': schedule_id,
                'user_id': user_id,
                'schedule_date': request.date,
                'schedule_title': request.title,
                'schedule_content': request.content,
                'is_completed': False,
                'created_at': current_time,
                'updated_at': current_time
            }
            
            self.table.put_item(Item=schedule_item)
            return schedule_id
            
        except Exception as e:
            raise Exception(f"Failed to create schedule: {str(e)}")

    def get_schedules(self, user_id: str, schedule_type: str) -> List[Dict]:
        """일정 조회"""

        print(f"get_schedules: {user_id}, {schedule_type}")

        try:
            if schedule_type == "general":
                return self._get_general_schedules(user_id)
            elif schedule_type == "apply":
                return self._get_apply_schedules(user_id)
            else:  # all
                general_schedules = self._get_general_schedules(user_id)
                apply_schedules = self._get_apply_schedules(user_id)
                
                return general_schedules + apply_schedules
                
        except Exception as e:
            raise Exception(f"Failed to get schedules: {str(e)}")

    def _get_general_schedules(self, user_id: str) -> List[Dict]:
        """일반 일정 조회"""
        try:
            print(f"_get_general_schedules - user_id: {user_id}")
            
            response = self.table.query(
                KeyConditionExpression=Key('PK').eq(f"USER#{user_id}") & 
                Key('SK').begins_with('SCHEDULE#')
            )
            schedules = response.get('Items', [])
            print(f"Found schedules before filtering: {schedules}")
            
            # 해당 월의 일정만 필터링
            filtered_schedules = [
                schedule for schedule in schedules 
                if schedule['schedule_date']
            ]
            print(f"Filtered schedules: {filtered_schedules}")
            
            return filtered_schedules
            
        except Exception as e:
            print(f"Error in _get_general_schedules: {str(e)}")
            raise Exception(f"Failed to get general schedules: {str(e)}")

    def _get_apply_schedules(self, user_id: str) -> List[Dict]:
        """취업 일정 조회"""
        try:
            response = self.apply_table.query(
                KeyConditionExpression=Key('PK').eq(f"USER#{user_id}") & 
                Key('SK').begins_with('APPLY#')
            )
            apply_schedules = response.get('Items', [])
            print(apply_schedules)
            formatted_schedules = []
            for apply in apply_schedules:
                deadline = apply.get('deadline_date')

                if deadline and deadline !="채용시":
                    deadline = re.sub(r"\(.*\)", "", deadline).strip()
                    current_year = datetime.now().year
                    deadline = datetime.strptime(f"{current_year}.{deadline}", "%Y.%m.%d").strftime("%Y%m%d")


                job = self.job_postings.query(
                    IndexName="JobPostId",
                    KeyConditionExpression="post_id = :post_id",
                    ExpressionAttributeValues={
                        ":post_id": apply['SK'].split("#")[1]
                    }
                )
                
                formatted_schedules.append({
                    'schedule_type': "applies",
                    'company': f"{job['Items'][0]['company_name']}",
                    'schedule_id': f"{apply['post_id']}",
                    'schedule_deadline': deadline,
                    'document_result_date': apply.get('document_result_date'),
                    'interview_date': apply.get('interview_date'),
                    'final_date': apply.get('final_date'),
                    'schedule_title': f"{apply['post_name']}",
                    'schedule_content': f"{apply.get('memo')}",
                    'is_completes': apply.get('is_resulted', False),
                })
                        
            return formatted_schedules
            
        except Exception as e:
            raise Exception(f"Failed to get apply schedules: {str(e)}")


    def _get_date_field(self, date_type: str) -> str:
        """날짜 타입에 따른 필드명 반환"""
        date_fields = {
            '공고 마감일': 'deadline_date',
            '서류 합격 발표': 'document_result_date',
            '면접 일정': 'deadline_date',
            '최종발표': 'final_date'
        }
        return date_fields.get(date_type)

    def update_general_schedule(self, user_id: str, schedule_id: str, request: Dict) -> bool:
        """일정을 수정합니다."""
        try:
            # 먼저 기존 항목이 있는지 확인
            response = self.table.get_item(
                Key={
                    'PK': f"USER#{user_id}",
                    'SK': f"SCHEDULE#{schedule_id}"
                }
            )
            
            if 'Item' not in response:
                raise Exception("일정을 찾을 수 없습니다")

            existing_item = response['Item']
            current_time = datetime.now().isoformat()
            
            # 기존 항목 업데이트
            updated_item = existing_item.copy()  # 기존 항목을 복사
            
            # 필요한 필드만 업데이트
            updated_item.update({
                'schedule_title': request['title'],
                'schedule_date': request['date'],
                'schedule_content': request.get('content', ''),
                'GSI1SK': request['date'],  # GSI도 함께 업데이트
                'updated_at': current_time
            })
            
            # 전체 항목을 새로운 데이터로 업데이트
            self.table.put_item(Item=updated_item)
            
            return True
            
        except Exception as e:
            raise Exception(f"Failed to update schedule: {str(e)}")
    
    def update_apply_schedule(self, user_id: str, schedule_id: str, request: Dict) -> bool:
        """일정을 수정합니다."""
        try:
            # 먼저 기존 항목이 있는지 확인
            response = self.apply_table.get_item(
                Key={
                    'PK': f"USER#{user_id}",
                    'SK': f"APPLY#{schedule_id}"
                }
            )
            
            if 'Item' not in response:
                raise Exception("지원 공고을 찾을 수 없습니다")

            existing_item = response['Item']
            current_time = datetime.now().isoformat()
            
            # 기존 항목 업데이트
            updated_item = existing_item.copy()  # 기존 항목을 복사
            
            # 필요한 필드만 업데이트
            updated_item.update({
                'document_result_date':request['documentResultDate'],
                'final_date':request['finalDate'],
                'interview_date':request['interviewDate'],
                'memo':request['content'],
                'updated_at': current_time
            })
            
            self.apply_table.put_item(Item=updated_item)
            
            return True
            
        except Exception as e:
            raise Exception(f"Failed to update schedule: {str(e)}")


    def delete_general_schedule(self, user_id: str, schedule_id: str) -> bool:
        """일반 일정을 삭제합니다."""
        try:
            # 먼저 일정이 존재하는지 확인
            response = self.table.get_item(
                Key={
                    'PK': f"USER#{user_id}",
                    'SK': f"SCHEDULE#{schedule_id}"
                }
            )
            
            if 'Item' not in response:
                raise ValueError("일정을 찾을 수 없습니다")
                
            # 일정 삭제
            self.table.delete_item(
                Key={
                    'PK': f"USER#{user_id}",
                    'SK': f"SCHEDULE#{schedule_id}"
                }
            )
            
            return True
            
        except Exception as e:
            raise Exception(f"Failed to delete schedule: {str(e)}")

    def toggle_schedule_completion(self, user_id: str, schedule_id: str) -> bool:
        """일정의 완료 상태를 토글합니다."""
        try:
            # 먼저 일정이 존재하는지 확인
            response = self.table.get_item(
                Key={
                    'PK': f"USER#{user_id}",
                    'SK': f"SCHEDULE#{schedule_id}"
                }
            )
            
            if 'Item' not in response:
                raise ValueError("일정을 찾을 수 없습니다")

            existing_item = response['Item']
            current_time = datetime.now().isoformat()
            
            # 현재 완료 상태의 반대로 토글
            is_completed = not existing_item.get('is_completed', False)
            
            # 기존 항목 업데이트
            updated_item = existing_item.copy()
            updated_item.update({
                'is_completed': is_completed,
                'updated_at': current_time
            })
            
            # 전체 항목을 새로운 데이터로 업데이트
            self.table.put_item(Item=updated_item)
            
            return is_completed
            
        except Exception as e:
            raise Exception(f"Failed to toggle schedule completion: {str(e)}")