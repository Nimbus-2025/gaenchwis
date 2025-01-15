import boto3
from typing import Dict, Any
import os
from botocore.exceptions import ClientError

class AWSClient:
    _instances: Dict[str, Any] = {}
    
    @classmethod
    def get_client(cls, service_name: str):
        if service_name not in cls._instances:
            try:
                # 환경 변수에서 AWS 인증 정보 가져오기
                aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
                aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
                aws_region = os.getenv('AWS_REGION', 'ap-northeast-2')
                
                # DynamoDB는 resource로, 나머지는 client로 생성
                if service_name == 'dynamodb':
                    cls._instances[service_name] = boto3.resource(
                        service_name,
                        aws_access_key_id=aws_access_key,
                        aws_secret_access_key=aws_secret_key,
                        region_name=aws_region
                    )
                else:
                    cls._instances[service_name] = boto3.client(
                        service_name,
                        aws_access_key_id=aws_access_key,
                        aws_secret_access_key=aws_secret_key,
                        region_name=aws_region
                    )
                    
            except Exception as e:
                raise ClientError(
                    error_response={
                        'Error': {
                            'Code': 'ClientInitializationError',
                            'Message': f"AWS 클라이언트 생성 실패: {str(e)}"
                        }
                    },
                    operation_name='ClientInitialization'
                )
                
        return cls._instances[service_name]

    @classmethod
    def clear_instances(cls):
        """테스트를 위한 인스턴스 초기화 메서드"""
        cls._instances.clear()