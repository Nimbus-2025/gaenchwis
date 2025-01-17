from enum import Enum

class EssayStatus(str, Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    IN_REVIEW = "IN_REVIEW"
    COMPLETED = "COMPLETED"
    
    @classmethod
    def is_valid(cls, status: str) -> bool:
        return status in [item.value for item in cls]