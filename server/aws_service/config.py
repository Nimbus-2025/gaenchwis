from dataclasses import dataclass
from typing import Optional
import os

@dataclass
class AWSConfig:
    """AWS 설정"""
    region: str = os.getenv('AWS_REGION', 'ap-northeast-2')
    access_key: Optional[str] = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key: Optional[str] = os.getenv('AWS_SECRET_ACCESS_KEY')

@dataclass
class MongoDBConfig:
    """MongoDB 설정"""
    uri: str = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
    database: str = os.getenv('MONGODB_DATABASE', 'crawler_db')