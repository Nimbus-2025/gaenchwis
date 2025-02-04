import os
from enum import Enum
from aws_service.services.dynamodb.common.enums import StorageType

STORAGE_TYPES = [storage_type.value for storage_type in StorageType]

class TableNames(str, Enum):
    # Crawling related tables
    COMPANIES = os.getenv('DYNAMODB_COMPANIES_TABLE', 'companies')
    JOB_POSTINGS = os.getenv('DYNAMODB_JOB_POSTINGS_TABLE', 'job_postings')
    TAGS = os.getenv('DYNAMODB_TAGS_TABLE', 'tags')
    JOB_TAGS = os.getenv('DYNAMODB_JOB_TAGS_TABLE', 'job_tags')
    
    # User related tables
    USERS = os.getenv('DYNAMODB_USERS_TABLE', 'users')
    # USER_IMAGES = os.getenv('DYNAMODB_USER_IMAGES_TABLE', 'user_images')
    USER_TAGS = os.getenv('DYNAMODB_USER_TAGS_TABLE', 'user_tags')
    SCHEDULES = os.getenv('DYNAMODB_SCHEDULES_TABLE', 'schedules')
    BOOKMARKS = os.getenv('DYNAMODB_BOOKMARKS_TABLE', 'bookmarks')
    APPLIES = os.getenv('DYNAMODB_APPLIES_TABLE', 'applies')
    INTEREST_COMPANIES = os.getenv('DYNAMODB_INTEREST_COMPANIES_TABLE', 'interest_companies')
    
    # Essay related tables
    ESSAYS = os.getenv('DYNAMODB_ESSAYS_TABLE', 'essays')
    ESSAY_JOB_POSTINGS = os.getenv('DYNAMODB_ESSAY_JOB_POSTINGS_TABLE', 'essay_job_postings')

class IndexNames:
    class DynamoDB:
        # Crawling related indexes
        STATUS_GSI = 'StatusIndex'
        DATE_GSI = 'DateIndex'
        TAG_GSI = 'TagIndex'
        
        # User related indexes
        USER_GSI = 'UserIndex'
        # IMAGE_GSI = 'ImageIndex'
        SCHEDULE_GSI = 'ScheduleIndex'
        BOOKMARK_GSI = 'BookmarkIndex'
        APPLY_GSI = 'ApplyIndex'
        INTEREST_COMPANY_GSI = 'InterestCompanyIndex'
        
        # Essay related indexes
        ESSAY_GSI = 'EssayIndex'
        ESSAY_JOB_POSTING_GSI = 'EssayJobPostingIndex'
        
DB_CONSTANTS = {
    'batch_size': 25,
    'max_retries': 3,
    'timeout': 30,
}