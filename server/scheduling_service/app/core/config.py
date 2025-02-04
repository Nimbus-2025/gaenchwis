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
    schedules_table: str = os.getenv('DYNAMODB_SCHEDULES_TABLE', 'schedules')
    schedules_job_postings_table: str = os.getenv('DYNAMODB_SCHEDULES_JOB_POSTINGS_TABLE', 'schedule_job_postings')
    schedules_applies: str = os.getenv('DYNAMODB_APPLIES_TABLE', 'applies')

@dataclass
class Config:
    aws: AWSConfig = field(default_factory=lambda: AWSConfig())
    dynamodb: DynamoDBConfig = field(default_factory=lambda: DynamoDBConfig())

config = Config() 