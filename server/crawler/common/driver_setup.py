# Python 내장 라이브러리 
import os
import random
# 외부 HTTP 요청 라이브러리 
import requests
# Selenium 관련 라이브러리 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# WebDriver 매니저 
from webdriver_manager.chrome import ChromeDriverManager
# 로컬 상수
from .constants import CrawlerConfig

def get_chrome_version():
    try:
        # Chrome 버전 확인 (Docker 환경에서만 동작)
        if os.environ.get('DOCKER_CONTAINER'):
            version = os.popen('google-chrome --version').read()
            version = version.strip('Google Chrome ').strip().split('.')[0]
            return version
        return None
    except Exception as e:
        print(f"Chrome 버전 확인 실패: {str(e)}")
        return None
    
def get_chromedriver_url(version):
    try: 
        # 특정 버전의 ChromeDriver URL 가져오기
        response = requests.get(f'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{version}')
        if response.status_code == 200:
            driver_version = response.text.strip()
            # ChromeDriver 다운로드 URL 반환 
            return f"https://chromedriver.storage.googleapis.com/{driver_version}/chromedriver_linux64.zip"
    except Exception as e:
        print(f"ChromeDriver URL 가져오기 실패: {str(e)}")
    return None

# 웹 드라이버 설정
def setup_driver():
    # Chrome 옵션 객체 생성 
    options = webdriver.ChromeOptions()
    
    # Docker 환경 감지
    in_docker = os.environ.get('DOCKER_CONTAINER', False)
        
    # [봇 감지 방지를 위한 핵심 설정]
    
    # 0. 기본 옵션  
    options.add_argument('--disable-infobars')  # 자동화된 테스트 소프트웨어에 의해 제어되고 있다는 알림 배너 비활성화
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-features=NetworkService')
    
    # 1. 랜덤 User-Agent 설정
    options.add_argument(f'user-agent={random.choice(CrawlerConfig.USER_AGENTS)}')    # 랜덤 User-Agent로 봇 감지 방지 
    
    # 2. 자동화 흔적 제거 
    options.add_argument('--disable-blink-features=AutomationControlled')   # 자동화 감지 플래그 제거
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 자동화 관련 로그 숨김
    options.add_experimental_option('useAutomationExtension', False)
    
    # 3. 웹 드라이버 관련 플래그 제거 
    options.add_argument('--disable-web-security')  # 웹 보안 정책 우회ㅑ 
    options.add_argument('--ignore-certificate-errors') # 인증서 오류 무시
    options.add_argument('--ignore-ssl-errors') # SSL 오류 무시 
    
    # 4. 실제 브라우저처럼 보이게 하는 설정
    options.add_argument('--start-maximized')   # 실제 사용자처럼 전체 화면으로 사용
    options.add_argument('--lang=ko_KR')    # 한국어 설정으로 현지화 
    
    # 5. 필수 성능 옵션
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Docker 환경 전용 설정 
    if in_docker:
        options.add_argument('--headless')
        options.binary_location = '/usr/bin/google-chrome'
    
    # 6. 추가 봇 감지 방지 설정 
    prefs = {
        'profile.default_content_setting_values.notifications': 2,
        'credentials_enable_service': False,
        'profile.password_manager_enabled': False
    }
    options.add_experimental_option('prefs', prefs)
    
    # 페이지 로드 전략 변경 (normal: 모든 리소스 로드 대기)
    options.page_load_strategy = 'normal'
    
    try: 
        if in_docker:
            # Docker 환경에서는 설치된 Chrome 버전 확인 
            chrome_version = get_chrome_version()
            print(f"Detected Chrome vserion: {chrome_version}")
        
            if not chrome_version:
                raise Exception("Chrome 버전을 확인할 수 없습니다.")
            
            service = Service()
        else: 
            # 로컬 환경에서는 자동으로 ChromeDriverManager 설치 및 관리
            service = Service(ChromeDriverManager().install())
        
        # WebDriver 인스턴스 생성 
        driver = webdriver.Chrome(
                service=service,
                options=options
        )
        
        # 7. WebDriver 속성 숨기기
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        driver.implicitly_wait(30) # 요소 대기 시간 설정 
        return driver
    
    except Exception as e:
        print(f"ChromeDriver 초기화 실패: {str(e)}")
        raise