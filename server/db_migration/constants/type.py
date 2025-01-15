from enum import Enum

class StorageType(str, Enum):
    DYNAMODB = 'dynamodb'
    
class RepositoryType(Enum):
    CRAWLING = 'CRAWLING'
    USER = 'USER'
    ESSAY = 'ESSAY'

class ScheduleType(str, Enum):
    INTERVIEW = "INTERVIEW"
    EXAM = "EXAM"
    DOCUMENT_DEADLINE = "DOCUMENT_DEADLINE"
    CODING_TEST = "CODING_TEST"
    OTHER = "OTHER"
    
    @classmethod
    def is_valid(cls, type: str) -> bool:
        return type in [item.value for item in cls]