from aws_service.services.dynamodb.common.constants import TableNames, IndexNames

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
            'IndexName': IndexNames.DynamoDB.ESSAY_GSI,
            'KeySchema': [
                {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'},
                {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'}
            ],
            **COMMON_GSI_SETTINGS
        }
    ],
    'BillingMode': 'PAY_PER_REQUEST'
}

ESSAY_CONTENTS_TABLE = {
    'TableName': TableNames.ESSAY_CONTENTS,
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
            'IndexName': IndexNames.DynamoDB.ESSAY_CONTENT_GSI,
            'KeySchema': [
                {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'},
                {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'}
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
            'IndexName': IndexNames.DynamoDB.ESSAY_JOB_POSTING_GSI,
            'KeySchema': [
                {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'},
                {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'}
            ],
            **COMMON_GSI_SETTINGS
        }
    ],
    'BillingMode': 'PAY_PER_REQUEST'
}

# 전체 테이블 리스트
TABLES = [
    ESSAYS_TABLE,
    ESSAY_CONTENTS_TABLE,
    ESSAY_JOB_POSTINGS_TABLE
]