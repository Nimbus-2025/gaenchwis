# Standard library imports 
import os
import time
import random

# Third-party imports
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
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
    """결과를 저장할 디렉토리 생성"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"'{directory}' 디렉토리가 생성되었습니다.")

def setup_driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    
    # User-Agent 설정
    options.add_argument(f'user-agent={random.choice(USER_AGENTS)}')
    
    # 기본 옵션 설정
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # 안정성 향상을 위한 추가 옵션
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
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(30)
    
    return driver

def wait_for_page_load(driver, timeout=30):
    """페이지가 완전히 로드될 때까지 대기"""
    try:
        # DOM 준비 대기
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        
        # 주요 요소 존재 확인
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        time.sleep(2)  # 추가 안정화 대기
        return True
        
    except TimeoutException:
        print("페이지 로딩 타임아웃. 계속 진행합니다...")
        return False

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

def apply_job_filters(driver):
    """개발·데이터 직군 필터링 및 정렬 설정"""
    try:
        # 직무 선택 버튼 클릭
        duty_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "dl.job.circleType"))
        )
        driver.execute_script("arguments[0].click();", duty_button)
        time.sleep(2)
        
        # 개발·데이터 직군 선택
        dev_data_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='duty_10031']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", dev_data_element)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", dev_data_element)
        time.sleep(3)
        
        # 개발·데이터 하위 직무 모두 선택
        sub_duties = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#duty_step2_10031_ly li.item input[type='checkbox']"))
        )
        
        print(f"발견된 하위 직무 개수: {len(sub_duties)}")
        
        for duty in sub_duties:
            try:
                if not duty.is_selected():
                    driver.execute_script("arguments[0].scrollIntoView(true);", duty)
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", duty)
                    print(f"선택된 직무: {duty.get_attribute('data-name')}")
                    time.sleep(0.5)
            except Exception as e:
                print(f"하위 직무 선택 중 오류: {e}")
                continue
        
        # 검색 버튼 클릭
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "dev-btn-search"))
        )
        driver.execute_script("arguments[0].click();", search_button)
        time.sleep(2)
        
        return True
        
    except Exception as e:
        print(f"필터 적용 중 오류 발생: {e}")
        print(f"현재 페이지 URL: {driver.current_url}")
        return False

def apply_sort_settings(driver):
    """정렬 옵션 설정"""
    try:
        # 최신업데이트순 설정
        order_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "orderTab"))
        )
        Select(order_select).select_by_value("3")
        time.sleep(1)
        
        # 50개씩 보기 설정
        count_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "pstab"))
        )
        Select(count_select).select_by_value("50")
        time.sleep(2)
        
        return True
        
    except Exception as e:
        print(f"정렬 설정 중 오류 발생: {e}")
        return False

def crawl_jobkorea(driver):
    """잡코리아 채용공고 크롤링"""
    jobkorea_data = []
    
    while True:
        # 페이지 로딩 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.tplList"))
        )
        time.sleep(2)
        
        # 현재 페이지의 HTML 가져오기
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        jobs = soup.select('tr.devloopArea')
        
        print(f"발견된 채용공고 수: {len(jobs)}")
        
        for job in jobs:
            try:
                # 회사명
                company_element = job.find_elements(By.CSS_SELECTOR, "td.tplCo span.compName, td.tplCo a.link")
                company = company_element[0].text.strip() if company_element else "회사명 없음"
                
                # 공고 제목
                title_element = job.find_elements(By.CSS_SELECTOR, "td.tplTit a.link")
                title = title_element[0].text.strip() if title_element else "제목 없음"
                job_url = title_element[0].get_attribute("href") if title_element else ""
                
                # 직무분야 정보
                job_fields_element = job.find_elements(By.CSS_SELECTOR, "p.dsc")
                job_fields = job_fields_element[0].text.strip() if job_fields_element else ""
                
                # 경력, 학력, 근무지 정보
                etc_info = job.find_elements(By.CSS_SELECTOR, "p.etc span.cell")
                experience = etc_info[0].text.strip() if len(etc_info) > 0 else ""
                education = etc_info[1].text.strip() if len(etc_info) > 1 else ""
                location = etc_info[2].text.strip() if len(etc_info) > 2 else ""
                job_type = etc_info[3].text.strip() if len(etc_info) > 3 else ""
                
                # 마감일 정보
                date_elements = job.find_elements(By.CSS_SELECTOR, "td.odd span.date")
                deadline = date_elements[0].text.strip().replace("~", "").strip() if date_elements else ""
                
                # 수정일 정보
                time_elements = job.find_elements(By.CSS_SELECTOR, "td.odd span.time")
                modified = time_elements[0].text.strip() if time_elements else ""
                
                # 유효한 데이터만 추가
                if company != "회사명 없음" and title != "제목 없음":
                    job_dict = {
                        '회사명': company,
                        '공고제목': title,
                        '직무분야': job_fields,
                        '경력': experience,
                        '학력': education,
                        '근무지': location,
                        '고용형태': job_type,
                        '마감일': deadline,
                        '수정일': modified,
                        '공고URL': job_url
                    }
                    jobkorea_data.append(job_dict)
                
                time.sleep(random.uniform(0.3, 0.7))
                
            except Exception as e:
                print(f"항목 파싱 중 오류 발생: {e}")
                continue
            
        return jobkorea_data

def main():
    output_dir = 'jobkorea_crawling_results'
    create_directory(output_dir)
    
    url = "https://www.jobkorea.co.kr/recruit/joblist?menucode=duty"
    driver = None
    
    try:
        driver = setup_driver()
        
        # 잡코리아 채용정보 페이지 접속
        driver.get(url)
        time.sleep(3)
        
        # 페이지 로딩 대기
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div#dev-gi-list"))
        )
        
        # 필터 및 정렬 설정 적용
        if apply_job_filters(driver) and apply_sort_settings(driver):
            # 크롤링 실행
            jobkorea_data = crawl_jobkorea(driver)
            
            # 결과 저장
            if jobkorea_data:
                output_file = os.path.join(output_dir, 'jobkorea_jobs.csv')
                save_to_csv(jobkorea_data, output_file)
                print(f"잡코리아 공고 크롤링이 완료되었습니다. 총 {len(jobkorea_data)}개의 공고가 수집되었습니다.")
            else:
                print("크롤링된 데이터가 없습니다.")
        else:
            print("필터 또는 정렬 설정 적용에 실패했습니다.")
            
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