# 웹 드라이버 설정
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from .constants import USER_AGENTS
import random

# 웹 드라이버 설정
def setup_driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    
    # User-Agent 설정
    options.add_argument(f'user-agent={random.choice(USER_AGENTS)}')
    
    # 기본 옵션 설정
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-extensions')
    options.add_argument('--lang=ko_KR')
    options.add_argument('--start-maximized')
    
    # 추가 옵션 설정 
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("detach", True)
    
    # 페이지 로드 전략 설정
    options.page_load_strategy = 'normal'
    
    driver = webdriver.Chrome(service=service, options=options)
    
    # WebDriver 감지 우회
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })
    
    # 암시적 대기 설정 
    driver.implicitly_wait(10)
    
    return driver