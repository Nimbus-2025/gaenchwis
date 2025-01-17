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
    applies: str = os.getenv('DYNAMODB_APPLIES', 'applies')
    essay_job_postings: str = os.getenv('DYNAMODB_ESSAY_JOB_POSTINGS', 'essay_job_postings')
    essays: str = os.getenv('DYNAMODB_ESSAYS', 'essays') 
    job_postings: str = os.getenv('DYNAMODB_JOB_POSTINGS', 'job_postings')
    bookmarks: str = os.getenv('DYNAMODB_BOOKMARKS', 'bookmarks')  
    interest_companies: str = os.getenv('DYNAMODB_INTEREST_COMPANIES', 'interest_companies')
    
@dataclass
class Config:
    aws: AWSConfig = field(default_factory=lambda: AWSConfig())
    dynamodb: DynamoDBConfig = field(default_factory=lambda: DynamoDBConfig())

config = Config() 

print("DynamoDB Config values:")
print(f"applies: {config.dynamodb.applies}")
print(f"essay_job_postings: {config.dynamodb.essay_job_postings}")
print(f"essays: {config.dynamodb.essays}")
print(f"job_postings: {config.dynamodb.job_postings}")
print(f"bookmarks: {config.dynamodb.bookmarks}") 