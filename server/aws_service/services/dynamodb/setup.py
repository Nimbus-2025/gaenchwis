from typing import Optional
from boto3.resources.base import ServiceResource
from .table_schemas import TABLES

def setup_dynamodb(dynamodb: ServiceResource, region: Optional[str] = None):
    """DynamoDB 테이블들을 생성합니다."""
    try:
        # 1. 기존 테이블 확인
        existing_tables = dynamodb.meta.client.list_tables()['TableNames']
        
        # 2. 테이블 생성
        for table_schema in TABLES:  # 여러 테이블 스키마를 순회
            table_name = table_schema['TableName']
            
            if table_name not in existing_tables:
                # 2.1 테이블 생성
                table = dynamodb.create_table(**table_schema)
                
                # 2.2 테이블 생성 완료 대기
                waiter = table.meta.client.get_waiter('table_exists')
                waiter.wait(
                    TableName=table_name,
                    WaiterConfig={
                        'Delay': 5,  # 5초마다 확인
                        'MaxAttempts': 20  # 최대 100초 대기
                    }
                )
                print(f"테이블 생성 완료: {table_name}")
            else:
                print(f"테이블이 이미 존재합니다: {table_name}")
                
        print("DynamoDB 설정 완료")
    except Exception as e:
        print(f"DynamoDB 설정 중 오류 발생: {str(e)}")
        raise e