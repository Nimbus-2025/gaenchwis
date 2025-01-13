from typing import Dict, List, Union, Optional
from botocore.exceptions import ClientError
from aws_service.aws_client import AWSClient
from .exceptions import (
    DynamoDBException,
    TableNotFoundException,
    ConditionCheckFailedException,
    ValidationException,
    OperationException
)

class BaseRepository:
    def __init__(self, table_name: str):
        try:
            self.table_name = table_name
            self.dynamodb= AWSClient.get_client('dynamodb')
            self.table = self.dynamodb.Table(self.table_name)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                raise TableNotFoundException(f"테이블을 찾을 수 없습니다: {table_name}")
            raise DynamoDBException(f"DynamoDB 초기화 중 오류 발생: {str(e)}")   
        
    def create(self, item: Dict) -> Dict:
        """아이템 생성"""
        try:
            self.table.put_item(Item=item)
            return item
        except ClientError as e:
            self._handle_dynamodb_error(e, "생성")

    def get(self, key: Dict) -> Optional[Dict]:
        """아이템 조회"""
        try:
            response = self.table.get_item(Key=key)
            return response.get('Item')
        except ClientError as e:
            self._handle_dynamodb_error(e, "조회")

    def update(self, key: Dict, data: Dict) -> Dict:
        """아이템 업데이트"""
        try:
            update_expression = self._create_update_expression(data)
            response = self.table.update_item(
                Key=key,
                ReturnValues="ALL_NEW",
                **update_expression
            )
            return response.get('Attributes', {})
        except ClientError as e:
            self._handle_dynamodb_error(e, "업데이트")

    def delete(self, key: Dict) -> None:
        """아이템 삭제"""
        try:
            self.table.delete_item(Key=key)
        except ClientError as e:
            self._handle_dynamodb_error(e, "삭제")

    def scan(self, **kwargs) -> List[Dict]:
        """전체 아이템 스캔"""
        try:
            response = self.table.scan(**kwargs)
            return response.get('Items', [])
        except ClientError as e:
            self._handle_dynamodb_error(e, "스캔")
            
    def _create_update_expression(self, data: Dict) -> Dict:
        """업데이트 표현식 생성"""
        try:
            update_attrs = {k: v for k, v in data.items() if k not in ['PK', 'SK']}
            
            if not update_attrs:
                raise ValidationException("업데이트할 속성이 없습니다.")

            expression_parts = []
            expression_names = {}
            expression_values = {}

            for key in update_attrs.keys():
                expression_parts.append(f"#{key} = :{key}")
                expression_names[f"#{key}"] = key
                expression_values[f":{key}"] = update_attrs[key]

            return {
                'UpdateExpression': 'SET ' + ', '.join(expression_parts),
                'ExpressionAttributeNames': expression_names,
                'ExpressionAttributeValues': expression_values
            }
        except Exception as e:
            if isinstance(e, ValidationException):
                raise
            raise OperationException(f"업데이트 표현식 생성 중 오류 발생: {str(e)}")

    def _handle_dynamodb_error(self, error: ClientError, operation: str) -> None:
        """DynamoDB 에러 처리"""
        error_code = error.response['Error']['Code']
        error_message = error.response['Error']['Message']
        
        if error_code == 'ResourceNotFoundException':
            raise TableNotFoundException(f"테이블을 찾을 수 없습니다: {self.table_name}")
        elif error_code == 'ConditionalCheckFailedException':
            raise ConditionCheckFailedException(f"{operation} 중 조건 검사 실패")
        elif error_code == 'ValidationException':
            raise ValidationException(f"{operation} 중 유효성 검증 실패: {error_message}")
        else:
            raise OperationException(f"{operation} 중 오류 발생: {error_message}")
            