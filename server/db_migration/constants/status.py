from enum import Enum

class JobStatus(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    
    @classmethod
    def is_valid(cls, status: str) -> bool:
        return status in [item.value for item in cls]