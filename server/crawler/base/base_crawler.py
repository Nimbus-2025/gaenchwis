# Python 내장 라이브러리
import os
import random
import time
import logging
from abc import ABC, abstractmethod
from typing import Tuple, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

from common.driver_setup import setup_driver

class BaseCrawler(ABC):
    # BaseCrawler 초기화 
    def __init__(self, output_dir: str) -> None: 
        # 결과물 저장 디렉토리 경로
        self.output_dir = output_dir
        self.driver: Optional[WebDriver] = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.chrome_driver_path = os.getenv('CHROME_DRIVER_PATH', '/usr/local/bin/chromedriver')
        self.headless = os.getenv('HEADLESS', 'true').lower() == 'true'
        
    # 크롤러 초기화: 웹드라이버 설정 
    def initialize(self):
        try:
            self.driver = setup_driver()
        except Exception as e:
            raise RuntimeError(f"크롤러 초기화 실패: {e}")
        
    @abstractmethod
    def crawl(self) -> None:
        # 크롤링 로직을 구현해야 하는 추상 메서드
        pass
    
    def cleanup(self) -> None:
        # 웹 드라이버 및 리소스 정리
        if self.driver:
            try: 
                self.driver.quit()
            except WebDriverException as e:
                print("드라이버 종료 중 오류가 발생했습니다.")
            finally:
                self.driver = None
                
    def natural_scroll(self, scroll_pause: Tuple[float, float] = (0.3, 0.7)) -> None:
        # 자연스러운 스크롤 동작 수행
        try:
            total_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            current_position = 0
            
            while current_position < total_height:
                # 랜덤한 거리만큼 스크롤
                scroll_distance = random.randint(100, 300)
                current_position = min(current_position + scroll_distance, total_height)
                
                self.driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
                self.wait_random(*scroll_pause)
                # time.sleep(random.uniform(0.3, 0.7))
                
        except Exception as e:
            print(f"스크롤 중 오류 발생: {e}")
            
    def wait_random(self, min_time: float = 0.5, max_time: float = 1.5) -> None:
        # 랜덤한 시간만큼 대기
        # time.sleep(random.uniform(min_time, max_time))
        time.sleep(random.uniform(min_time, max_time))

    def wait_for_element(self, by: By, selector: str, timeout: int = 10) -> Optional[WebElement]:
        # 요소가 나타날 때까지 대기        
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, selector))
            )
        except TimeoutException:
            print(f"요소를 찾을 수 없음: {selector}")
            return None
        except WebDriverException as e:
            print(f"요소 대기 중 오류 발생: {e}")
            return None
            
    def safe_page_navigation(self, url: str, wait_time_range: Tuple[float, float] = (5, 10)) -> bool:
        # 안전한 페이지 이동
        try:
            self.driver.get(url)
            self.natural_scroll()
            self.wait_random(*wait_time_range)
            return True
        except WebDriverException as e:
            print(f"페이지 이동 중 오류 발생: {e}")
            return False