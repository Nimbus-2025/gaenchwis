from .config import Config

config = Config()

class TableNames:
    APPLIES = config.dynamodb.applies
    ESSAY_JOB_POSTINGS = config.dynamodb.essay_job_postings  # 'essay_job_postings'라는 기본값을 가짐
    ESSAYS = config.dynamodb.essays
    JOB_POSTINGS = config.dynamodb.job_postings
    BOOKMARKS = config.dynamodb.bookmarks 
    INTEREST_COMPANIES = config.dynamodb.interest_companies 
    
class IndexNames:
    POST_ESSAY_GSI = 'EssayJobPostingIndex'
    BOOKMARK_GSI = 'BookmarkIndex'
    INTEREST_COMPANY_GSI = 'InterestCompanyIndex'
    
DB_CONSTANTS = {
    'batch_size': 25,
    'max_retries': 3,
    'timeout': 30,
}