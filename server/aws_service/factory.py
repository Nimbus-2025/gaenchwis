from typing import Literal
from .base import BaseRepository
from .services.mongodb.repository import MongoDBRepository
from .services.dynamodb.repository import DynamoDBRepository

class RepositoryFactory:
    @staticmethod
    def create(
        repo_type: Literal['mongodb', 'dynamodb'],
        collection_name: str
    ) -> BaseRepository:
        if repo_type == 'mongodb':
            return MongoDBRepository(collection_name)
        elif repo_type == 'dynamodb':
            return DynamoDBRepository(collection_name)
        raise ValueError(f"Unknown repository type: {repo_type}")