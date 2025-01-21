from constants.table import TableNames
from constants.index import IndexNames

# 공통 GSI 설정
COMMON_GSI_SETTINGS = {
    'Projection': {'ProjectionType': 'ALL'}
}

USERS_TABLE = {
    'TableName': TableNames.USERS,
    'KeySchema': [
        {'AttributeName': 'PK', 'KeyType': 'HASH'}
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'PK', 'AttributeType': 'S'},
        {'AttributeName': 'GSI1PK', 'AttributeType': 'S'},
        {'AttributeName': 'GSI1SK', 'AttributeType': 'S'}
    ],
    'GlobalSecondaryIndexes': [
        {
            'IndexName': IndexNames.DynamoDB.USER_DATA_GSI,          # 가입일자순 전체 유저 조회
            'KeySchema': [
                {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'}, # USER#ALL
                {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'} # <created_at>
            ],
            **COMMON_GSI_SETTINGS
        }
    ],
    'BillingMode': 'PAY_PER_REQUEST'
}

USER_TAGS_TABLE = {
    'TableName': TableNames.USER_TAGS,
    'KeySchema': [
        {'AttributeName': 'PK', 'KeyType': 'HASH'},
        {'AttributeName': 'SK', 'KeyType': 'RANGE'}
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'PK', 'AttributeType': 'S'},
        {'AttributeName': 'SK', 'AttributeType': 'S'},
        {'AttributeName': 'GSI1PK', 'AttributeType': 'S'},
        {'AttributeName': 'GSI1SK', 'AttributeType': 'S'}
    ],
    'GlobalSecondaryIndexes': [
        {
            'IndexName': IndexNames.DynamoDB.USER_TAG_INVERSE_GSI,       # 태그별 유저 조회를 위한 역인덱스
            'KeySchema': [
                {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'}, # TAG#<tag_id>
                {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'} # USER#<user_id>
            ],
            **COMMON_GSI_SETTINGS
        }
    ],
    'BillingMode': 'PAY_PER_REQUEST'
}

SCHEDULES_TABLE = {
    'TableName': TableNames.SCHEDULES,
    'KeySchema': [
        {'AttributeName': 'PK', 'KeyType': 'HASH'},
        {'AttributeName': 'SK', 'KeyType': 'RANGE'}
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'PK', 'AttributeType': 'S'},
        {'AttributeName': 'SK', 'AttributeType': 'S'},
        {'AttributeName': 'GSI1PK', 'AttributeType': 'S'},
        {'AttributeName': 'GSI1SK', 'AttributeType': 'S'}
    ],
    'GlobalSecondaryIndexes': [
        {
            'IndexName': IndexNames.DynamoDB.SCHEDULE_GSI,      # 일정 날짜순 전체 조회
            'KeySchema': [  
                {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'}, # 일정 날짜순 전체 조회
                {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'} # <schedule_date>
            ],
            **COMMON_GSI_SETTINGS
        }
    ],
    'BillingMode': 'PAY_PER_REQUEST'
}

BOOKMARKS_TABLE = {
    'TableName': TableNames.BOOKMARKS,
    'KeySchema': [
        {'AttributeName': 'PK', 'KeyType': 'HASH'},
        {'AttributeName': 'SK', 'KeyType': 'RANGE'}
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'PK', 'AttributeType': 'S'},
        {'AttributeName': 'SK', 'AttributeType': 'S'},
        {'AttributeName': 'GSI1PK', 'AttributeType': 'S'},
        {'AttributeName': 'GSI1SK', 'AttributeType': 'S'}
    ],
    'GlobalSecondaryIndexes': [
        {
            'IndexName': IndexNames.DynamoDB.BOOKMARK_GSI,      # 공고별 북마크한 유저 조회를 위한 역인덱스
            'KeySchema': [
                {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'}, # POST#<post_id>
                {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'} # USER#<user_id>
            ],
            **COMMON_GSI_SETTINGS
        }
    ],
    'BillingMode': 'PAY_PER_REQUEST'
}

APPLIES_TABLE = {
    'TableName': TableNames.APPLIES,
    'KeySchema': [
        {'AttributeName': 'PK', 'KeyType': 'HASH'},
        {'AttributeName': 'SK', 'KeyType': 'RANGE'}
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'PK', 'AttributeType': 'S'},
        {'AttributeName': 'SK', 'AttributeType': 'S'},
        {'AttributeName': 'GSI1PK', 'AttributeType': 'S'},
        {'AttributeName': 'GSI1SK', 'AttributeType': 'S'}
    ],
    'GlobalSecondaryIndexes': [
        {
            'IndexName': IndexNames.DynamoDB.APPLY_GSI,     # 공고별 지원일자순 조회
            'KeySchema': [
                {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'},     # POST#<post_id>
                {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'}     # <apply_date>
            ],
            **COMMON_GSI_SETTINGS
        }
    ],
    'BillingMode': 'PAY_PER_REQUEST'
}

INTEREST_COMPANIES_TABLE = {
    'TableName': TableNames.INTEREST_COMPANIES,
    'KeySchema': [
        {'AttributeName': 'PK', 'KeyType': 'HASH'},
        {'AttributeName': 'SK', 'KeyType': 'RANGE'}
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'PK', 'AttributeType': 'S'},
        {'AttributeName': 'SK', 'AttributeType': 'S'},
        {'AttributeName': 'GSI1PK', 'AttributeType': 'S'},
        {'AttributeName': 'GSI1SK', 'AttributeType': 'S'}
    ],
    'GlobalSecondaryIndexes': [
        {
            'IndexName': IndexNames.DynamoDB.INTEREST_COMPANY_GSI,  # 기업별 관심 유저 조회를 위한 역인덱스
            'KeySchema': [
                {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'},     # COMPANY#<company_id>
                {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'}     # USER#<user_id>
            ],
            **COMMON_GSI_SETTINGS
        }
    ],
    'BillingMode': 'PAY_PER_REQUEST'
}

# 전체 테이블 리스트
TABLES = [
    USERS_TABLE,
    USER_TAGS_TABLE,
    SCHEDULES_TABLE,
    BOOKMARKS_TABLE,
    APPLIES_TABLE,
    INTEREST_COMPANIES_TABLE
]