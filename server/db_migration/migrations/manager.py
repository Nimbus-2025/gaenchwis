import time
from botocore.exceptions import ClientError
from typing import Dict, Any
from utils.aws_client import AWSClient
from schemas import ALL_TABLES

class MigrationManager:
    def __init__(self):
        self.dynamodb = AWSClient.get_client('dynamodb')

    def table_exists(self, table_name: str) -> bool:
        try:
            self.dynamodb.Table(table_name).load()
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                return False
            raise

    def wait_for_table_deletion(self, table_name: str, max_attempts: int = 10) -> None:
        """테이블이 완전히 삭제될 때까지 대기"""
        for _ in range(max_attempts):
            try:
                self.dynamodb.describe_table(TableName=table_name)
                print(f"Waiting for {table_name} to be deleted...")
                time.sleep(5)  # 5초 대기
            except ClientError as e:
                if e.response['Error']['Code'] == 'ResourceNotFoundException':
                    return  # 테이블이 완전히 삭제됨
                raise
        raise Exception(f"Table {table_name} deletion timeout")

    def delete_table(self, table_name: str) -> None:
        """테이블 삭제"""
        try:
            if self.table_exists(table_name):
                self.dynamodb.Table(table_name).delete()
                print(f"Deleted table: {table_name}")
                self.wait_for_table_deletion(table_name)  
        except ClientError as e:
            print(f"Error deleting table {table_name}: {str(e)}")
            raise

    def create_table(self, table_schema: Dict[str, Any]) -> None:
        """테이블 생성"""
        try:
            self.dynamodb.create_table(**table_schema)
            print(f"Created table: {table_schema['TableName']}")
        except ClientError as e:
            print(f"Error creating table {table_schema['TableName']}: {str(e)}")
            raise

    def recreate_tables(self):
        """모든 테이블을 삭제하고 재생성"""
        # 1. 기존 테이블 모두 삭제
        for table in ALL_TABLES:
            self.delete_table(table['TableName'])
        
        # 2. 새로운 스키마로 테이블 생성
        for table in ALL_TABLES:
            self.create_table(table)