from typing import Dict, List, Union, Optional
from ...base import BaseRepository
from ...aws_client import AWSClient
from ...exceptions import StorageException

class DynamoDBRepository(BaseRepository):
    def __init__(self, table_name: str):
        super().__init__(table_name)
        self.client = AWSClient.get_client('dynamodb')
        
    def health_check(self) -> bool:
        try:
            self.client.describe_table(TableName=self.collection_name)
            return True
        except Exception:
            return False
    
    def save(self, item: Union[Dict, List[Dict]]) -> bool:
        try:
            if isinstance(item, list):
                with self.client.batch_writer(
                    TableName=self.collection_name
                ) as batch:
                    for i in item:
                        batch.put_item(Item=i)
                return True
            else:
                response = self.client.put_item(
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
                    response = self.client.batch_get_item(
                        RequestItems={
                            self.collection_name: {
                                'Keys': [{'id': {'S': i}} for i in id]
                            }
                        }
                    )
                    return response['Responses'][self.collection_name]
                else:
                    response = self.client.get_item(
                        TableName=self.collection_name,
                        Key={'id': {'S': id}}
                    )
                    return response.get('Item')
            else:
                response = self.client.scan(
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
            
            response = self.client.update_item(
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
                with self.client.batch_writer(
                    TableName=self.collection_name
                ) as batch:
                    for i in id:
                        batch.delete_item(Key={'id': {'S': i}})
                return True
            else:
                response = self.client.delete_item(
                    TableName=self.collection_name,
                    Key={'id': {'S': id}}
                )
                return response['ResponseMetadata']['HTTPStatusCode'] == 200
        except Exception as e:
            raise StorageException(f"DynamoDB 삭제 실패: {str(e)}")