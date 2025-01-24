from dataclasses import dataclass, field
from typing import Optional
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# 1. 로깅 설정 
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 핸들러 추가
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# 환경변수 로드 
env_path = Path(__file__).parent.parent.parent.parent / '.env'
logger.info(f"Loading .env from: {env_path}")
logger.info(f"Env file exists: {env_path.exists()}")
load_dotenv(dotenv_path=env_path)

@dataclass
class AWSConfig:
    region: str = os.getenv('AWS_REGION', 'ap-northeast-2')

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