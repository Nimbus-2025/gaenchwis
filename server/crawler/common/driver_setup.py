import random
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from .constants import USER_AGENTS

def get_chrome_version():
    try:
        # Chrome 버전 확인
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
            return f"https://chromedriver.storage.googleapis.com/{driver_version}/chromedriver_linux64.zip"
    except Exception as e:
        print(f"ChromeDriver URL 가져오기 실패: {str(e)}")
    return None

# 웹 드라이버 설정
def setup_driver():
    options = webdriver.ChromeOptions()
    
    # Docker 환경 감지
    in_docker = os.environ.get('DOCKER_CONTAINER', False)
        
    # User-Agent 설정
    options.add_argument(f'user-agent={random.choice(USER_AGENTS)}')
    
    # 기본 옵션 설정
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    
    # Docker 환경일 때만 적용되는 옵션 
    if in_docker:
        options.add_argument('--headless')
        options.binary_location = '/usr/bin/google-chrome'
        
    # 공통 옵션 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--lang=ko_KR')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-web-security')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--start-maximized')
    
    # 추가 옵션
    options.add_argument('--disable-features=IsolateOrigins,site-per-process')
    options.add_argument('--disable-site-isolation-trials')
    options.add_argument('--disable-features=NetworkService')
    options.add_argument('--disable-features=VizDisplayCompositor')
    options.add_experimental_option("detach", True)
    
    # 성능 관련 옵션 추가
    prefs = {
        'profile.default_content_setting_values.notifications': 2,
        'profile.managed_default_content_settings.images': 1,
        'disk-cache-size': 4096
    }
    options.add_experimental_option('prefs', prefs)
    
    # 페이지 로드 전략 변경
    options.page_load_strategy = 'normal'
    
    try: 
        if in_docker:
            # Docker 환경에서는 Chrome 버전 확인 
            chrome_version = get_chrome_version()
            print(f"Detected Chrome vserion: {chrome_version}")
        
            if not chrome_version:
                raise Exception("Chrome 버전을 확인할 수 없습니다.")
            
            service = Service()
        else: 
            # 로컬 환경에서는 ChromeDriverManager 사용 
            service = Service(ChromeDriverManager().install())
        
        driver = webdriver.Chrome(
                service=service,
                options=options
        )
        driver.implicitly_wait(30)
        return driver
    
    except Exception as e:
        print(f"ChromeDriver 초기화 실패: {str(e)}")
        raise