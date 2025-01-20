class IndexNames:
    class DynamoDB:
        # Crawling related indexes
        STATUS_GSI = 'StatusIndex'
        DATE_GSI = 'DateIndex'
        TAG_GSI = 'TagIndex'
        REC_IDX_GSI = 'PostId'
        
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