import jwt
import datetime
from fastapi import HTTPException

def test_token_validation_success(mock_token_validator):
    # JWT 헤더에 kid를 포함시킨 토큰 생성
    token_headers = {
        "kid": "test_key_id",
        "alg": "HS256",
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
        headers=token_headers  # 헤더 정보 추가
    )
    
    result = mock_token_validator.verify_id_token(test_token)
    
    assert result["cognito:username"] == "test_user"
    assert result["email"] == "test@example.com"