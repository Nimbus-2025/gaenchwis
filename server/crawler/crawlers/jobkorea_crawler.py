from base.base_crawler import BaseCrawler
import os
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from common.utils import save_to_csv
from common.constants import URLS

class JobKoreaCrawler(BaseCrawler):
    def __init__(self, output_dir):
        super().__init__(output_dir)
        self.url = URLS['jobkorea']
        
    def apply_job_filters(self):
        try:
            # 직무 선택 버튼 클릭
            duty_button = self.wait_for_element(By.CSS_SELECTOR, "dl.job.circleType")
            self.driver.execute_script("arguments[0].click();", duty_button)
            self.wait_random(1, 2)
            
            # 개발·데이터 직군 선택
            dev_data_element = self.wait_for_element(By.CSS_SELECTOR, "label[for='duty_10031']")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", dev_data_element)
            self.wait_random()
            self.driver.execute_script("arguments[0].click();", dev_data_element)
            self.wait_random(2, 3)
            
            # 개발·데이터 하위 직무 모두 선택
            sub_duties = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#duty_step2_10031_ly li.item input[type='checkbox']"))
            )
            
            print(f"발견된 하위 직무 개수: {len(sub_duties)}")
            
            for duty in sub_duties:
                try:
                    if not duty.is_selected():
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", duty)
                        time.sleep(0.5)
                        self.driver.execute_script("arguments[0].click();", duty)
                        print(f"선택된 직무: {duty.get_attribute('data-name')}")
                        time.sleep(0.5)
                except Exception as e:
                    print(f"하위 직무 선택 중 오류: {e}")
                    continue
                    
            return True
        
        except Exception as e:
            print(f"직무 필터 적용 중 오류 발생: {e}")
            print(f"현재 페이지 URL: {self.driver.current_url}")
            return False

    def apply_location_filters(self):
        try:
            # 근무지역 버튼 클릭 (수정된 선택자)
            location_button = self.wait_for_element(By.CSS_SELECTOR, "dl.loc.circleType")
            self.driver.execute_script("arguments[0].click();", location_button)
            self.wait_random(1, 2)
            
            # 서울 선택 (수정된 선택자)
            seoul_element = self.wait_for_element(By.CSS_SELECTOR, "input[type='checkbox'][id='local_I000']")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", seoul_element)
            self.wait_random()
            
            if not seoul_element.is_selected():
                self.driver.execute_script("arguments[0].click();", seoul_element)
                print("서울 지역이 선택되었습니다.")
            
            self.wait_random(1, 2)
            
            # 검색 버튼 클릭
            search_button = self.wait_for_element(By.ID, "dev-btn-search")
            self.driver.execute_script("arguments[0].click();", search_button)
            self.wait_random(2, 3)
            
            print("서울 지역 필터가 적용되었습니다.")
            return True
            
        except Exception as e:
            print(f"지역 필터 적용 중 오류 발생: {e}")
            print(f"현재 페이지 URL: {self.driver.current_url}")
            return False
        
    def apply_sort_settings(self): 
        try:
            # 최신업데이트순 설정
            order_select = self.wait_for_element(By.ID, "orderTab")
            Select(order_select).select_by_value("3")
            self.wait_random()
            
            # 50개씩 보기 설정
            count_select = self.wait_for_element(By.ID, "pstab")
            Select(count_select).select_by_value("50")
            self.wait_random(1, 2)
            
            return True
            
        except Exception as e:
            print(f"정렬 설정 중 오류 발생: {e}")
            return False
        
    def crawl_jobs(self):
        jobkorea_data = []
        page = 1
        max_pages = 2

        try:
            while page <= max_pages:
                print(f"현재 페이지: {page}")

                # 페이지 로딩 대기
                self.wait_for_element(By.CLASS_NAME, "tplList")
                
                self.natural_scroll()

                # 데이터 수집
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                jobs = soup.select('div.tplList table tbody tr.devloopArea')

                print(f"페이지 {page} - 발견된 채용공고 수: {len(jobs)}")

                for job in jobs:
                    try:
                        # 기존 파싱 로직 유지
                        company_element = job.select_one("td.tplCo a.link")
                        company = company_element.text.strip() if company_element else "회사명 없음"

                        title_element = job.select_one("td.tplTit a.link")
                        title = title_element.text.strip() if title_element else "제목 없음"
                        job_url = title_element.get("href") if title_element else ""
                        if job_url and not job_url.startswith('http'):
                            job_url = f"https://www.jobkorea.co.kr{job_url}"

                        job_fields_element = job.select_one("p.dsc")
                        job_fields = job_fields_element.text.strip() if job_fields_element else ""

                        etc_info = job.select("p.etc span.cell")
                        experience = etc_info[0].text.strip() if len(etc_info) > 0 else ""
                        education = etc_info[1].text.strip() if len(etc_info) > 1 else ""
                        location = etc_info[2].text.strip() if len(etc_info) > 2 else ""
                        job_type = etc_info[3].text.strip() if len(etc_info) > 3 else ""

                        date_elements = job.select_one("td.odd span.date")
                        deadline = date_elements.text.strip().replace("~", "").strip() if date_elements else ""

                        time_elements = job.select_one("td.odd span.time")
                        modified = time_elements.text.strip() if time_elements else ""

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
                            print(f"수집된 공고: {company} - {title}")

                        self.wait_random(0.3, 0.7)

                    except Exception as e:
                        print(f"항목 파싱 중 오류 발생: {e}")
                        continue

                # 다음 페이지로 이동
                if page < max_pages:
                    try:
                        next_page = self.wait_for_element(
                            By.CSS_SELECTOR, 
                            f".tplPagination.newVer a[data-page='{page + 1}']"
                        )
                        if next_page:
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", next_page)
                            self.wait_random(1, 2)
                            self.driver.execute_script("arguments[0].click();", next_page)
                            self.wait_random(2, 3)
                            page += 1
                        else:
                            print("더 이상 페이지를 찾을 수 없습니다.")
                            break
                    except Exception as e:
                        print(f"페이지 넘김 중 오류 발생: {e}")
                        break
                else:
                    break

        except Exception as e:
            print(f"크롤링 중 오류 발생: {e}")

        print(f"총 수집된 공고 수: {len(jobkorea_data)}")
        return jobkorea_data
    
    def crawl(self):
        try: 
            self.driver.get(self.url)
            self.wait_random(2, 3)
            
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div#dev-gi-list"))
            )
            
            if (self.apply_job_filters() and 
                self.apply_location_filters() and
                self.apply_sort_settings()):
                
                jobkorea_data = self.crawl_jobs()
                
                if jobkorea_data:
                    output_file = os.path.join(self.output_dir, 'jobkorea_jobs.csv')
                    save_to_csv(jobkorea_data, output_file)
                    print(f"잡코리아 공고 크롤링이 완료되었습니다. 총 {len(jobkorea_data)}개의 공고가 수집되었습니다.")
                else:
                    print("크롤링된 데이터가 없습니다.")
            else:
                print("필터 또는 정렬 설정 적용에 실패했습니다.")
                
        except TimeoutException:
            print("페이지 로딩 시간이 초과되었습니다. 네트워크 상태를 확인해주세요.")
        except Exception as e:
            print(f"크롤링 중 오류 발생: {e}")