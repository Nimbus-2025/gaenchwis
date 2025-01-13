from enum import Enum

class StorageType(str, Enum):
    MONGODB = 'mongodb'
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

# TODO 테이블 데이터에 맞게 수정 필요 
class TagCategory(str, Enum):
    LOCATION = "location"
    SKILL = "skill" 
    POSITION = "position"
    EDUCATION = "education"
    
    @classmethod
    def is_valid(cls, category: str) -> bool:
        return category in [item.value for item in cls]
    
class EssayStatus(str, Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    IN_REVIEW = "IN_REVIEW"
    COMPLETED = "COMPLETED"
    
    @classmethod
    def is_valid(cls, status: str) -> bool:
        return status in [item.value for item in cls]

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

class ScheduleType(str, Enum):
    INTERVIEW = "INTERVIEW"
    EXAM = "EXAM"
    DOCUMENT_DEADLINE = "DOCUMENT_DEADLINE"
    CODING_TEST = "CODING_TEST"
    OTHER = "OTHER"
    
    @classmethod
    def is_valid(cls, type: str) -> bool:
        return type in [item.value for item in cls]

class UserTagCategory(str, Enum):
    INTEREST = "interest"
    CAREER = "career"
    EDUCATION = "education"
    CERTIFICATE = "certificate"
    
    @classmethod
    def is_valid(cls, category: str) -> bool:
        return category in [item.value for item in cls]

class ImageType(str, Enum):
    PROFILE = "profile"
    PORTFOLIO = "portfolio"
    CERTIFICATE = "certificate"
    
    @classmethod
    def is_valid(cls, type: str) -> bool:
        return type in [item.value for item in cls]