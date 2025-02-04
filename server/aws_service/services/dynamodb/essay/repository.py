from typing import Dict, List, Union, Optional
from datetime import datetime
from botocore.exceptions import ClientError
from aws_service.services.dynamodb.common.base_repository import BaseRepository
from aws_service.services.dynamodb.common.exceptions import (
    ValidationException, 
    OperationException
)

class EssayRepository(BaseRepository):
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

    # Essay 도메인 특화 메서드들
    def get_essay_contents(self, essay_id: str) -> List[Dict]:
        """자소서 내용 이력 조회"""
        try:
            return self.get_by_keys(f"ESSAY#{essay_id}", "CONTENT#")
        except Exception as e:
            raise OperationException(f"자소서 내용 조회 중 오류 발생: {str(e)}")

    def get_latest_essay_content(self, essay_id: str) -> Optional[Dict]:
        """자소서 최신 내용 조회"""
        try:
            contents = self.get_by_keys(f"ESSAY#{essay_id}", "CONTENT#")
            if not contents:
                return None
            return sorted(contents, key=lambda x: x['version'], reverse=True)[0]
        except Exception as e:
            raise OperationException(f"최신 자소서 내용 조회 중 오류 발생: {str(e)}")

    def get_essay_job_postings(self, essay_id: str) -> List[Dict]:
        """자소서와 연결된 채용공고 목록 조회"""
        try:
            return self.get_by_keys(f"ESSAY#{essay_id}", "POST#")
        except Exception as e:
            raise OperationException(f"연결된 채용공고 조회 중 오류 발생: {str(e)}")

    def get_user_essays(self, user_id: str) -> List[Dict]:
        """사용자의 자소서 목록 조회"""
        try:
            return self.get_by_keys(f"USER#{user_id}", "ESSAY#")
        except Exception as e:
            raise OperationException(f"자소서 목록 조회 중 오류 발생: {str(e)}")

    def get_essay_versions(self, essay_id: str) -> List[Dict]:
        """자소서의 모든 버전 조회"""
        try:
            contents = self.get_by_keys(f"ESSAY#{essay_id}", "CONTENT#")
            return sorted(contents, key=lambda x: x['version'])
        except Exception as e:
            raise OperationException(f"자소서 버전 조회 중 오류 발생: {str(e)}")

    def save_essay_version(self, essay_id: str, content: str) -> bool:
        """새로운 자소서 버전 저장"""
        try:
            versions = self.get_essay_versions(essay_id)
            new_version = len(versions) + 1
            
            essay_content = {
                'PK': f"ESSAY#{essay_id}",
                'SK': f"CONTENT#{new_version}",
                'essay_id': essay_id,
                'essay_content': content,
                'version': new_version,
                'created_at': datetime.now().isoformat(),
                'GSI1PK': "CONTENT#ALL",
                'GSI1SK': datetime.now().isoformat()
            }
            
            return bool(self.create(essay_content))
        except Exception as e:
            raise OperationException(f"자소서 버전 저장 중 오류 발생: {str(e)}")

    def link_essay_to_job(self, essay_id: str, post_id: str) -> bool:
        """자소서와 채용공고 연결"""
        try:
            link = {
                'PK': f"ESSAY#{essay_id}",
                'SK': f"POST#{post_id}",
                'essay_id': essay_id,
                'post_id': post_id,
                'created_at': datetime.now().isoformat(),
                'GSI1PK': f"POST#{post_id}",
                'GSI1SK': f"ESSAY#{essay_id}"
            }
            
            return bool(self.create(link))
        except Exception as e:
            raise OperationException(f"자소서-채용공고 연결 중 오류 발생: {str(e)}")