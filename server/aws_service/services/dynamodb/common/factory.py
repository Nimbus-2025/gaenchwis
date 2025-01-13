from typing import Dict, Type
from aws_service.services.dynamodb.common.base_repository import BaseRepository
from aws_service.services.dynamodb.common.exceptions import DynamoDBException
from aws_service.services.dynamodb.common.constants import TableNames
from aws_service.services.dynamodb.common.enums import RepositoryType
from aws_service.services.dynamodb.crawling.repository import CrawlingRepository
from aws_service.services.dynamodb.user.repository import UserRepository
from aws_service.services.dynamodb.essay.repository import EssayRepository

REPOSITORIES: Dict[str, Type[BaseRepository]] = {
    RepositoryType.CRAWLING.value: CrawlingRepository,
    RepositoryType.USER.value: UserRepository,
    RepositoryType.ESSAY.value: EssayRepository
}

def create_repository(repo_type: str, table_name: str, **kwargs) -> BaseRepository:
    if repo_type not in REPOSITORIES:
        raise DynamoDBException(f"지원하지 않는 레포지토리 타입: {repo_type}")
    
    if table_name not in [table.value for table in TableNames]:
        raise DynamoDBException(f"정의되지 않은 테이블 이름: {table_name}")
    
    repo_class = REPOSITORIES[repo_type]
    return repo_class(table_name, **kwargs)