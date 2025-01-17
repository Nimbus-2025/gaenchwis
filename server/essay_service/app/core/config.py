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
    essays_table: str = os.getenv('DYNAMODB_ESSAYS_TABLE', 'essays')
    essay_job_postings_table: str = os.getenv('DYNAMODB_ESSAY_JOB_POSTINGS_TABLE', 'essay_job_postings')
    applies: str = os.getenv('DYNAMODB_APPLIES', 'applies')
    job_postings: str = os.getenv('DYNAMODB_JOB_POSTINGS', 'job_postings')

@dataclass
class Config:
    aws: AWSConfig = field(default_factory=lambda: AWSConfig())
    dynamodb: DynamoDBConfig = field(default_factory=lambda: DynamoDBConfig())

config = Config() 