from enum import Enum

class JobStatus(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    
    @classmethod
    def is_valid(cls, status: str) -> bool:
        return status in [item.value for item in cls]

class EssayStatus(str, Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    IN_REVIEW = "IN_REVIEW"
    COMPLETED = "COMPLETED"
    
    @classmethod
    def is_valid(cls, status: str) -> bool:
        return status in [item.value for item in cls]
    

class ScheduleType(str, Enum):
    INTERVIEW = "INTERVIEW"
    EXAM = "EXAM"
    DOCUMENT_DEADLINE = "DOCUMENT_DEADLINE"
    CODING_TEST = "CODING_TEST"
    OTHER = "OTHER"
    
    @classmethod
    def is_valid(cls, type: str) -> bool:
        return type in [item.value for item in cls]
    
    
class ApplyStatus(str, Enum):
    APPLIED = "APPLIED"
    DOCUMENT_PASS = "DOCUMENT_PASS"
    DOCUMENT_FAIL = "DOCUMENT_FAIL"
    INTERVIEW_SCHEDULED = "INTERVIEW_SCHEDULED"
    INTERVIEW_COMPLETE = "INTERVIEW_COMPLETE"
    OFFER_RECEIVED = "OFFER_RECEIVED"
    REJECTED = "REJECTED"
    ACCEPTED = "ACCEPTED"
    WITHDRAWN = "WITHDRAWN"
    
    @classmethod
    def is_valid(cls, status: str) -> bool:
        return status in [item.value for item in cls]