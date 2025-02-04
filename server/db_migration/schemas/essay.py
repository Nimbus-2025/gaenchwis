from constants.table import TableNames
from constants.index import IndexNames

# 공통 GSI 설정
COMMON_GSI_SETTINGS = {
    'Projection': {'ProjectionType': 'ALL'}
}

ESSAYS_TABLE = {
    'TableName': TableNames.ESSAYS,
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
            'IndexName': IndexNames.DynamoDB.ESSAY_DATE_GSI,             # 생성일자순 전체 조회
            'KeySchema': [
                {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'},     # ESSAY#ALL
                {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'}     # <created_at>
            ],
            **COMMON_GSI_SETTINGS
        }
    ],
    'BillingMode': 'PAY_PER_REQUEST'
}

ESSAY_JOB_POSTINGS_TABLE = {
    'TableName': TableNames.ESSAY_JOB_POSTINGS,
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
            'IndexName': IndexNames.DynamoDB.ESSAY_POST_INVERSE_GSI,     # 공고별 자소서 조회를 위한 역인덱스
            'KeySchema': [
                {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'},         # POST#<post_id>
                {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'}         # ESSAY#<essay_id>
            ],
            **COMMON_GSI_SETTINGS
        }
    ],
    'BillingMode': 'PAY_PER_REQUEST'
}

# 전체 테이블 리스트
TABLES = [
    ESSAYS_TABLE,
    ESSAY_JOB_POSTINGS_TABLE
]