from typing import Dict, Type
from .base import BaseRepository
from .services.mongodb.repository import MongoDBRepository
from .services.dynamodb.repository import DynamoDBRepository
from .exceptions import StorageException

REPOSITORIES: Dict[str, Type[BaseRepository]] = {
    'mongodb': MongoDBRepository,
    'dynamodb': DynamoDBRepository
}

def create_repository(repo_type: str, collection_name: str) -> BaseRepository:
    """저장소 인스턴스 생성"""
    repo_class = REPOSITORIES.get(repo_type)
    if not repo_class:
        raise StorageException(f"지원하지 않는 저장소 타입: {repo_type}")
    return repo_class(collection_name)