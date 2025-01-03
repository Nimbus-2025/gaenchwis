from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict

class JobPosting:
    id: str
    title: str
    company: str
    location: str
    description: str
    url: str
    source: str
    status: str = 'active'
    created_at: str = None
    
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
            
    def to_dict(self) -> Dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'JobPosting':
        return cls(**data)