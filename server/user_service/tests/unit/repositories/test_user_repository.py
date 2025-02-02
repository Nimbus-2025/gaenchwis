import boto3
from app.repositories.user_repository import UserRepository
from app.schemas.user_schemas import ApplyCreate

def test_create_apply(mock_dynamodb):
    repository = UserRepository()
    apply_data = ApplyCreate(
        post_id="test_post",
        post_name="Test Position"
    )
    
    result = repository.create_apply("test_user", apply_data)
    
    assert result["user_id"] == "test_user"
    assert result["post_id"] == "test_post"
    assert result["post_name"] == "Test Position"