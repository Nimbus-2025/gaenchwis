from enum import Enum

class StorageType(str, Enum):
    DYNAMODB = 'dynamodb'
    
class RepositoryType(Enum):
    CRAWLING = 'CRAWLING'
    USER = 'USER'
    ESSAY = 'ESSAY'

class JobStatus(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    
    @classmethod
    def is_valid(cls, status: str) -> bool:
        return status in [item.value for item in cls]

class TagCategory(str, Enum):
    LOCATION = "location"   # 지역 
    SKILL = "skill"         # 직무 분야 
    POSITION = "position"   # 경력/고용형태
    EDUCATION = "education" # 학력
    
    @classmethod
    def is_valid(cls, category: str) -> bool:
        return category in [item.value for item in cls]