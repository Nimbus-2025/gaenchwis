from base.base_crawler import BaseCrawler
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)

import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from common.utils import save_to_csv
from common.constants import URLS
from aws_service.factory import create_repository
from aws_service.services.common.constants import TableNames

class JobKoreaCrawler(BaseCrawler):
    def __init__(self, output_dir):
        super().__init__(output_dir)
        self.url = URLS['jobkorea']
        self.company_repo = create_repository('mongodb', TableNames.COMPANIES)
        self.job_repo = create_repository('mongodb', TableNames.JOB_POSTINGS)
        self.tag_repo = create_repository('mongodb', TableNames.TAGS)
        self.job_tag_repo = create_repository('mongodb', TableNames.JOB_TAGS)
        
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
    
    def process_and_save_data(self, jobkorea_data):
        for job_data in jobkorea_data:
            try:
                # 1. 기업 정보 저장
                company_data = {
                    '_id': job_data['회사명'],  # 회사명을 기업 식별자로 사용
                    'name': job_data['회사명']
                    # 추가 회사 정보가 있다면 여기에 추가
                }
                self.company_repo.save(company_data)

                # 2. 태그 정보 추출 및 저장
                tags = []
                if job_data['직무분야']:
                    tags.extend(job_data['직무분야'].split(','))
                if job_data['고용형태']:
                    tags.append(job_data['고용형태'])
                if job_data['경력']:
                    tags.append(job_data['경력'])
                
                tag_ids = []
                for tag in set(tags):  # 중복 제거
                    tag_data = {
                        '_id': tag.strip(),
                        'name': tag.strip(),
                        'category': self._determine_tag_category(tag)  # 태그 카테고리 결정 함수 필요
                    }
                    self.tag_repo.save(tag_data)
                    tag_ids.append(tag.strip())

                # 3. 채용 공고 저장
                job_data_processed = {
                    '_id': job_data['공고URL'],
                    'company_id': job_data['회사명'],  # 회사명으로 참조
                    'title': job_data['공고제목'],
                    'location': job_data['근무지'],
                    'education': job_data['학력'],
                    'deadline': job_data['마감일'],
                    'modified_date': job_data['수정일'],
                    'url': job_data['공고URL']
                }
                self.job_repo.save(job_data_processed)

                # 4. 공고-태그 매핑 정보 저장
                for tag_id in tag_ids:
                    mapping_data = {
                        '_id': f"{job_data['공고URL']}_{tag_id}",  # 복합 키
                        'job_id': job_data['공고URL'],
                        'tag_id': tag_id
                    }
                    self.job_tag_repo.save(mapping_data)

            except Exception as e:
                print(f"데이터 처리 중 오류 발생 (회사: {job_data['회사명']}): {e}")
                continue

    def _determine_tag_category(self, tag: str) -> str:
        """태그 카테고리 결정"""
        # 태그의 성격에 따라 카테고리 반환
        if '신입' in tag or '경력' in tag:
            return 'experience'
        elif '정규직' in tag or '계약직' in tag:
            return 'employment_type'
        else:
            return 'job_field'
        
        
    def crawl(self):
        try: 
            print("URL 접속 시도:", self.url)
            self.driver.get(self.url)
            print("URL 접속 성공")
            self.wait_random(2, 3)
            
            print("페이지 로딩 대기 중...")
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div#dev-gi-list"))
            )
            print("페이지 로딩 완료")
            
            # Chrome 설정 확인
            print("Chrome 옵션:", self.driver.capabilities)
            
            # 현재 URL 출력
            print("현재 페이지 URL:", self.driver.current_url)
            
            if (self.apply_job_filters() and 
                self.apply_location_filters() and
                self.apply_sort_settings()):
                
                jobkorea_data = self.crawl_jobs()
                
                if jobkorea_data:
                    # CSV 파일 저장 
                    output_file = os.path.join(self.output_dir, 'jobkorea_jobs.csv')
                    save_to_csv(jobkorea_data, output_file)
                    
                    # MongoDB에 저장
                    self.process_and_save_data(jobkorea_data)
                        
                    print(f"잡코리아 공고 크롤링이 완료되었습니다. 총 {len(jobkorea_data)}개의 공고가 수집되었습니다.")
                else:
                    print("크롤링된 데이터가 없습니다.")
            else:
                print("필터 또는 정렬 설정 적용에 실패했습니다.")
                
        except TimeoutException:
            print("페이지 로딩 시간이 초과되었습니다. 네트워크 상태를 확인해주세요.")
        except Exception as e:
            print(f"크롤링 중 오류 발생: {e}")
            print(f"현재 URL: {self.driver.current_url if self.driver else 'driver not initialized'}")
            print(f"Page source: {self.driver.page_source if self.driver else 'no page source'}")
            raise