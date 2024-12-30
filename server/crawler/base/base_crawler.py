from abc import ABC, abstractmethod
from common.utils import create_directory
from common.driver_setup import setup_driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

class BaseCrawler(ABC):
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.driver = None
        
    def initialize(self):
        create_directory(self.output_dir)
        self.driver = setup_driver()
        
    @abstractmethod
    def crawl(self):
        pass
    
    def cleanup(self):
        if self.driver:
            try: 
                self.driver.quit()
            except:
                print("드라이버 종료 중 오류가 발생했습니다.")
                
    # 자연스러운 스크롤 동작 수행
    def natural_scroll(self):
        try:
            total_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            current_position = 0
            
            while current_position < total_height:
                scroll_distance = random.randint(100, 300)
                current_position += scroll_distance
                
                self.driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
                time.sleep(random.uniform(0.3, 0.7))
                
        except Exception as e:
            print(f"스크롤 중 오류 발생: {e}")
            
    # 랜덤한 시간만큼 대기
    def wait_random(self, min_time=0.5, max_time=1.5):
        time.sleep(random.uniform(min_time, max_time))

    # 요소가 나타날 때까지 대기        
    def wait_for_element(self, by, selector, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, selector))
            )
            return element
        except Exception as e:
            print(f"요소 대기 중 오류 발생: {e}")
            return None
            
    # 안전한 페이지 이동
    def safe_page_navigation(self, url, wait_time_range=(5, 10)):
        try:
            self.driver.get(url)
            self.natural_scroll()
            self.wait_random(*wait_time_range)
            return True
        except Exception as e:
            print(f"페이지 이동 중 오류 발생: {e}")
            return False