from abc import ABC, abstractmethod
import boto3
from typing import Dict, List, Optional, Any
from .exceptions import AWSServiceException

class AWSBaseService(ABC):
    def __init__(self, service_name: str):
        try:
            self.client = boto3.client(service_name)
            self.resource = boto3.resource(service_name)
        except Exception as e:
            raise AWSServiceException(f"{service_name} 초기화 실패: {str(e)}")
        
        # 서비스 상태 확인
        @abstractmethod
        def health_check(self) -> bool:
            pass
        
        def get_client(self):
            return self.client
        
        def get_resource(self):
            return self.resource
        
class BaseRepository(AWSBaseService):
    # Repository 기본 클래스

    def __init__(self, service_name: str, table_name: str):
        super().__init__(service_name)
        self.table_name = table_name
        
    @abstractmethod
    def save_items(self, items: List[Dict]) -> bool:
        # 여러 아이템 저장 
        pass
    
    @abstractmethod
    def save_item(self, item: Dict) -> bool:
        # 단일 아이템 저장 
        pass
    
    @abstractmethod
    def get_items(self, query: Optional[Dict] = None) -> List[Dict]:
        # 조건에 맞는 아이템들 조회
        pass
    
    @abstractmethod
    def get_item(self, id: str) -> List[Dict]:
        # 단일 아이템들 조회
        pass
    
    @abstractmethod
    def update_item(self, id: str, data: Dict) -> bool:
        # 아이템 업데이트
        pass
    
    @abstractmethod
    def delete_item(self, id: str) -> bool:
        # 아이템 삭제
        pass
    
    @abstractmethod
    def batch_delete(self, ids: List[str]) -> bool:
        # 여러 아이템 삭제
        pass
    
    @abstractmethod
    def query(self,
            index_name: str,
            key_condition: Dict,
            filter_expression: Optional[Dict] = None) -> List[Dict]:
        # 인덱스를 사용한 쿼리
        pass
    
# class LocalRepository(BaseRepository):
#     # 로컬 테스트용 Repository 기본 클래스
#     def __init__(self, table_name: str):
#         self.table_name = table_name
        
#     def health_check(self) -> bool:
#         # 로컬 저장소 상태 확인
#         try:
#             self.get_items(limit=1)
#             return True
#         except Exception:
#             return False
    