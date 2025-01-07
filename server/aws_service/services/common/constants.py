from enum import Enum

class TableNames:
    COMPANIES = 'companies'
    JOB_POSTINGS = 'job_postings'
    TAGS = 'tags'
    JOB_TAGS = 'job_tags'

class IndexNames:
    # MongoDB Index Names
    COMPANY_DATE = 'company_date_index'
    STATUS_DATE = 'status_date_index'
    TAG_COUNT = 'tag_count_index'
    
    # DynamoDB GSI Names
    STATUS_GSI = 'StatusIndex'
    DATE_GSI = 'DateIndex'
    TAG_GSI = 'TagIndex' 