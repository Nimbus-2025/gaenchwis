from typing import Dict, List, Optional
from ...base import BaseRepository
from ...exceptions import StorageException

class DynamoDBRepository(BaseRepository):
    def __init__(self, table_name: str):
        super().__init__('dynamodb', table_name)
        self.table = self.resource.Table(table_name)
    
    def health_check(self) -> bool:
        try:
            self.table.scan(Limit=1)
            return True
        except Exception:
            return False
    
    def save_items(self, items: List[Dict]) -> bool:
        try:
            with self.table.batch_writer() as batch:
                for item in items:
                    batch.put_item(Item=item)
            return True
        except Exception as e:
            raise StorageException(f"DynamoDB 배치 저장 실패: {str(e)}")
    
    def save_item(self, item: Dict) -> bool:
        try:
            self.table.put_item(Item=item)
            return True
        except Exception as e:
            raise StorageException(f"DynamoDB 저장 실패: {str(e)}")
    
    def get_items(self, query: Optional[Dict] = None) -> List[Dict]:
        try:
            if query:
                response = self.table.scan(
                    FilterExpression=query.get('filter_expression'),
                    ExpressionAttributeValues=query.get('expression_values')
                )
            else:
                response = self.table.scan()
            return response['Items']
        except Exception as e:
            raise StorageException(f"DynamoDB 조회 실패: {str(e)}")
    
    def get_item(self, id: str) -> Optional[Dict]:
        try:
            response = self.table.get_item(Key={'id': id})
            return response.get('Item')
        except Exception as e:
            raise StorageException(f"DynamoDB 조회 실패: {str(e)}")
    
    def update_item(self, id: str, data: Dict) -> bool:
        try:
            update_expression = "SET " + ", ".join(f"#{k} = :{k}" for k in data.keys())
            expression_values = {f":{k}": v for k, v in data.items()}
            expression_names = {f"#{k}": k for k in data.keys()}
            
            self.table.update_item(
                Key={'id': id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
                ExpressionAttributeNames=expression_names
            )
            return True
        except Exception as e:
            raise StorageException(f"DynamoDB 업데이트 실패: {str(e)}")
    
    def delete_item(self, id: str) -> bool:
        try:
            self.table.delete_item(Key={'id': id})
            return True
        except Exception as e:
            raise StorageException(f"DynamoDB 삭제 실패: {str(e)}")
    
    def batch_delete(self, ids: List[str]) -> bool:
        try:
            with self.table.batch_writer() as batch:
                for id in ids:
                    batch.delete_item(Key={'id': id})
            return True
        except Exception as e:
            raise StorageException(f"DynamoDB 배치 삭제 실패: {str(e)}")
    
    def query(self, 
            index_name: str, 
            key_condition: Dict,
            filter_expression: Optional[Dict] = None) -> List[Dict]:
        try:
            params = {
                'IndexName': index_name,
                'KeyConditionExpression': key_condition
            }
            if filter_expression:
                params['FilterExpression'] = filter_expression
            
            response = self.table.query(**params)
            return response['Items']
        except Exception as e:
            raise StorageException(f"DynamoDB 쿼리 실패: {str(e)}")