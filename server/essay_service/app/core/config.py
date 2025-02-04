from dataclasses import dataclass, field
from typing import Optional
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

env_path = Path(__file__).parent.parent.parent.parent / '.env'
logger.info(f"Loading .env from: {env_path}")
logger.info(f"Env file exists: {env_path.exists()}")
load_dotenv(dotenv_path=env_path)

logger.info("Initial AWS Credentials Check:")
logger.info(f"AWS_REGION: {os.getenv('AWS_REGION')}")

@dataclass
class AWSConfig:
    region: str = os.getenv('AWS_REGION', 'ap-northeast-2')

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