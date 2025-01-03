from dataclasses import dataclass
from typing import Dict

@dataclass
class AWSConfig:
    region: str
    dynamodb_table: str
    s3_bucket: str
    
    @classmethod
    def from_env(cls) -> 'AWSConfig':
        import os
        return cls(
            region=os.getenv('AWS_REGION', 'ap-northeast-2'),
            dynamodb_table=os.getenv('DYNAMODB_TABLE'),
            s3_bucket=os.getenv('S3_BUCKET')
        )