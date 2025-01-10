from typing import Dict, Type
from ..common.base_repository import BaseRepository
from ..common.exceptions import DynamoDBException
from ..common.constants import TableNames
from ..common.enums import RepositoryType
from ..crawling.repository import CrawlingRepository
from ..user.repository import UserRepository
from ..essay.repository import EssayRepository

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