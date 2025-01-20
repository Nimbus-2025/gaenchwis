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
            'IndexName': 'GSI1',
            'KeySchema': [
                {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'},
                {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'}
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
        {'AttributeName': 'GSI2PK', 'AttributeType': 'S'},
        {'AttributeName': 'GSI2SK', 'AttributeType': 'S'},
        {'AttributeName': 'rec_idx', 'AttributeType': 'S'}
    ],
    'GlobalSecondaryIndexes': [
        {
            'IndexName': IndexNames.DynamoDB.STATUS_GSI,  
            'KeySchema': [
                {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'},
                {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'}
            ],
            **COMMON_GSI_SETTINGS
        },
        {
            'IndexName': IndexNames.DynamoDB.DATE_GSI,  
            'KeySchema': [
                {'AttributeName': 'GSI2PK', 'KeyType': 'HASH'},
                {'AttributeName': 'GSI2SK', 'KeyType': 'RANGE'}
            ],
            **COMMON_GSI_SETTINGS
        },
        {
            'IndexName': IndexNames.DynamoDB.REC_IDX_GSI,  # rec_idx를 위한 새로운 GSI
            'KeySchema': [
                {'AttributeName': 'rec_idx', 'KeyType': 'HASH'}  # rec_idx를 파티션 키로 사용
            ],
            **COMMON_GSI_SETTINGS
        }
    ],
    'BillingMode': 'PAY_PER_REQUEST'
}

TAGS_TABLE = {
    'TableName': TableNames.TAGS,
    'KeySchema': [
        {'AttributeName': 'PK', 'KeyType': 'HASH'},  # TAG#<tag_id>
        {'AttributeName': 'SK', 'KeyType': 'RANGE'}  # TAG#<category>
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'PK', 'AttributeType': 'S'},
        {'AttributeName': 'SK', 'AttributeType': 'S'},
        {'AttributeName': 'GSI1PK', 'AttributeType': 'S'},
        {'AttributeName': 'GSI1SK', 'AttributeType': 'S'}
    ],
    'GlobalSecondaryIndexes': [
        {
            'IndexName': IndexNames.DynamoDB.TAG_GSI,
            'KeySchema': [
                {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'},  # TAG#ALL -> TAG#<category>
                {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'}  # <count>#<tag_id>
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
            'IndexName': IndexNames.DynamoDB.TAG_GSI,  # 태그별 공고 조회를 위한 인덱스
            'KeySchema': [
                {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'},
                {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'}
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