import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    # API 설정
    API_KEY: str = os.getenv('API_KEY', 'default_api_key')
    
    # 서버 설정
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', '8000'))
    DEBUG: bool = os.getenv('FLASK_ENV') == 'development'
    
    # AWS 설정
    AWS_REGION: str = os.getenv('AWS_REGION', 'ap-northeast-2')

    # 크롤러 설정
    CHROME_DRIVER_PATH: str = os.getenv('CHROME_DRIVER_PATH', '/usr/local/bin/chromedriver')
    HEADLESS: bool = os.getenv('HEADLESS', 'true').lower() == 'true'
    
    # 로깅 설정
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = os.getenv('LOG_FILE', 'crawler_executor.log')
    
    def __post_init__(self):
        """설정 유효성 검증"""
        os.environ['AWS_REGION'] = self.AWS_REGION