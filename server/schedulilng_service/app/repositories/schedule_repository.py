import boto3
from boto3.dynamodb.conditions import Key, Attr
from typing import List, Dict
import uuid
from datetime import datetime
from app.schemas.scheduling_schema import GeneralScheduleCreate
from app.core.config import config
import logging

class ScheduleRepository:
    def __init__(self):
        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name=config.aws.region,
            aws_access_key_id=config.aws.access_key,
            aws_secret_access_key=config.aws.secret_key
        )
        self.table = self.dynamodb.Table(config.dynamodb.schedules_table)
        # TODO: Apply 테이블 연결 필요
        # self.apply_table = self.dynamodb.Table('applies')

    async def create_general_schedule(self, user_id: str, request: GeneralScheduleCreate) -> str:
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
                'schedule_type': 'general',
                'created_at': current_time,
                'updated_at': current_time
            }
            
            self.table.put_item(Item=schedule_item)
            return schedule_id
            
        except Exception as e:
            raise Exception(f"Failed to create schedule: {str(e)}")

    async def get_schedules(self, user_id: str, schedule_type: str = "all") -> List[Dict]:
        """일정 조회"""
        try:
            schedules = []
            
            # 일반 일정 조회
            if schedule_type in ["all", "general"]:
                general_response = self.table.query(
                    KeyConditionExpression=Key('PK').eq(f"USER#{user_id}")
                )
                general_schedules = general_response.get('Items', [])
                for schedule in general_schedules:
                    schedule['schedule_type'] = 'general'
                schedules.extend(general_schedules)

            # TODO: 취업 일정 조회 기능 구현 예정
            if schedule_type in ["all", "apply"]:
                # TODO: applies 테이블에서 취업 일정 조회
                # apply_schedules = await self.get_apply_schedules(user_id)
                # for schedule in apply_schedules:
                #     schedule['schedule_type'] = 'apply'
                # schedules.extend(apply_schedules)
                pass

            # 날짜순 정렬
            schedules.sort(key=lambda x: x['schedule_date'])
            return schedules
                
        except Exception as e:
            raise Exception(f"Failed to get schedules: {str(e)}")

    # TODO: Apply 일정 조회 기능 구현 예정
    async def get_apply_schedules(self, user_id: str) -> List[Dict]:
        """취업 일정 조회"""
        try:
            # TODO: applies 테이블 구조에 맞춰 쿼리 작성 필요
            # response = self.apply_table.query(
            #     KeyConditionExpression=Key('user_id').eq(user_id)
            # )
            # apply_schedules = response.get('Items', [])
            # 
            # # 필요한 형식으로 데이터 변환
            # formatted_schedules = []
            # for apply in apply_schedules:
            #     formatted_schedules.append({
            #         'schedule_id': apply['id'],
            #         'schedule_date': apply['date'],
            #         'schedule_title': apply['company_name'],
            #         'schedule_content': apply['position'],
            #         'created_at': apply['created_at'],
            #         'updated_at': apply['updated_at']
            #     })
            # return formatted_schedules
            return []
            
        except Exception as e:
            raise Exception(f"Failed to get apply schedules: {str(e)}")

    # TODO: 일정 상세 조회 기능 구현 예정
    async def get_schedule_detail(self, user_id: str, schedule_id: str) -> Dict:
        """특정 일정의 상세 정보를 조회합니다."""
        try:
            response = self.table.get_item(
                Key={
                    'PK': f"USER#{user_id}",
                    'SK': f"SCHEDULE#{schedule_id}"
                }
            )
            
            if 'Item' not in response:
                raise ValueError("일정을 찾을 수 없습니다")
                
            schedule = response['Item']
            
            return {
                'title': schedule['schedule_title'],
                'date': schedule['schedule_date'],
                'content': schedule.get('schedule_content', '')
            }
            
        except Exception as e:
            raise Exception(f"Failed to get schedule detail: {str(e)}")


    async def update_general_schedule(self, user_id: str, schedule_id: str, request: Dict) -> bool:
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

    async def get_general_schedules(self, user_id: str) -> List[Dict]:
        """일반 일정만 조회"""
        try:
            logging.info(f"Getting general schedules for user {user_id}")
            response = self.table.query(
                KeyConditionExpression=Key('PK').eq(f"USER#{user_id}")
            )
            
            schedules = response.get('Items', [])
            
            # 모든 필드를 포함하여 반환
            formatted_schedules = []
            for schedule in schedules:
                formatted_schedules.append({
                    'schedule_id': schedule['schedule_id'],
                    'title': schedule['schedule_title'],
                    'date': schedule['schedule_date'],
                    'content': schedule.get('schedule_content', ''),
                    'schedule_type': schedule['schedule_type'],
                    'created_at': schedule['created_at'],
                    'updated_at': schedule['updated_at']
                })
            
            logging.info(f"Found {len(formatted_schedules)} schedules")
            return formatted_schedules
            
        except Exception as e:
            logging.error(f"Error in get_general_schedules: {str(e)}")
            raise Exception(f"Failed to get general schedules: {str(e)}")