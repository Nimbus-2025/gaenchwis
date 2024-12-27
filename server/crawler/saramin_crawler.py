# Standard library imports 
import os
import time
import random

# Third-party imports
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


# User-Agent 리스트
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59'
]

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"'{directory}' 디렉토리가 생성되었습니다.")
        
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
    
def save_to_csv(data, filename):
    # 모든 필드의 따옴표 제거
    for item in data:
        for key in item:
            if isinstance(item[key], str):  # 문자열인 경우에만 처리
                item[key] = item[key].replace('"', '').replace("'", '')
    
    df = pd.DataFrame(data)
    
    # CSV 파일로 저장 (따옴표 없이)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"데이터가 {filename}에 저장되었습니다.")
    
def crawl_saramin(driver, url):
    saramin_list = []
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                driver.quit()
                driver = setup_driver()
            
            driver.get(url)
            time.sleep(random.uniform(5, 10))
            
            try:
                # 명시적 대기 조건 수정
                wait = WebDriverWait(driver, 30)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "box_item")))
                wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
                
                # 스크롤 동작
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(2)
                
                # HTML 파싱
                soup = BeautifulSoup(driver.page_source, 'html.parser')            
                job_items = soup.select('.box_item')  # 선택자 수정
                
                if not job_items:
                    print("공고 항목을 찾을 수 없습니다. 다시 시도합니다.")
                    continue
                
                for item in job_items:
                    try:
                        # 회사명
                        company_elem = item.select_one('.company_nm .str_tit')
                        company = company_elem.text.strip() if company_elem else ''
                        
                        # 공고 제목
                        title_elem = item.select_one('.job_tit .str_tit')
                        title = title_elem.text.strip() if title_elem else ''
                        
                        # 직무분야
                        sector_elem = item.select_one('.job_sector')
                        if sector_elem:
                            # 모든 span 태그 내의 텍스트를 리스트로 수집
                            sector_spans = sector_elem.select('span')
                            sector_texts = [span.text.strip() for span in sector_spans if span.text.strip()]
                            
                            # '외' 텍스트 제거
                            sector_texts = [text for text in sector_texts if text != '외']
                            
                            # 쉼표와 공백으로 연결
                            sector = ', '.join(sector_texts)
                        else:
                            sector = ''
                        
                        # 근무지
                        location_elem = item.select_one('.work_place')
                        location = location_elem.text.strip() if location_elem else ''
                        
                        # 경력/고용형태
                        career_elem = item.select_one('.career')
                        career = career_elem.text.strip() if career_elem else ''
                        
                        # 학력
                        education_elem = item.select_one('.education')
                        education = education_elem.text.strip() if education_elem else ''
                        
                        # 마감일 및 등록일
                        deadline_elem = item.select_one('.support_detail .date')
                        deadline = deadline_elem.text.strip() if deadline_elem else ''
                        
                        posted_elem = item.select_one('.support_detail .deadlines')
                        posted = posted_elem.text.strip() if posted_elem else ''
                        
                        # 공고 URL 추가
                        url_elem = item.select_one('.job_tit .str_tit')
                        job_url = ''
                        if url_elem and 'href' in url_elem.attrs:
                            job_url = 'https://www.saramin.co.kr' + url_elem['href']
                        
                        job_dict = {
                            '회사명': company,
                            '공고제목': title,
                            '직무분야': sector,
                            '근무지': location,
                            '경력/고용형태': career,
                            '학력': education,
                            '마감일': deadline,
                            '등록일': posted,
                            '공고URL': job_url  # URL 추가
                        }
                        
                        saramin_list.append(job_dict)
                        time.sleep(random.uniform(0.5, 1))
                        
                    except AttributeError as e:
                        print(f"항목 파싱 중 오류 발생: {e}")
                        continue
                
                if saramin_list:
                    return saramin_list
            
            except Exception as inner_e:
                print(f"페이지 처리 중 오류 발생: {inner_e}")
                continue
                
        except Exception as e:
            print(f"시도 {attempt + 1}/{max_retries} 실패: {e}")
            if attempt < max_retries - 1:
                print("잠시 후 재시도합니다...")
                time.sleep(random.uniform(10, 15))
            else:
                print("최대 재시도 횟수를 초과했습니다.")
    
    return []

def main():
    output_dir = 'saramin_crawling_results'
    create_directory(output_dir)
    
    url = "https://www.saramin.co.kr/zf_user/jobs/list/job-category?cat_mcls=2&panel_type=&search_optional_item=n&search_done=y&panel_count=y&preview=y&page=1&sort=RD"
    driver = None
    
    try:
        driver = setup_driver()
        
        # 사람인 채용정보 페이지 접속
        driver.get(url)
        
        # 페이지 로딩 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.box_item"))
        )
        
        # 크롤링 실행 
        saramin_data = crawl_saramin(driver, url)
        
        if saramin_data:
            output_file = os.path.join(output_dir, 'saramin_job.csv')
            save_to_csv(saramin_data, output_file)
            print(f"사람인 공고 크롤링이 완료되었습니다. 총 {len(saramin_data)}개의 공고가 수집되었습니다.")
        else:
            print("크롤링된 데이터가 없습니다.")
            
    except TimeoutException:
        print("페이지 로딩 시간이 초과되었습니다. 네트워크 상태를 확인해주세요.")
    except WebDriverException as e:
        print(f"WebDriver 오류 발생: {e}")
    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}")
        
    finally:
        if driver:
            try:
                driver.quit()
            except:
                print("드라이버 종료 중 오류가 발생했습니다.")

if __name__ == "__main__":
    main()