import os
from enum import Enum
from .enums import StorageType

# 프로젝트 루트 디렉토리 경로 설정
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class CrawlerConfig:
    # 크롤러 관련 설정 
    STORAGE_TYPES = [storage_type.value for storage_type in StorageType]
    
    # User Agent 목록  
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59'
    ]

    # 출력 디렉토리 설정 
    OUTPUT_DIRS = {
        'saramin': os.path.join(PROJECT_ROOT, 'output', 'saramin'),
        'jobkorea': 'jobkorea_crawling_results'
    }

    # 크롤링 URL 설정 
    URLS = {
        'saramin': 'https://www.saramin.co.kr/zf_user/jobs/list/job-category?cat_mcls=2&loc_mcd=101000%2C102000%2C108000&panel_type=&search_optional_item=n&search_done=y&panel_count=y&preview=y&page=1&sort=RD&page_count=100',
        # 'jobkorea': 'https://www.jobkorea.co.kr/recruit/joblist?menucode=duty'
    }

class TableNames(str, Enum):
    # Crawling related tables
    COMPANIES = os.getenv('DYNAMODB_COMPANIES_TABLE', 'companies')
    JOB_POSTINGS = os.getenv('DYNAMODB_JOB_POSTINGS_TABLE', 'job_postings')
    TAGS = os.getenv('DYNAMODB_TAGS_TABLE', 'tags')
    JOB_TAGS = os.getenv('DYNAMODB_JOB_TAGS_TABLE', 'job_tags')
    
    # User related tables
    USERS = os.getenv('DYNAMODB_USERS_TABLE', 'users')
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

# 모든 출력 디렉토리 생성
for dir_path in CrawlerConfig.OUTPUT_DIRS.values():
    os.makedirs(dir_path, exist_ok=True)