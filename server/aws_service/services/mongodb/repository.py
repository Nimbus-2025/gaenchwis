from typing import Dict, List, Optional
from pymongo import MongoClient
from ...base import BaseRepository
from ...exceptions import StorageException

class MongoDBRepository(BaseRepository):
    def __init__(self, collection_name: str):
        super().__init__('mongodb', collection_name)
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['crawler_db']
        self.collection = self.db[collection_name]
    
    def health_check(self) -> bool:
        try:
            self.collection.find_one()
            return True
        except Exception:
            return False
    
    def save_items(self, items: List[Dict]) -> bool:
        try:
            self.collection.insert_many(items)
            return True
        except Exception as e:
            raise StorageException(f"MongoDB 배치 저장 실패: {str(e)}")
    
    def save_item(self, item: Dict) -> bool:
        try:
            self.collection.insert_one(item)
            return True
        except Exception as e:
            raise StorageException(f"MongoDB 저장 실패: {str(e)}")
    
    def get_items(self, query: Optional[Dict] = None) -> List[Dict]:
        try:
            return list(self.collection.find(query or {}))
        except Exception as e:
            raise StorageException(f"MongoDB 조회 실패: {str(e)}")
    
    def get_item(self, id: str) -> Optional[Dict]:
        try:
            return self.collection.find_one({"_id": id})
        except Exception as e:
            raise StorageException(f"MongoDB 조회 실패: {str(e)}")
    
    def update_item(self, id: str, data: Dict) -> bool:
        try:
            result = self.collection.update_one(
                {"_id": id},
                {"$set": data}
            )
            return result.modified_count > 0
        except Exception as e:
            raise StorageException(f"MongoDB 업데이트 실패: {str(e)}")
    
    def delete_item(self, id: str) -> bool:
        try:
            result = self.collection.delete_one({"_id": id})
            return result.deleted_count > 0
        except Exception as e:
            raise StorageException(f"MongoDB 삭제 실패: {str(e)}")
    
    def batch_delete(self, ids: List[str]) -> bool:
        try:
            result = self.collection.delete_many({"_id": {"$in": ids}})
            return result.deleted_count == len(ids)
        except Exception as e:
            raise StorageException(f"MongoDB 배치 삭제 실패: {str(e)}")
    
    def query(self, 
            index_name: str, 
            key_condition: Dict,
            filter_expression: Optional[Dict] = None) -> List[Dict]:
        try:
            query = {**key_condition}
            if filter_expression:
                query.update(filter_expression)
            
            return list(self.collection.find(query))
        except Exception as e:
            raise StorageException(f"MongoDB 쿼리 실패: {str(e)}")