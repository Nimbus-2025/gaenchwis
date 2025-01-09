import os
from typing import Dict, List, Union, Optional
import pymongo
from ...base import BaseRepository
from ...config import MongoDBConfig
from ...exceptions import StorageException

class MongoDBRepository(BaseRepository):
    def __init__(self, collection_name: str):
        super().__init__(collection_name)
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://admin:password@mongodb:27017/crawler_db?authSource=admin')
        # config = MongoDBConfig()
        
        try:
            self.client = pymongo.MongoClient(mongodb_uri)
            db_name = mongodb_uri.split('/')[-1].split('?')[0]
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
            
            # 연결 테스트
            self.client.admin.command('ping')
            print(f"MongoDB 연결 성공: {collection_name} 컬렉션")
        except Exception as e:
            print(f"MongoDB 연결 에러: {str(e)}")
            raise StorageException(f"MongoDB 연결 실패: {str(e)}")
    
    def health_check(self) -> bool:
        try:
            self.client.admin.command('ping')
            return True
        except Exception:
            return False
    
    def save(self, item: Union[Dict, List[Dict]]) -> bool:
        try:
            if isinstance(item, list):
                result = self.collection.insert_many(item)
                return len(result.inserted_ids) == len(item)
            else:
                result = self.collection.insert_one(item)
                return bool(result.inserted_id)
        except Exception as e:
            raise StorageException(f"MongoDB 저장 실패: {str(e)}")
    
    def get(self, 
            id: Optional[Union[str, List[str]]] = None,
            query: Optional[Dict] = None) -> Union[Dict, List[Dict]]:
        try:
            if id:
                if isinstance(id, list):
                    return list(self.collection.find({'_id': {'$in': id}}))
                return self.collection.find_one({'_id': id})
            return list(self.collection.find(query or {}))
        except Exception as e:
            raise StorageException(f"MongoDB 조회 실패: {str(e)}")
    
    def update(self, id: str, data: Dict, upsert: bool = False) -> bool:
        """
        데이터 업데이트
        Args:
            id (str): 업데이트할 문서의 ID
            data (Dict): 업데이트할 데이터
            upsert (bool): 문서가 없을 경우 새로 생성할지 여부
        """
        try:
            result = self.collection.update_one(
                {'_id': id},
                {'$set': data},
                upsert=upsert
            )
            return bool(result.modified_count or result.upserted_id)
        except Exception as e:
            raise StorageException(f"MongoDB 수정 실패: {str(e)}")
    
    def delete(self, id: Union[str, List[str]]) -> bool:
        try:
            if isinstance(id, list):
                result = self.collection.delete_many({'_id': {'$in': id}})
                return result.deleted_count == len(id)
            else:
                result = self.collection.delete_one({'_id': id})
                return bool(result.deleted_count)
        except Exception as e:
            raise StorageException(f"MongoDB 삭제 실패: {str(e)}")