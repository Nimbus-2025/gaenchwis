from dataclasses import dataclass, field
from typing import Optional
import os

@dataclass
class AWSConfig:
    region: str = os.getenv('AWS_REGION', 'ap-northeast-2')
    access_key: Optional[str] = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key: Optional[str] = os.getenv('AWS_SECRET_ACCESS_KEY')

@dataclass
class DynamoDBConfig:
    schedules_table: str = os.getenv('DYNAMODB_SCHEDULES_TABLE', 'schedules')
    schedules_job_postings_table: str = os.getenv('DYNAMODB_SCHEDULES_JOB_POSTINGS_TABLE', 'schedule_job_postings')

@dataclass
class Config:
    aws: AWSConfig = field(default_factory=lambda: AWSConfig())
    dynamodb: DynamoDBConfig = field(default_factory=lambda: DynamoDBConfig())

config = Config() 