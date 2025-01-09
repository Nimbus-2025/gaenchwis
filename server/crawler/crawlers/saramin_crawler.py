# Python 내장 라이브러리 
import os
import sys
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
# 외부 라이브러리 
import boto3
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# 로컬 애플리케이션
from base.base_crawler import BaseCrawler
from common.utils import save_to_csv
from common.constants import URLS
# AWS 서비스 관련
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from aws_service.factory import create_repository
from aws_service.services.common.constants import TableNames
from aws_service.services.dynamodb.setup import setup_dynamodb

class SaraminCrawler(BaseCrawler):
    def __init__(self, output_dir: str) -> None:
        #크롤러 초기화 
        super().__init__(output_dir)
        self.url = URLS['saramin']
        self.logger = self._setup_logger()
        
        # AWS 리소스 및 Repository 초기화
        self._setup_aws_resources()
        self._initialize_repositories()
        
    def _setup_logger(self) -> logging.Logger:
        # 로깅 설정
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        # 파일 핸들러 추가
        fh = logging.FileHandler(os.path.join(self.output_dir, 'saramin_crawler.log'), encoding='utf-8')
        fh.setLevel(logging.INFO)
        
        # 포맷터 설정
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
        return logger
    
    def _setup_aws_resources(self) -> None:
        # AWS DynamoDB 리소스 초기화
        try:
            self.dynamodb= boto3.resource(
                'dynamodb',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=os.getenv('AWS_REGION', 'ap-northeast-2')
            )
            setup_dynamodb(self.dynamodb)  # 테이블 생성 실행
        
            # 테이블 존재 여부 확인
            tables = list(self.dynamodb.tables.all())
            self.logger.info(f"사용 가능한 테이블: {[table.name for table in tables]}")
        except Exception as e:
            self.logger.error(f"AWS 리소스 설정 실패: {str(e)}")
            raise
        
    def _initialize_repositories(self) -> None:
        # Repository 객체들 초기화 
        try:
            self.company_repo = create_repository('dynamodb', TableNames.COMPANIES)
            self.job_repo = create_repository('dynamodb', TableNames.JOB_POSTINGS)
            self.tag_repo = create_repository('dynamodb', TableNames.TAGS)
            self.job_tag_repo = create_repository('dynamodb', TableNames.JOB_TAGS)
            
            self.logger.info("모든 Repository 초기화 완료")
            
        except Exception as e:
            self.logger.error(f"Repository 초기화 실패: {str(e)}")
            raise
        
    def _generate_hash(self, text: str) -> str:
        return hashlib.md5(text.encode()).hexdigest()
        
    def process_and_save_data(self, saramin_data: List[Dict]) -> None:
        # 크롤링한 데이터 처리 및 저장 
        for job_data in saramin_data:
            try:
                # 고유 ID 생성
                company_id = self._generate_hash(job_data['회사명'])
                post_id = self._generate_hash(job_data['공고URL'])
                
                # 회사 정보 저장
                self._save_compnay_info(company_id, job_data)
                
                # 태그 처리 및 저장 
                tags = self._process_tags(job_data)
                
                # 채용 공고 저장
                self._save_job_posting(company_id, post_id, job_data)
                
                # 공고-태그 매핑 저장
                self._save_job_tags(post_id, tags)
                
                self.logger.info(f"데이터 처리 완료: {job_data['회사명']} - {job_data['공고제목']}")
                
            except Exception as e:
                self.logger.error(f"데이터 처리 중 오류 ({job_data['회사명']}): {str(e)}")
                continue                
                
                
    def _save_compnay_info(self, company_id: str, job_data: Dict) -> None:
        # 1. 기업 정보 저장
        company_data = {
            'PK': f"COMPANY#{company_id}",  # 직접 값 할당
            'SK': f"METADATA#{company_id}",
            'company_id': company_id,
            'company_name': job_data['회사명'],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'GSI1PK': "COMPANY#ALL",
            'GSI1SK': job_data['회사명']
        }
                
        self.company_repo.save(company_data)
        print(f"기업 정보 저장: {job_data['회사명']}")

    def _process_tags(self, job_data: Dict) -> None:
        # 2. 태그 처리
        tags = []
        if job_data['직무분야']:
            for tag in job_data['직무분야'].split(','):
                tag = tag.strip()
                tag_id = self._generate_hash(f"skill_{tag}")
                tag_data = {
                    'PK': f"TAG#skill",
                    'SK': f"TAG#{tag_id}",
                    'tag_id': tag_id,
                    'category': 'skill',
                    'name': tag,
                    'level': 1,
                    'count': 1,
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat(),
                    'GSI1PK': "TAG#ALL",
                    'GSI1SK': f"1#{tag_id}"
                }
                self.tag_repo.save(tag_data)
                tags.append(tag_id)

                # 지역 태그 처리
                if job_data['근무지']:
                    location = job_data['근무지'].split()[0]
                    tag_id = hashlib.md5(f"location_{location}".encode()).hexdigest()
                    
                    tag_data = {
                        'PK': f"TAG#location",
                        'SK': f"TAG#{tag_id}",
                        'tag_id': tag_id,
                        'category': 'location',
                        'name': location,
                        'level': 1,
                        'count': 1,
                        'created_at': datetime.now().isoformat(),
                        'updated_at': datetime.now().isoformat(),
                        'GSI1PK': "TAG#ALL",
                        'GSI1SK': f"1#{tag_id}"
                    }
                    self.tag_repo.save(tag_data)
                    tags.append(tag_id)
            return tags

    def _save_job_posting(self, company_id: str, post_id: str, job_data: Dict) -> None:
        # 3. 채용 공고 저장
        deadline_date = self._parse_deadline(job_data['마감일'])
        job_data_processed = {
            'PK': f"COMPANY#{company_id}",
            'SK': f"JOB#{post_id}",
            'post_id': post_id,
            'post_name': job_data['공고제목'],
            'company_id': company_id,
            'company_name': job_data['회사명'],
            'is_closed': deadline_date.isoformat(),
            'post_url': job_data['공고URL'],
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'GSI1PK': "STATUS#active",
            'GSI1SK': datetime.now().isoformat(),
            'GSI2PK': "JOB#ALL",
            'GSI2SK': datetime.now().isoformat()
        }
        self.job_repo.save(job_data_processed)
        self.logger.info(f"채용공고 저장: {job_data['공고제목']}")
        print(f"채용공고 저장: {job_data['공고제목']}")

    def _save_job_tags(self, post_id: str, tags: List[str]) -> None:
        # 4. 공고-태그 매핑 저장
            for tag_id in tags:
                job_tag_id = self._generate_hash(f"{post_id}_{tag_id}")

                mapping_data = {
                    'PK': f"JOB#{post_id}",
                    'SK': f"TAG#{tag_id}",
                    'job_tag_id': job_tag_id,
                    'job_id': post_id,
                    'tag_id': tag_id,
                    'created_at': datetime.now().isoformat(),
                    'GSI1PK': f"TAG#{tag_id}",
                    'GSI1SK': f"JOB#{post_id}"
                }
            
            self.job_tag_repo.save(mapping_data)
            
    def _parse_deadline(self, deadline_str: str) -> datetime:
        # 마감일 문자열을 datetime으로 변환
        try:
            if 'D-' in deadline_str:
                days = int(deadline_str.replace('D-', ''))
                return datetime.now() + timedelta(days=days)
            elif '내일마감' in deadline_str:
                return datetime.now() + timedelta(days=1)
            else:
                return datetime.now() + timedelta(days=30)  # 기본값
        except Exception as e:
            self.logger.warning(f"마감일 파싱 실패 ({deadline_str}): {str(e)}")
            return datetime.now() + timedelta(days=30)     

    def _parse_job_item(self, item: BeautifulSoup) -> Optional[Dict]:
        # 채용공고 항목 파싱 
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
                
            # URL 추출
            url_elem = item.select_one('.job_tit .str_tit')
            job_url = ''
            if url_elem and 'href' in url_elem.attrs:
                job_url = 'https://www.saramin.co.kr' + url_elem['href']
                
            if not (company and title):  # 필수 필드 검증
                return None
            
            print(f"수집된 공고: {company} - {title}")
                
            return {
                '회사명': company,
                '공고제목': title,
                '직무분야': self._parse_sector(sector_elem),
                '근무지': location,
                '경력/고용형태': career,
                '학력': education,
                '마감일': deadline,
                '등록일': posted,
                '공고URL': job_url
            }
            
        except Exception as e:
            self.logger.error(f"항목 파싱 중 오류: {str(e)}")
            return None
        
    def _parse_sector(self, sector_elem: Optional[BeautifulSoup]) -> str:
        # 직무분야 파싱
        if not sector_elem:
            return ''
            
        sector_spans = sector_elem.select('span')
        sector_texts = [span.text.strip() for span in sector_spans if span.text.strip()]
        sector_texts = [text for text in sector_texts if text != '외']
        return ', '.join(sector_texts)
        
    def crawl_jobs(self) -> List[Dict]:
        # 채용공고 크롤링 수행 
        saramin_list = []
        max_pages = 2
        
        for page in range(1, max_pages + 1):
            try:
                # 페이지 이동
                if page > 1:
                    page_url = f"{self.url}?page={page}"
                    if not self.safe_page_navigation(page_url):
                        self.logger.warning(f"페이지 {page} 이동 실패")
                        continue
                
                # 채용공고 항목 대기 
                if not self.wait_for_element(By.CLASS_NAME, "box_item"):
                    self.logger.warning(f"페이지 {page}에서 채용공고 항목을 찾을 수 없음")
                    continue
                
                # 자연스러운 스크롤 동작
                self.natural_scroll()
                
                # HTML 파싱
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')            
                job_items = soup.select('.box_item')
                
                if not job_items:
                    print(f"페이지 {page}: 공고 항목을 찾을 수 없습니다. 다음 페이지로 진행합니다.")
                    continue
                
                self.logger.info(f"페이지 {page} - 발견된 채용공고 수: {len(job_items)}")
                
                for item in job_items:
                    parsed_item = self._parse_job_item(item)
                    if parsed_item: 
                        saramin_list.append(parsed_item)
                        self.logger.info(f"수집된 공고: {parsed_item['회사명']} - {parsed_item['공고제목']}")
                    
                    self.wait_random(2, 3)  # 자연스러운 딜레이
                
                self.wait_random(15, 30) # 페이지 이동 전 딜레이 
                
            except TimeoutException:
                self.logger.error(f"페이지 {page} 처리 중 시간 초과")
                continue
            except Exception as e:
                self.logger.error(f"페이지 {page} 처리 중 오류 발생: {str(e)}")
                continue
        
        self.logger.info(f"총 수집된 공고 수: {len(saramin_list)}")
        return saramin_list
    
    def crawl(self):
        # 크롤링 메인 프로세스 
        try: 
            self.driver.get(self.url)
            print("URL 접속 시도:", self.url)
            
            # 초기 페이지 로딩 대기
            if not self.wait_for_element(By.CSS_SELECTOR, "div.box_item"):
                raise TimeoutException("초기 페이지 로딩 실패")
            print("페이지 로딩 완료")
            
            # 채용공고 크롤링 
            saramin_data = self.crawl_jobs()
            
            if saramin_data:
                # CSV 파일 저장
                output_file = os.path.join(self.output_dir, 'saramin_job.csv')
                save_to_csv(saramin_data, output_file)
                self.logger.info(f"CSV 파일 저장 완료: {output_file}")
                
                # DynamoDB에 데이터 저장
                self.process_and_save_data(saramin_data)
                
                print(f"사람인 공고 크롤링이 완료되었습니다. 총 {len(saramin_data)}개의 공고가 수집되었습니다.")
            else:
                print("크롤링된 데이터가 없습니다.")
        except TimeoutException:
            self.logger.error("페이지 로딩 시간 초과. 네트워크 상태를 확인하세요.")
        except Exception as e:
            self.logger.error(f"크롤링 중 오류 발생: {str(e)}")
        finally:
            self.cleanup()

    # def _determine_tag_category(self, tag: str) -> str:
    #     """태그 카테고리 결정"""
    #     if '신입' in tag or '경력' in tag:
    #         return 'experience'
    #     elif '정규직' in tag or '계약직' in tag or '인턴' in tag:
    #         return 'employment_type'
    #     elif '학력' in tag or '대졸' in tag or '초대졸' in tag:
    #         return 'education'
    #     else:
    #         return 'job_field'