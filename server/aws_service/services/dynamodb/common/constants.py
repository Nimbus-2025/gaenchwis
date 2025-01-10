import os
from enum import Enum
from .enums import StorageType

STORAGE_TYPES = [storage_type.value for storage_type in StorageType]

class TableNames(str, Enum):
    COMPANIES = os.getenv('DYNAMODB_COMPANIES_TABLE', 'companies')
    JOB_POSTINGS = os.getenv('DYNAMODB_JOB_POSTINGS_TABLE', 'job_postings')
    TAGS = os.getenv('DYNAMODB_TAGS_TABLE', 'tags')
    JOB_TAGS = os.getenv('DYNAMODB_JOB_TAGS_TABLE', 'job_tags')

class IndexNames:
    class MongoDB:
        COMPANY_DATE = 'company_date_index'
        STATUS_DATE = 'status_date_index'
        TAG_COUNT = 'tag_count_index'
    
    class DynamoDB:
        STATUS_GSI = 'StatusIndex'
        DATE_GSI = 'DateIndex'
        TAG_GSI = 'TagIndex'
        
DB_CONSTANTS = {
    'batch_size': 25,
    'max_retries': 3,
    'timeout': 30,
}