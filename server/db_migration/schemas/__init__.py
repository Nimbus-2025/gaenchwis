from constants.table import TableNames
from constants.index import IndexNames

from .crawling import TABLES as CRAWLING_TABLES
from .user import TABLES as USER_TABLES
from .essay import TABLES as ESSAY_TABLES

# 모든 테이블 스키마를 하나의 리스트로 통합
ALL_TABLES = [
    *CRAWLING_TABLES,  # 크롤링 관련 테이블
    *USER_TABLES,      # 사용자 관련 테이블
    *ESSAY_TABLES      # 자소서 관련 테이블
]