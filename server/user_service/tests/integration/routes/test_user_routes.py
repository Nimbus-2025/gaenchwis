from fastapi.testclient import TestClient
import jwt
import datetime
from app.core.security.token_validator import TokenValidator
from main import app

client = TestClient(app=app)

def test_create_apply_endpoint(mock_dynamodb, mock_token_validator):
    # 유효한 테스트 토큰 생성
    token_headers = {
        "kid": "test_key_id",
        "alg": "HS256",  # RS256에서 HS256으로 변경
        "typ": "JWT"
    }
    test_token = jwt.encode(
        {
            "cognito:username": "test_user",
            "email": "test@example.com",
            "exp": datetime.datetime.now() + datetime.timedelta(hours=1)
        },
        "test_secret",
        algorithm="HS256",
        headers=token_headers
    )

    response = client.post(
        "/api/v1/apply",
        json={
            "post_id": "test_post",
            "post_name": "Test Position"
        },
        headers={
            "access_token": test_token,
            "id_token": test_token,
            "user_id": "test_user"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "test_user"
    assert data["post_id"] == "test_post"