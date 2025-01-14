import boto3
from typing import Dict, Any
from .config import Config

class AWSClient:
    _instances: Dict[str, Any] = {}
    
    @classmethod
    def get_client(cls, service_name: str):
        if service_name not in cls._instances:
            try:
                config = Config()
                if service_name == 'dynamodb':
                    cls._instances[service_name] = boto3.resource(
                        service_name,
                        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
                        region_name=config.AWS_REGION
                    )
                else:
                    cls._instances[service_name] = boto3.client(
                        service_name,
                        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
                        region_name=config.AWS_REGION
                    )
            except Exception as e:
                raise Exception(f"AWS 클라이언트 생성 실패: {str(e)}")
        return cls._instances[service_name]    
