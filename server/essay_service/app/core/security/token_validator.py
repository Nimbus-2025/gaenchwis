from fastapi import HTTPException
from typing import Dict
import jwt
import jwt.algorithms
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import requests
import json
import os
from dotenv import load_dotenv
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# .env 파일에서 환경변수 로드
load_dotenv()

# Cognito 설정
REGION = os.getenv('AWS_REGION')
USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')
APP_CLIENT_ID = os.getenv('COGNITO_APP_CLIENT_ID')

class TokenValidator:
    _instance = None
    jwks = None  # 클래스 레벨에서 속성 정의
    jwks_url = None  # 클래스 레벨에서 속성 정의
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TokenValidator, cls).__new__(cls)
            cls._instance.__init__()  # 초기화를 __init__에서 처리
        return cls._instance

    def __init__(self):
        if self.jwks_url is None:  # 한 번만 초기화되도록
            self.jwks_url = f"https://cognito-idp.{REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json"
            self._load_jwks()

    def _load_jwks(self):
        try:
            if not self.jwks:  # JWKS가 없을 때만 로드
                logger.info("Loading JWKS from Cognito...")
                response = requests.get(self.jwks_url)
                self.jwks = response.json()
                logger.info("JWKS loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load JWKS: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to load JWKS: {str(e)}"
            )
    
    def get_public_key(self, kid):
        try:
            if not self.jwks:
                self._load_jwks()
                
            key = next((k for k in self.jwks['keys'] if k['kid'] == kid), None)
            if not key:
                logger.error(f"Key ID not found: {kid}")
                raise HTTPException(
                    status_code=401, 
                    detail="Invalid token: Key ID not found"
                )
            return key
        except Exception as e:
            logger.error(f"Error getting public key: {str(e)}")
            raise HTTPException(
                status_code=401,
                detail=f"Error getting public key: {str(e)}"
            )
    
    def decode_and_validate_token(self, token: str) -> Dict:
        try:
            logger.info("Starting token validation...")
            
            # 토큰 헤더 디코딩 시도
            logger.info("Attempting to decode token header...")
            headers = jwt.get_unverified_header(token)
            kid = headers.get('kid')
            logger.info(f"Extracted kid from token: {kid}")
            
            if not kid:
                logger.error("No kid found in token header")
                raise HTTPException(status_code=401, detail="No kid found in token")
                
            # public key 가져오기
            logger.info("Fetching public key...")
            public_key = self.get_public_key(kid)
            logger.info("Successfully retrieved public key")
            
            # 토큰 검증 시도
            logger.info("Attempting to decode and validate token...")
            decoded_token = jwt.decode(
                token,
                key=jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(public_key)),
                algorithms=['RS256'],
                audience=APP_CLIENT_ID
            )
            
            logger.info("Token successfully validated")
            return decoded_token
                
        except jwt.exceptions.InvalidTokenError as e:
            logger.error(f"Invalid token error: {str(e)}")
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise HTTPException(status_code=401, detail=str(e))

    def verify_access_token(self, access_token: str) -> bool:
        """Access 토큰 검증 메서드"""
        try:
            self.decode_and_validate_token(access_token)
            return True
        except Exception:
            return False
            
    def verify_id_token(self, id_token: str) -> Dict:
        """ID 토큰 검증 및 사용자 정보 반환 메서드"""
        return self.decode_and_validate_token(id_token)

# 글로벌 인스턴스 생성
token_validator = TokenValidator()