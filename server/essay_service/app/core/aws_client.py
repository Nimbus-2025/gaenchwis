import boto3
from typing import Dict, Any
from .config import config

class AWSClient:
    _instances: Dict[str, Any] = {}
    
    @classmethod
    def get_client(cls, service_name: str):
        if service_name not in cls._instances:
            try:
                if service_name == 'dynamodb':
                    cls._instances[service_name] = boto3.resource(
                        service_name,
                        aws_access_key_id=config.aws.access_key,
                        aws_secret_access_key=config.aws.secret_key,
                        region_name=config.aws.region
                    )
                else:
                    cls._instances[service_name] = boto3.client(
                        service_name,
                        aws_access_key_id=config.aws.access_key,
                        aws_secret_access_key=config.aws.secret_key,
                        region_name=config.aws.region
                    )
            except Exception as e:
                raise Exception(f"AWS 클라이언트 생성 실패: {str(e)}")
        return cls._instances[service_name]