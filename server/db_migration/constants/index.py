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