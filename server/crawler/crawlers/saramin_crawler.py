from base.base_crawler import BaseCrawler
import os
from datetime import datetime, timedelta
import hashlib
from typing import Dict
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from common.utils import save_to_csv
from common.constants import URLS

import sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from aws_service.factory import create_repository
from aws_service.services.common.enums import JobStatus, TagCategory

class SaraminCrawler(BaseCrawler):
    def __init__(self, output_dir):
        super().__init__(output_dir)
        self.url = URLS['saramin']
        # Repository 초기화
        self.company_repo = create_repository('mongodb', 'companies')
        self.job_repo = create_repository('mongodb', 'jobs')
        self.tag_repo = create_repository('mongodb', 'tags')
        self.job_tag_repo = create_repository('mongodb', 'job_tags')
        
    def process_and_save_data(self, saramin_data):
        for job_data in saramin_data:
            try:
                # 고유 ID 생성
                company_id = hashlib.md5(job_data['회사명'].encode()).hexdigest()
                post_id = hashlib.md5(job_data['공고URL'].encode()).hexdigest()
                
                # 1. 기업 정보 저장
                company_data = {
                    '_id': company_id,  # _id로 변경
                    'company_id': company_id,
                    'company_name': job_data['회사명'],
                    'created_at': datetime.now(),
                    'updated_at': datetime.now()
                }
                self.company_repo.update(company_id, company_data, upsert=True)
                print(f"기업 정보 저장/업데이트: {company_data['company_name']}")

                # 2. 태그 처리
                tags = []
                if job_data['직무분야']:
                    for tag in job_data['직무분야'].split(','):
                        tag = tag.strip()
                        tag_id = hashlib.md5(f"skill_{tag}".encode()).hexdigest()
                        tag_data = {
                            '_id': tag_id,  # _id로 변경
                            'tag_id': tag_id,
                            'category': TagCategory.SKILL.value,
                            'name': tag,
                            'level': 1,
                            'count': 1,
                            'created_at': datetime.now(),
                            'updated_at': datetime.now()
                        }
                        self.tag_repo.update(tag_id, tag_data, upsert=True)
                        tags.append(tag_id)

                # 지역 태그
                if job_data['근무지']:
                    location = job_data['근무지'].split()[0]  # 첫 번째 단위(시/도)만 사용
                    tag_id = hashlib.md5(f"location_{location}".encode()).hexdigest()
                    tag_data = {
                        '_id': tag_id,  # _id로 변경
                        'tag_id': tag_id,
                        'category': TagCategory.LOCATION.value,
                        'name': location,
                        'level': 1,
                        'count': 1,
                        'created_at': datetime.now(),
                        'updated_at': datetime.now()
                    }
                    self.tag_repo.update(tag_id, tag_data, upsert=True)
                    tags.append(tag_id)

                # 고용형태 태그
                if job_data['경력/고용형태']:
                    emp_type = job_data['경력/고용형태'].split('·')[-1].strip()
                    tag_id = hashlib.md5(f"position_{emp_type}".encode()).hexdigest()
                    tag_data = {
                        '_id': tag_id,  # _id로 변경
                        'tag_id': tag_id,
                        'category': TagCategory.POSITION.value,
                        'name': emp_type,
                        'level': 1,
                        'count': 1,
                        'created_at': datetime.now(),
                        'updated_at': datetime.now()
                    }
                    self.tag_repo.update(tag_id, tag_data, upsert=True)
                    tags.append(tag_id)

                # 3. 채용 공고 저장
                deadline_date = self._parse_deadline(job_data['마감일'])
                job_data_processed = {
                    '_id': post_id,  # _id로 변경
                    'post_id': post_id,
                    'post_name': job_data['공고제목'],
                    'company_id': company_id,
                    'company_name': job_data['회사명'],
                    'is_closed': deadline_date,
                    'post_url': job_data['공고URL'],
                    'status': JobStatus.ACTIVE.value,
                    'created_at': datetime.now(),
                    'updated_at': datetime.now(),
                    'tags': tags
                }
                self.job_repo.update(post_id, job_data_processed, upsert=True)
                print(f"채용공고 저장: {job_data['공고제목']}")

                # 4. 공고-태그 매핑 저장
                for tag_id in tags:
                    job_tag_id = hashlib.md5(f"{post_id}_{tag_id}".encode()).hexdigest()
                    mapping_data = {
                        '_id': job_tag_id,  # _id로 변경
                        'job_tag_id': job_tag_id,
                        'job_id': post_id,
                        'tag_id': tag_id,
                        'created_at': datetime.now()
                    }
                    self.job_tag_repo.update(job_tag_id, mapping_data, upsert=True)

            except Exception as e:
                print(f"데이터 처리 중 오류 발생 (회사: {job_data['회사명']}): {e}")
                continue

            
    def _parse_deadline(self, deadline_str: str) -> datetime:
        """마감일 문자열을 datetime으로 변환"""
        try:
            if 'D-' in deadline_str:
                days = int(deadline_str.replace('D-', ''))
                return datetime.now() + timedelta(days=days)
            elif '내일마감' in deadline_str:
                return datetime.now() + timedelta(days=1)
            else:
                return datetime.now() + timedelta(days=30)  # 기본값
        except:
            return datetime.now() + timedelta(days=30)  # 파싱 실패시 기본값
                    
    def _determine_tag_category(self, tag: str) -> str:
        """태그 카테고리 결정"""
        if '신입' in tag or '경력' in tag:
            return 'experience'
        elif '정규직' in tag or '계약직' in tag or '인턴' in tag:
            return 'employment_type'
        elif '학력' in tag or '대졸' in tag or '초대졸' in tag:
            return 'education'
        else:
            return 'job_field'
        
    def crawl_jobs(self):
        saramin_list = []
        max_retries = 3
        max_pages = 2
        
        for page in range(1, max_pages + 1):
            try:
                if page > 1:
                    page_url = f"{self.url}?page={page}"
                    if not self.safe_page_navigation(page_url):
                        continue
                
                # 명시적 대기 조건
                if not self.wait_for_element(By.CLASS_NAME, "box_item"):
                    continue
                
                # 자연스러운 스크롤 동작
                self.natural_scroll()
                
                # HTML 파싱
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')            
                job_items = soup.select('.box_item')
                
                if not job_items:
                    print(f"페이지 {page}: 공고 항목을 찾을 수 없습니다. 다음 페이지로 진행합니다.")
                    continue
                
                print(f"페이지 {page} - 발견된 채용공고 수: {len(job_items)}")
                
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
                            sector_spans = sector_elem.select('span')
                            sector_texts = [span.text.strip() for span in sector_spans if span.text.strip()]
                            sector_texts = [text for text in sector_texts if text != '외']
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
                        
                        # 공고 URL
                        url_elem = item.select_one('.job_tit .str_tit')
                        job_url = ''
                        if url_elem and 'href' in url_elem.attrs:
                            job_url = 'https://www.saramin.co.kr' + url_elem['href']
                        
                        if company and title:  # 필수 정보가 있는 경우만 저장
                            job_dict = {
                                '회사명': company,
                                '공고제목': title,
                                '직무분야': sector,
                                '근무지': location,
                                '경력/고용형태': career,
                                '학력': education,
                                '마감일': deadline,
                                '등록일': posted,
                                '공고URL': job_url
                            }
                            
                            saramin_list.append(job_dict)
                            print(f"수집된 공고: {company} - {title}")
                        
                        self.wait_random(0.5, 1)
                        
                    except Exception as e:
                        print(f"항목 파싱 중 오류 발생: {e}")
                        continue
                
                # 페이지 이동 전 대기
                self.wait_random(8, 15)
                
            except Exception as e:
                print(f"페이지 {page} 처리 중 오류 발생: {e}")
                continue
        
        print(f"총 수집된 공고 수: {len(saramin_list)}")
        return saramin_list
    
    def crawl(self):
        try: 
            self.driver.get(self.url)
            print("URL 접속 시도:", self.url)
            
            # 초기 페이지 로딩 대기
            if not self.wait_for_element(By.CSS_SELECTOR, "div.box_item"):
                raise TimeoutException("초기 페이지 로딩 실패")
            print("페이지 로딩 완료")
            
            saramin_data = self.crawl_jobs()
            
            if saramin_data:
                # CSV 파일 저장 
                output_file = os.path.join(self.output_dir, 'saramin_job.csv')
                save_to_csv(saramin_data, output_file)
                
                # MongoDB에 데이터 저장
                self.process_and_save_data(saramin_data)
                
                print(f"사람인 공고 크롤링이 완료되었습니다. 총 {len(saramin_data)}개의 공고가 수집되었습니다.")
            else:
                print("크롤링된 데이터가 없습니다.")
                
        except TimeoutException:
            print("페이지 로딩 시간이 초과되었습니다. 네트워크 상태를 확인해주세요.")
        except Exception as e:
            print(f"크롤링 중 오류 발생: {e}")