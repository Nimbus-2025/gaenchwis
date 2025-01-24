import boto3
from typing import Dict, Any
import logging
from .config import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 핸들러 추가
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

class AWSClient:
    _instances: Dict[str, Any] = {}
    
    @classmethod
    def get_client(cls, service_name: str):
        if service_name not in cls._instances:
            try:
                # logger.info(f"Creating new {service_name} client...")
                # logger.info(f"Using region: {config.aws.region}")
                # logger.info(f"Access key exists: {bool(config.aws.access_key)}")
                
                # credentials = {
                #     'aws_access_key_id': config.aws.access_key,
                #     'aws_secret_access_key': config.aws.secret_key,
                #     'region_name': config.aws.region or 'ap-northeast-2'  # 기본 리전 설정
                # }

                if service_name == 'dynamodb':
                    cls._instances[service_name] = boto3.resource(
                        service_name,
                        # **credentials
                    )
                else:
                    cls._instances[service_name] = boto3.client(
                        service_name,
                        # **credentials
                    )
                logger.info(f"{service_name} client created successfully")
                    
            except Exception as e:
                logger.error(f"AWS 클라이언트 생성 실패: {str(e)}")
                raise

        return cls._instances[service_name]