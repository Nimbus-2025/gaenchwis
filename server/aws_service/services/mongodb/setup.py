# mongodb/setup.py
from pymongo import MongoClient
from .table_schemas import (
    # 컬렉션명
    COMPANIES_COLLECTION,
    JOB_POSTINGS_COLLECTION,
    TAGS_COLLECTION,
    JOB_TAGS_COLLECTION,
    # 인덱스
    company_indexes,
    job_posting_indexes,
    tag_indexes,
    job_tag_indexes,
    # 스키마
    company_schema,
    job_posting_schema,
    tag_schema,
    job_tag_schema
)

def setup_mongodb(connection_string: str, database_name: str):
    """MongoDB 초기 설정을 수행합니다."""
    client = MongoClient(connection_string)
    db = client[database_name]
    
    try:
        # 1. 스키마 검증 설정 - 데이터 무결성을 위해 필수
        db.command({
            'collMod': COMPANIES_COLLECTION,
            'validator': {'$jsonSchema': company_schema},
            'validationLevel': 'strict'
        })
        db.command({
            'collMod': JOB_POSTINGS_COLLECTION,
            'validator': {'$jsonSchema': job_posting_schema},
            'validationLevel': 'strict'
        })
        db.command({
            'collMod': TAGS_COLLECTION,
            'validator': {'$jsonSchema': tag_schema},
            'validationLevel': 'strict'
        })
        db.command({
            'collMod': JOB_TAGS_COLLECTION,
            'validator': {'$jsonSchema': job_tag_schema},
            'validationLevel': 'strict'
        })
        print("스키마 검증 설정 완료")

        # 2. 인덱스 생성 - 쿼리 성능을 위해 필수
        db[COMPANIES_COLLECTION].create_indexes(company_indexes)
        db[JOB_POSTINGS_COLLECTION].create_indexes(job_posting_indexes)
        db[TAGS_COLLECTION].create_indexes(tag_indexes)
        db[JOB_TAGS_COLLECTION].create_indexes(job_tag_indexes)
        print("인덱스 생성 완료")
        
        print("MongoDB 설정 완료")
    except Exception as e:
        print(f"인덱스 생성 중 오류 발생: {str(e)}")