from enum import Enum

class StorageType(str, Enum):
    MONGODB = 'mongodb'
    DYNAMODB = 'dynamodb'

class JobStatus(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    
    @classmethod
    def is_valid(cls, status: str) -> bool:
        return status in [item.value for item in cls]

class TagCategory(str, Enum):
    LOCATION = "location"
    SKILL = "skill" 
    POSITION = "position"
    
    @classmethod
    def is_valid(cls, category: str) -> bool:
        return category in [item.value for item in cls]