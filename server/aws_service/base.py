from abc import ABC, abstractmethod
import boto3
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
        
        