# Python 내장 라이브러리 
import os
import sys
import logging
from datetime import datetime
from typing import Dict, List, Optional
# 외부 라이브러리
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
# 로컬 애플리케이션
from base.base_crawler import BaseCrawler
from common.utils import save_to_csv
from common.constants import URLS

# 프로젝트 루트 설정
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)

from aws_service.factory import create_repository
from aws_service.services.common.constants import TableNames

class JobKoreaCrawler(BaseCrawler):
    def __init__(self, output_dir: str) -> None:
        super().__init__(output_dir)
        self.url = URLS['jobkorea']
        self.logger = self._setup_logger() 
        
        self._initialize_repositories()
        
    def _setup_logger(self) -> logging.Logger:
        """로깅 설정"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        # 파일 핸들러 추가
        fh = logging.FileHandler(os.path.join(self.output_dir, 'jobkorea_crawler.log'))
        fh.setLevel(logging.INFO)
        
        # 포맷터 설정
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
        return logger
    
    def _initialize_repositories(self) -> None:
        """Repository 객체들 초기화"""
        try:
            self.company_repo = create_repository('mongodb', TableNames.COMPANIES)
            self.job_repo = create_repository('mongodb', TableNames.JOB_POSTINGS)
            self.tag_repo = create_repository('mongodb', TableNames.TAGS)
            self.job_tag_repo = create_repository('mongodb', TableNames.JOB_TAGS)
            
            self.logger.info("모든 Repository 초기화 완료")
        except Exception as e:
            self.logger.error(f"Repository 초기화 실패: {str(e)}")
            raise
        
    def apply_job_filters(self) -> bool:
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
                        self.wait_random(0.5, 1)
                        self.driver.execute_script("arguments[0].click();", duty)
                        duty_name = duty.get_attribute('data-name')
                        self.logger.info(f"선택된 직무: {duty_name}")
                        self.wait_random(0.5, 1)
                except Exception as e:
                    self.logger.error(f"하위 직무 선택 중 오류: {str(e)}")
                    continue
                    
            return True
        
        except Exception as e:
            print(f"직무 필터 적용 중 오류 발생: {e}")
            print(f"현재 페이지 URL: {self.driver.current_url}")
            return False

    def apply_location_filters(self):
        try:
            # 근무지역 버튼 클릭
            location_button = self.wait_for_element(By.CSS_SELECTOR, "dl.loc.circleType")
            self.driver.execute_script("arguments[0].click();", location_button)
            self.wait_random(2, 3)
            
            # 서울 선택
            seoul_element = self.wait_for_element(By.CSS_SELECTOR, "input[type='checkbox'][id='local_I000']")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", seoul_element)
            self.wait_random(1, 2)
            
            if not seoul_element.is_selected():
                self.driver.execute_script("arguments[0].click();", seoul_element)
                self.logger.info("서울 지역이 선택되었습니다.")
            
            self.wait_random(2, 3)
            
            # 검색 버튼 클릭
            search_button = self.wait_for_element(By.ID, "dev-btn-search")
            self.driver.execute_script("arguments[0].click();", search_button)
            self.wait_random(3, 4)
            
            self.logger.info("서울 지역 필터가 적용되었습니다.")
            return True
            
        except Exception as e:
            self.logger.error(f"지역 필터 적용 중 오류: {str(e)}")
            self.logger.error(f"현재 URL: {self.driver.current_url}")
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
        
    def _parse_job_item(self, job: BeautifulSoup) -> Optional[Dict]:
        """채용공고 항목 파싱"""
        try:
            company_element = job.select_one("td.tplCo a.link")
            company = company_element.text.strip() if company_element else None
            
            title_element = job.select_one("td.tplTit a.link")
            title = title_element.text.strip() if title_element else None
            
            if not (company and title):
                return None
                
            job_url = title_element.get("href", "")
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
            
            return {
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
            
        except Exception as e:
            self.logger.error(f"항목 파싱 중 오류: {str(e)}")
            return None
        
    def crawl_jobs(self) -> List[Dict]:
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
                    job_data = self._parse_job_item(job)
                    if job_data:
                        jobkorea_data.append(job_data)
                        self.logger.info(f"수집된 공고: {job_data['회사명']} - {job_data['공고제목']}")
                    
                    self.wait_random(2, 3)

                # 다음 페이지 이동
                if page < max_pages:
                    if not self._move_to_next_page(page):
                        break
                    page += 1
                    self.wait_random(3, 4)
                else:
                    break

        except Exception as e:
            print(f"크롤링 중 오류 발생: {e}")

        print(f"총 수집된 공고 수: {len(jobkorea_data)}")
        return jobkorea_data

    def _move_to_next_page(self, current_page: int) -> bool:
        """다음 페이지로 이동"""
        try:
            next_page = self.wait_for_element(
                By.CSS_SELECTOR,
                f".tplPagination.newVer a[data-page='{current_page + 1}']"
            )
            if next_page:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", next_page)
                self.wait_random(1, 2)
                self.driver.execute_script("arguments[0].click();", next_page)
                self.wait_random(2, 3)
                return True
            else:
                self.logger.warning("더 이상 페이지를 찾을 수 없습니다.")
                return False
        except Exception as e:
            self.logger.error(f"페이지 이동 중 오류 발생: {str(e)}")
            return False
    
    def process_and_save_data(self, jobkorea_data):
        for job_data in jobkorea_data:
            try:
                # 1. 기업 정보 저장
                company_data = {
                    '_id': job_data['회사명'],
                    'name': job_data['회사명'],
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                }
                self.company_repo.save(company_data)
                self.logger.info(f"기업 정보 저장: {job_data['회사명']}")

                # 2. 태그 처리 및 저장
                tag_ids = self._process_tags(job_data)

                # 3. 채용 공고 저장
                job_data_processed = {
                    '_id': job_data['공고URL'],
                    'company_id': job_data['회사명'],
                    'title': job_data['공고제목'],
                    'location': job_data['근무지'],
                    'education': job_data['학력'],
                    'deadline': job_data['마감일'],
                    'modified_date': job_data['수정일'],
                    'url': job_data['공고URL'],
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                }
                self.job_repo.save(job_data_processed)
                self.logger.info(f"채용공고 저장: {job_data['공고제목']}")

                # 4. 공고-태그 매핑 저장
                self._save_job_tags(job_data['공고URL'], tag_ids)

            except Exception as e:
                self.logger.error(f"데이터 처리 중 오류 ({job_data['회사명']}): {str(e)}")
                continue
            
    def _process_tags(self, job_data: Dict) -> List[str]:
        """태그 정보 추출 및 저장"""
        tags = []
        tag_ids = []

        # 직무분야 태그
        if job_data['직무분야']:
            tags.extend(job_data['직무분야'].split(','))
        
        # 고용형태 태그
        if job_data['고용형태']:
            tags.append(job_data['고용형태'])
        
        # 경력 태그
        if job_data['경력']:
            tags.append(job_data['경력'])
        
        # 중복 제거 및 태그 저장
        for tag in set(tags):
            tag = tag.strip()
            if not tag:
                continue
                
            tag_data = {
                '_id': tag,
                'name': tag,
                'category': self._determine_tag_category(tag),
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            try:
                self.tag_repo.save(tag_data)
                tag_ids.append(tag)
            except Exception as e:
                self.logger.error(f"태그 저장 중 오류 ({tag}): {str(e)}")
                
        return tag_ids

    def _determine_tag_category(self, tag: str) -> str:
        """태그 카테고리 결정"""
        tag = tag.lower()
        
        if any(keyword in tag for keyword in ['신입', '경력', '년차']):
            return 'experience'
        elif any(keyword in tag for keyword in ['정규직', '계약직', '인턴', '파견']):
            return 'employment_type'
        elif any(keyword in tag for keyword in ['학력', '대졸', '초대졸', '석사', '박사']):
            return 'education'
        else:
            return 'job_field'

    def _save_job_tags(self, job_id: str, tag_ids: List[str]) -> None:
        """공고-태그 매핑 정보 저장"""
        for tag_id in tag_ids:
            mapping_data = {
                '_id': f"{job_id}_{tag_id}",
                'job_id': job_id,
                'tag_id': tag_id,
                'created_at': datetime.now().isoformat()
            }
            
            try:
                self.job_tag_repo.save(mapping_data)
            except Exception as e:
                self.logger.error(f"공고-태그 매핑 저장 중 오류: {str(e)}")

    def crawl(self) -> None:
        """크롤링 메인 프로세스"""
        try:
            self.logger.info(f"URL 접속 시도: {self.url}")
            self.driver.get(self.url)
            self.logger.info("URL 접속 성공")
            self.wait_random(2, 3)

            self.logger.info("페이지 로딩 대기 중...")
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div#dev-gi-list"))
            )
            self.logger.info("페이지 로딩 완료")

            if (self.apply_job_filters() and 
                self.apply_location_filters() and
                self.apply_sort_settings()):

                jobkorea_data = self.crawl_jobs()

                if jobkorea_data:
                    # CSV 파일 저장
                    output_file = os.path.join(self.output_dir, 'jobkorea_jobs.csv')
                    save_to_csv(jobkorea_data, output_file)
                    self.logger.info(f"CSV 파일 저장 완료: {output_file}")

                    # MongoDB에 데이터 저장
                    self.process_and_save_data(jobkorea_data)
                    self.logger.info(f"크롤링 완료. 총 {len(jobkorea_data)}개의 공고가 수집되었습니다.")
                else:
                    self.logger.warning("크롤링된 데이터가 없습니다.")
            else:
                self.logger.error("필터 또는 정렬 설정 적용에 실패했습니다.")

        except TimeoutException:
            self.logger.error("페이지 로딩 시간 초과. 네트워크 상태를 확인하세요.")
        except Exception as e:
            self.logger.error(f"크롤링 중 오류 발생: {str(e)}")
            self.logger.error(f"현재 URL: {self.driver.current_url if self.driver else 'driver not initialized'}")
        finally:
            self.cleanup()
    