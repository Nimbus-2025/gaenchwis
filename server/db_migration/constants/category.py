from enum import Enum

class TagCategory(str, Enum):
    LOCATION = "location"   # 지역 
    SKILL = "skill"         # 직무 분야 
    POSITION = "position"   # 경력/고용형태
    EDUCATION = "education" # 학력
    
    @classmethod
    def is_valid(cls, category: str) -> bool:
        return category in [item.value for item in cls]

class UserTagCategory(str, Enum):
    INTEREST = "interest"
    CAREER = "career"
    EDUCATION = "education"
    CERTIFICATE = "certificate"
    
    @classmethod
    def is_valid(cls, category: str) -> bool:
        return category in [item.value for item in cls]