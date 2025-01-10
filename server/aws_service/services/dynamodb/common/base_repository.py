from abc import ABC, abstractmethod
from typing import Dict, List, Union, Optional
from datetime import datetime

# 저장소 기본 인터페이스
class BaseRepository(ABC):
    def __init__(self, table_name: str):
        self.table_name = table_name
    
    # 저장소 연결 상태 확인
    @abstractmethod
    def health_check(self) -> bool:
        pass
    
    # 단일/다중 아이템 저장
    @abstractmethod
    def save(self, item: Union[Dict, List[Dict]]) -> bool:
        pass
    
    # 파티션 키/정렬 키 또는 쿼리 조건으로 아이템 조회
    @abstractmethod
    def get(self, 
            key: Optional[Dict] = None, 
            query: Optional[Dict] = None) -> Union[Dict, List[Dict]]:
        pass
    
    # 아이템 수정 
    @abstractmethod
    def update(self, 
               key: str, 
               updates: Dict,
               conditions: Optional[Dict] = None) -> bool:
        pass

    # 단일/다중 아이템 삭제
    @abstractmethod
    def delete(self, 
               id: Union[str, List[str]],
               conditions: Optional[Dict] = None) -> bool:
        pass