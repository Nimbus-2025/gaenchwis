from constants.table import TableNames
from constants.index import IndexNames

# 공통 GSI 설정
COMMON_GSI_SETTINGS = {
    'Projection': {'ProjectionType': 'ALL'}
}

# DynamoDB 테이블 스키마 정의
COMPANIES_TABLE = {
    'TableName': TableNames.COMPANIES,
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
            'IndexName': IndexNames.DynamoDB.COMPANY_NAME_GSI,        # 회사명으로 조회하기 위한 인덱스
            'KeySchema': [
                {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'},       # COMPANY#ALL
                {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'}       # <company_name>
            ],
            **COMMON_GSI_SETTINGS
        }
    ],
    'BillingMode': 'PAY_PER_REQUEST'
}

JOB_POSTINGS_TABLE = {
    'TableName': TableNames.JOB_POSTINGS,
    'KeySchema': [
        {'AttributeName': 'PK', 'KeyType': 'HASH'},
        {'AttributeName': 'SK', 'KeyType': 'RANGE'}
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'PK', 'AttributeType': 'S'},
        {'AttributeName': 'SK', 'AttributeType': 'S'},
        {'AttributeName': 'GSI1PK', 'AttributeType': 'S'},
        {'AttributeName': 'GSI1SK', 'AttributeType': 'S'},
        {'AttributeName': 'rec_idx', 'AttributeType': 'S'},
        {'AttributeName': 'post_id', 'AttributeType': 'S'},
    ],
    'GlobalSecondaryIndexes': [
        {
            'IndexName': IndexNames.DynamoDB.JOB_STATUS_GSI,        # 상태별 + 생성일자순 조회
            'KeySchema': [
                {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'}, # STATUS#<status>
                {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'} # <created_at>
            ],
            **COMMON_GSI_SETTINGS
        },
        {
            'IndexName': IndexNames.DynamoDB.REC_IDX_GSI,  # rec_idx를 위한 새로운 GSI
            'KeySchema': [
                {'AttributeName': 'rec_idx', 'KeyType': 'HASH'}  # rec_idx를 파티션 키로 사용
            ],
            **COMMON_GSI_SETTINGS
        },
        {
            'IndexName': IndexNames.DynamoDB.POST_ID_GSI,  # post_id를 위한 새로운 GSI
            'KeySchema': [
                {'AttributeName': 'post_id', 'KeyType': 'HASH'}  # post_id를 파티션 키로 사용
            ],
            **COMMON_GSI_SETTINGS
        }
    ],
    'BillingMode': 'PAY_PER_REQUEST'
}

TAGS_TABLE = {
    'TableName': 'tags',
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
            'IndexName': IndexNames.DynamoDB.TAG_CATEGORY_NAME_GSI,  # 카테고리별 태그명 검색을 위한 GSI
            'KeySchema': [
                {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'},  # TAG#<category>
                {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'}  # <tag_name>
            ],
            **COMMON_GSI_SETTINGS
        }
    ],
    'BillingMode': 'PAY_PER_REQUEST'
}

JOB_TAGS_TABLE = {
    'TableName': TableNames.JOB_TAGS,
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
            'IndexName': IndexNames.DynamoDB.JOB_TAG_INVERSE_GSI,  # 태그별 공고 조회를 위한 GSI
            'KeySchema': [
                {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'}, # TAG#<tag_id>
                {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'} # JOB#<job_id>
            ],
            **COMMON_GSI_SETTINGS
        }
    ],
    'BillingMode': 'PAY_PER_REQUEST'
}

# 테이블 생성 설정을 리스트로 관리
TABLES = [
    COMPANIES_TABLE,
    JOB_POSTINGS_TABLE,
    TAGS_TABLE,
    JOB_TAGS_TABLE
]