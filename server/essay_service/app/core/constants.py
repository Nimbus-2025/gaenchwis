from enum import Enum
from .config import Config

config = Config()

class TableNames(str, Enum):
    ESSAYS = config.dynamodb.essays_table
    ESSAY_JOB_POSTINGS = config.dynamodb.essay_job_postings_table
    APPLIES = config.dynamodb.applies
    JOB_POSTINGS = config.dynamodb.job_postings

class IndexNames:
    # Crawling related indexes
    COMPANY_NAME_GSI = 'CompanyNameIndex'
    JOB_STATUS_GSI = 'StatusIndex'
    REC_IDX_GSI = 'RecIdx'
    POST_ID_GSI = 'JobPostId'
    TAG_CATEGORY_NAME_GSI = 'TagCategoryNameIndex'
    JOB_TAG_INVERSE_GSI = 'JobTagInverseIndex'
        
    # User related indexes
    USER_DATA_GSI = 'UserIndex'
    USER_TAG_INVERSE_GSI = 'UserTagIndex'
    SCHEDULE_GSI = 'ScheduleIndex'
    BOOKMARK_GSI = 'BookmarkIndex'
    APPLY_GSI = 'ApplyIndex'
    INTEREST_COMPANY_GSI = 'InterestCompanyIndex'
        
    # Essay related indexes
    ESSAY_DATE_GSI = 'EssayDateIndex'
    ESSAY_POST_INVERSE_GSI = 'EssayPostInverseIndex'

DB_CONSTANTS = {
    'batch_size': 25,
    'max_retries': 3,
    'timeout': 30,
}