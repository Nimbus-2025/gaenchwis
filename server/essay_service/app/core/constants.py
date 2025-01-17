from enum import Enum
from .config import Config

config = Config()

class TableNames(str, Enum):
    ESSAYS = config.dynamodb.essays_table
    ESSAY_JOB_POSTINGS = config.dynamodb.essay_job_postings_table
    APPLIES = config.dynamodb.applies
    JOB_POSTINGS = config.dynamodb.job_postings

class IndexNames:
    ESSAY_GSI = 'EssayIndex'
    ESSAY_JOB_POSTING_GSI = 'EssayJobPostingIndex',

DB_CONSTANTS = {
    'batch_size': 25,
    'max_retries': 3,
    'timeout': 30,
}