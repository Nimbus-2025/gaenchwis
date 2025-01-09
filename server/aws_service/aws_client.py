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
            if service_name == 'dynamodb':
                cls._instances[service_name] = boto3.resource(
                    service_name,
                    aws_access_key_id='AKIAWX2IF5YDAMM7FH4V',
                    aws_secret_access_key='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',
                    region_name='ap-northeast-2'
                )
            else: 
                cls._instances[service_name] = boto3.client(service_name)    
        return cls._instances[service_name]