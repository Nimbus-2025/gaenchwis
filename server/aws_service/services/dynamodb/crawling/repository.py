from typing import Dict, List, Union, Optional
from datetime import datetime
from ..common.base_repository import BaseRepository
from ..common.constants import TableNames
from .models import Company, JobPosting, Tag, JobTag

class DynamoDBRepository(BaseRepository):
    def __init__(self, table_name: str):
        super().__init__(table_name)
        self.dynamodb = AWSClient.get_client('dynamodb')
        self.table = self.dynamodb.Table(self.collection_name)
        
    def health_check(self) -> bool:
        try:
            self.table.table_status
            return True
        except Exception:
            return False
    
    def save(self, item: Union[Dict, List[Dict]]) -> bool:
        try:
            if isinstance(item, list):
                with self.table.batch_writer(
                    TableName=self.collection_name
                ) as batch:
                    for i in item:
                        batch.put_item(Item=i)
                return True
            else:
                response = self.table.put_item(
                    TableName=self.collection_name,
                    Item=item
                )
                return response['ResponseMetadata']['HTTPStatusCode'] == 200
        except Exception as e:
            raise StorageException(f"DynamoDB 저장 실패: {str(e)}")
    
    def get(self, 
            id: Optional[Union[str, List[str]]] = None,
            query: Optional[Dict] = None) -> Union[Dict, List[Dict]]:
        try:
            if id:
                if isinstance(id, list):
                    response = self.table.batch_get_item(
                        RequestItems={
                            self.collection_name: {
                                'Keys': [{'id': {'S': i}} for i in id]
                            }
                        }
                    )
                    return response['Responses'][self.collection_name]
                else:
                    response = self.table.get_item(
                        TableName=self.collection_name,
                        Key={'id': {'S': id}}
                    )
                    return response.get('Item')
            else:
                response = self.table.scan(
                    TableName=self.collection_name,
                    FilterExpression=query if query else None
                )
                return response['Items']
        except Exception as e:
            raise StorageException(f"DynamoDB 조회 실패: {str(e)}")
    
    def update(self, id: str, data: Dict) -> bool:
        try:
            update_expression = "SET " + ", ".join(f"#{k} = :{k}" for k in data)
            expression_attribute_names = {f"#{k}": k for k in data}
            expression_attribute_values = {f":{k}": v for k, v in data.items()}
            
            response = self.table.update_item(
                TableName=self.collection_name,
                Key={'id': {'S': id}},
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values
            )
            return response['ResponseMetadata']['HTTPStatusCode'] == 200
        except Exception as e:
            raise StorageException(f"DynamoDB 수정 실패: {str(e)}")
    
    def delete(self, id: Union[str, List[str]]) -> bool:
        try:
            if isinstance(id, list):
                with self.table.batch_writer(
                    TableName=self.collection_name
                ) as batch:
                    for i in id:
                        batch.delete_item(Key={'id': {'S': i}})
                return True
            else:
                response = self.table.delete_item(
                    TableName=self.collection_name,
                    Key={'id': {'S': id}}
                )
                return response['ResponseMetadata']['HTTPStatusCode'] == 200
        except Exception as e:
            raise StorageException(f"DynamoDB 삭제 실패: {str(e)}")