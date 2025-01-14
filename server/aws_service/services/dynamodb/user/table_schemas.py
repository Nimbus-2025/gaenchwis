from aws_service.services.dynamodb.common.constants import TableNames, IndexNames

# 공통 GSI 설정
COMMON_GSI_SETTINGS = {
    'Projection': {'ProjectionType': 'ALL'}
}

USERS_TABLE = {
    'TableName': TableNames.USERS,
    'KeySchema': [
        {'AttributeName': 'PK', 'KeyType': 'HASH'}
        # {'AttributeName': 'SK', 'KeyType': 'RANGE'}
    ],
    'AttributeDefinitions': [
        {'AttributeName': 'PK', 'AttributeType': 'S'},
        # {'AttributeName': 'SK', 'AttributeType': 'S'},
        {'AttributeName': 'GSI1PK', 'AttributeType': 'S'},
        {'AttributeName': 'GSI1SK', 'AttributeType': 'S'}
    ],
    'GlobalSecondaryIndexes': [
        {
            'IndexName': IndexNames.DynamoDB.USER_GSI,
            'KeySchema': [
                {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'},
                {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'}
            ],
            **COMMON_GSI_SETTINGS
        }
    ],
    'BillingMode': 'PAY_PER_REQUEST'
}

# USER_IMAGES_TABLE = {
#     'TableName': TableNames.USER_IMAGES,
#     'KeySchema': [
#         {'AttributeName': 'PK', 'KeyType': 'HASH'},
#         {'AttributeName': 'SK', 'KeyType': 'RANGE'}
#     ],
#     'AttributeDefinitions': [
#         {'AttributeName': 'PK', 'AttributeType': 'S'},
#         {'AttributeName': 'SK', 'AttributeType': 'S'},
#         {'AttributeName': 'GSI1PK', 'AttributeType': 'S'},
#         {'AttributeName': 'GSI1SK', 'AttributeType': 'S'}
#     ],
#     'GlobalSecondaryIndexes': [
#         {
#             'IndexName': IndexNames.DynamoDB.IMAGE_GSI,
#             'KeySchema': [
#                 {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'},
#                 {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'}
#             ],
#             **COMMON_GSI_SETTINGS
#         }
#     ],
#     'BillingMode': 'PAY_PER_REQUEST'
# }

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
            'IndexName': IndexNames.DynamoDB.TAG_GSI,
            'KeySchema': [
                {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'},
                {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'}
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
            'IndexName': IndexNames.DynamoDB.SCHEDULE_GSI,
            'KeySchema': [
                {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'},
                {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'}
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
            'IndexName': IndexNames.DynamoDB.BOOKMARK_GSI,
            'KeySchema': [
                {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'},
                {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'}
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
            'IndexName': IndexNames.DynamoDB.APPLY_GSI,
            'KeySchema': [
                {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'},
                {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'}
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
            'IndexName': IndexNames.DynamoDB.INTEREST_COMPANY_GSI,
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
    USERS_TABLE,
    # USER_IMAGES_TABLE,
    USER_TAGS_TABLE,
    SCHEDULES_TABLE,
    BOOKMARKS_TABLE,
    APPLIES_TABLE,
    INTEREST_COMPANIES_TABLE
]