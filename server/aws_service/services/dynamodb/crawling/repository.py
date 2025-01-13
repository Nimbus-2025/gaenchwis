from typing import Dict, List, Union, Optional
from botocore.exceptions import ClientError
from ....services.dynamodb.common.base_repository import BaseRepository
from ....services.dynamodb.common.exceptions import (
    ValidationException,
    OperationException
)

class CrawlingRepository(BaseRepository):
    def _create_key_condition_expression(self, pk: str, sk: Optional[str] = None) -> Dict:
        """키 조건 표현식 생성"""
        try:
            if not pk:
                raise ValidationException("파티션 키는 필수입니다.")
            
            if sk:
                return {
                    'KeyConditionExpression': 'PK = :pk AND SK = :sk',
                    'ExpressionAttributeValues': {':pk': pk, ':sk': sk}
                }
            return {
                'KeyConditionExpression': 'PK = :pk',
                'ExpressionAttributeValues': {':pk': pk}
            }
        except Exception as e:
            if isinstance(e, ValidationException):
                raise
            raise OperationException(f"키 조건식 생성 중 오류 발생: {str(e)}")

    def batch_create(self, items: List[Dict]) -> bool:
        """여러 아이템 일괄 생성"""
        try:
            if not isinstance(items, list):
                raise ValidationException("items는 리스트 형태여야 합니다")
                
            with self.table.batch_writer() as batch:
                for item in items:
                    if not isinstance(item, dict):
                        raise ValidationException("모든 아이템은 딕셔너리 형태여야 합니다")
                    batch.put_item(Item=item)
            return True
        except ClientError as e:
            self._handle_dynamodb_error(e, "일괄 생성")
        except Exception as e:
            if isinstance(e, ValidationException):
                raise
            raise OperationException(f"일괄 생성 중 오류 발생: {str(e)}")

    def get_by_keys(self, pk: str, sk: Optional[str] = None) -> Union[Dict, List[Dict]]:
        """키를 사용한 아이템 조회"""
        try:
            key_condition = self._create_key_condition_expression(pk, sk)
            response = self.table.query(**key_condition)
            return response.get('Items', [])
        except ClientError as e:
            self._handle_dynamodb_error(e, "키 조회")
        except Exception as e:
            raise OperationException(f"키 조회 중 오류 발생: {str(e)}")

    def get_by_index(self, index_name: str, pk: str, sk: Optional[str] = None) -> List[Dict]:
        """인덱스를 사용한 아이템 조회"""
        try:
            key_condition = self._create_key_condition_expression(pk, sk)
            response = self.table.query(
                IndexName=index_name,
                **key_condition
            )
            return response.get('Items', [])
        except ClientError as e:
            self._handle_dynamodb_error(e, "인덱스 조회")
        except Exception as e:
            raise OperationException(f"인덱스 조회 중 오류 발생: {str(e)}")

    def conditional_update(self, pk: str, sk: str, data: Dict, condition_expression: str) -> bool:
        """조건부 아이템 업데이트"""
        try:
            update_expression = self._create_update_expression(data)
            response = self.table.update_item(
                Key={'PK': pk, 'SK': sk},
                ConditionExpression=condition_expression,
                **update_expression
            )
            return response['ResponseMetadata']['HTTPStatusCode'] == 200
        except ClientError as e:
            self._handle_dynamodb_error(e, "조건부 업데이트")
        except Exception as e:
            if isinstance(e, ValidationException):
                raise
            raise OperationException(f"조건부 업데이트 중 오류 발생: {str(e)}")

    def conditional_delete(self, pk: str, sk: str, condition_expression: str) -> bool:
        """조건부 아이템 삭제"""
        try:
            response = self.table.delete_item(
                Key={'PK': pk, 'SK': sk},
                ConditionExpression=condition_expression
            )
            return response['ResponseMetadata']['HTTPStatusCode'] == 200
        except ClientError as e:
            self._handle_dynamodb_error(e, "조건부 삭제")
        except Exception as e:
            raise OperationException(f"조건부 삭제 중 오류 발생: {str(e)}")

    def batch_delete(self, items: List[Dict[str, str]]) -> bool:
        """여러 아이템 일괄 삭제"""
        try:
            with self.table.batch_writer() as batch:
                for item in items:
                    if 'PK' not in item or 'SK' not in item:
                        raise ValidationException("모든 아이템은 PK와 SK를 포함해야 합니다")
                    batch.delete_item(Key={'PK': item['PK'], 'SK': item['SK']})
            return True
        except ClientError as e:
            self._handle_dynamodb_error(e, "일괄 삭제")
        except Exception as e:
            if isinstance(e, ValidationException):
                raise
            raise OperationException(f"일괄 삭제 중 오류 발생: {str(e)}")
        