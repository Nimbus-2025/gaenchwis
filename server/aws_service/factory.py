from typing import Dict, Type
from .base import BaseRepository
from .exceptions import StorageException
from .services.mongodb.repository import MongoDBRepository
from .services.dynamodb.repository import DynamoDBRepository
from .services.common.constants import STORAGE_TYPES
from .services.common.enums import StorageType
from .services.mongodb.repository import MongoDBRepository
from .services.dynamodb.repository import DynamoDBRepository

REPOSITORIES: Dict[str, Type[BaseRepository]] = {
    StorageType.MONGODB.value: MongoDBRepository,
    StorageType.DYNAMODB.value: DynamoDBRepository
}

def create_repository(repo_type: str, collection_name: str, **kwargs) -> BaseRepository:
    if repo_type not in STORAGE_TYPES:
        raise StorageException(f"지원하지 않는 저장소 타입: {repo_type}")    
    repo_class = REPOSITORIES[repo_type]
    return repo_class(collection_name, **kwargs)