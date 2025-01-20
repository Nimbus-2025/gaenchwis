from enum import Enum

class StorageType(str, Enum):
    DYNAMODB = 'dynamodb'
    
class RepositoryType(Enum):
    CRAWLING = 'CRAWLING'
    USER = 'USER'
    ESSAY = 'ESSAY'