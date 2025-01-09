from enum import Enum

class JobStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    # CLOSED = "closed"
    
class TagCategory(str, Enum):
    LOCATION = "location"
    SKILL = "skill" 
    POSITION = "position"