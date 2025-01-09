from pymongo import IndexModel, ASCENDING, DESCENDING
from ..common.constants import TableNames, IndexNames

# 컬렉션 이름 상수 정의
COMPANIES_COLLECTION = TableNames.COMPANIES
JOB_POSTINGS_COLLECTION = TableNames.JOB_POSTINGS
TAGS_COLLECTION = TableNames.TAGS
JOB_TAGS_COLLECTION = TableNames.JOB_TAGS

# 기업 컬렉션 인덱스
company_indexes = [
    IndexModel([('company_id', ASCENDING)], unique=True, name='company_id_unique'),
    IndexModel([('company_name', ASCENDING)], name='company_name_index'),
    IndexModel(
        [('created_at', DESCENDING)],
        name='company_created_index',
        partialFilterExpression={'status': 'active'}    # 활성 회사만 인덱싱
    )
]

# 채용공고 컬렉션 인덱스
job_posting_indexes = [
    IndexModel([('post_id', ASCENDING)], unique=True, name='post_id_unique'),
    IndexModel([('company_id', ASCENDING)], name='company_id_index'),
    IndexModel(
            [('status', ASCENDING), ('created_at', DESCENDING)],
            name=IndexNames.STATUS_DATE
    ),
    IndexModel(
        [('company_id', ASCENDING), ('created_at', DESCENDING)],
        name=IndexNames.COMPANY_DATE    
    ),
    IndexModel([('is_closed', ASCENDING), ('updated_at', DESCENDING)]),
    IndexModel([('tags', ASCENDING)], name='tags_index'),   # 태그 기반 검색용
    # 전문 검색을 위한 텍스트 인덱스
    IndexModel([
        ('post_name', 'text'), 
        ('company_name', 'text')
    ], name='text_search_index'),
]

# 태그 컬렉션 인덱스
tag_indexes = [
    IndexModel([('tag_id', ASCENDING)], unique=True, name='tag_id_unique'),
    IndexModel([('category', ASCENDING)], name='category_index'),
    IndexModel([('parent_id', ASCENDING)], name='parent_id_index'),
    IndexModel(
        [('category', ASCENDING), ('count', DESCENDING)],
        name=IndexNames.TAG_COUNT
    ),
    IndexModel([('level', ASCENDING), ('name', ASCENDING)])
]

# 채용공고-태그 매핑 컬렉션 인덱스
job_tag_indexes = [
    IndexModel([('job_tag_id', ASCENDING)], unique=True),
    IndexModel([('job_id', ASCENDING)], name='job_id_index'),
    IndexModel([('tag_id', ASCENDING)], name='tag_id_index'),
    IndexModel([('created_at', DESCENDING)])
]

# 컬렉션 스키마 정의
company_schema = {
    'bsonType': 'object',
    'required': ['company_id', 'company_name', 'created_at'],
    'properties': {
        'company_id': {'bsonType': 'string'},
        'company_name': {'bsonType': 'string'},        
        'created_at': {'bsonType': 'date'},
        'updated_at': {'bsonType': 'date'},
        'status': {
            'bsonType': 'string',
            'enum': ['active', 'inactive'],
            'default': 'active'
        }
    }
}

job_posting_schema = {
    'bsonType': 'object',
    'required': [
        'post_id', 'post_name', 'company_id', 'company_name',
        'is_closed', 'post_url', 'status', 'created_at', 'updated_at'
    ],
    'properties': {
        'post_id': {'bsonType': 'string'},
        'post_name': {'bsonType': 'string'},
        'company_id': {'bsonType': 'string'},
        'company_name': {'bsonType': 'string'},
        'is_closed': {'bsonType': 'date'},
        'post_url': {'bsonType': 'string'},
        'status': {
            'bsonType': 'string',
            'enum': ['active', 'inactive'],
            'default': 'active'
        },
        'created_at': {'bsonType': 'date'},
        'updated_at': {'bsonType': 'date'},
        'tags': {
            'bsonType': 'array',
            'items': {'bsonType': 'string'},
            'uniqueItems': True
        }
    }
}

tag_schema = {
    'bsonType': 'object',
    'required': [
        'tag_id', 'category', 'name', 'level',
        'count', 'created_at', 'updated_at'
    ],
    'properties': {
        'tag_id': {'bsonType': 'string'},
        'category': {
            'bsonType': 'string',
            'enum': ['location', 'skill', 'position']    
        },
        'name': {'bsonType': 'string'},
        'parent_id': {'bsonType': ['string', 'null']},
        'level': {'bsonType': 'int'},
        'count': {
            'bsonType': 'int',
            'minimum': 0,
            'default': 0
        },
        'created_at': {'bsonType': 'date'},
        'updated_at': {'bsonType': 'date'}
    }
}

job_tag_schema = {
    'bsonType': 'object',
    'required': ['job_tag_id', 'job_id', 'tag_id', 'created_at'],
    'properties': {
        'job_tag_id': {'bsonType': 'string'},
        'job_id': {'bsonType': 'string'},
        'tag_id': {'bsonType': 'string'},
        'created_at': {'bsonType': 'date'},
        # 선택적으로 추가할 수 있는 필드들
        'created_by': {'bsonType': 'string'},  # 태그를 추가한 주체
        'status': {  # 태그의 활성 상태
            'bsonType': 'string',
            'enum': ['active', 'removed'],
            'default': 'active'
        }
    }
}