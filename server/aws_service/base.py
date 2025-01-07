from abc import ABC, abstractmethod
from typing import Dict, List, Union, Optional

class BaseRepository(ABC):
    """저장소 기본 인터페이스"""
    
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
    
    @abstractmethod
    def health_check(self) -> bool:
        """저장소 연결 상태 확인"""
        pass
    
    @abstractmethod
    def save(self, item: Union[Dict, List[Dict]]) -> bool:
        """단일/다중 아이템 저장"""
        pass
    
    @abstractmethod
    def get(self, 
            id: Optional[Union[str, List[str]]] = None, 
            query: Optional[Dict] = None) -> Union[Dict, List[Dict]]:
        """ID 또는 쿼리 조건으로 아이템 조회"""
        pass
    
    @abstractmethod
    def update(self, id: str, data: Dict) -> bool:
        """아이템 수정"""
        pass
    
    @abstractmethod
    def delete(self, id: Union[str, List[str]]) -> bool:
        """단일/다중 아이템 삭제"""
        pass