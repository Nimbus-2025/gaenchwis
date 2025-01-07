import boto3
from typing import Dict
from .config import AWSConfig
from .exceptions import StorageException

class AWSClient:
    """AWS 클라이언트 관리"""
    _instances: Dict = {}
    
    @classmethod
    def get_client(cls, service_name: str):
        """AWS 서비스 클라이언트 반환"""
        if service_name not in cls._instances:
            try:
                config = AWSConfig()
                cls._instances[service_name] = boto3.client(
                    service_name,
                    region_name=config.region,
                    aws_access_key_id=config.access_key,
                    aws_secret_access_key=config.secret_key
                )
            except Exception as e:
                raise StorageException(f"AWS {service_name} 연결 실패: {str(e)}")
        return cls._instances[service_name]