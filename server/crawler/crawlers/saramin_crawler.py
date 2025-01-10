# Python 내장 라이브러리 
import os
import sys
import hashlib
import logging
from datetime import datetime
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
        print(f"처리할 데이터 개수: {len(saramin_data)}")
        
        # 크롤링한 데이터 처리 및 저장 
        for job_data in saramin_data:
            try: 
                print(f"현재 처리중인 데이터: {job_data}")  
                # 고유 ID 생성
                company_id = self._generate_hash(job_data['회사명'])
                post_id = self._generate_hash(job_data['공고URL'])
                print(f"생성된 ID - company_id: {company_id}, post_id: {post_id}")
                
                # 회사 정보 저장
                try: 
                    self._save_compnay_info(company_id, job_data)
                except Exception as e:
                    print(f"회사 정보 저장 실패: {str(e)}")
                    raise
                # 태그 처리 및 저장 
                try:
                    tags = self._process_tags(job_data)
                except Exception as e:
                    print(f"태그 처리 실패: {str(e)}")
                    raise
                # 채용 공고 저장
                try: 
                    self._save_job_posting(company_id, post_id, job_data)
                except Exception as e:
                    print(f"채용공고 저장 실패: {str(e)}")
                    raise                
                # 공고-태그 매핑 저장
                try:
                    self._save_job_tags(post_id, tags)
                except Exception as e:
                    print(f"태그매핑 저장 실패: {str(e)}")
                    raise           
                
                self.logger.info(f"데이터 처리 완료: {job_data['회사명']} - {job_data['공고제목']}")
                
            except Exception as e:
                self.logger.error(f"데이터 처리 중 오류 ({job_data['회사명']}): {str(e)}")
                print(f"전체 처리  실패: {str(e)}")
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

    def _process_location_tag(self, location: str) -> List[str]:
        tags = []
        try: 
            location = location.strip()
            parts = location.split()
            
            main_region = parts[0].replace('전체', '').replace('외', '')
            main_region_name = f"{main_region}전체"
            main_region_id = self._generate_hash(f"location_{main_region}")

            main_tag_data = {
                'PK': f"TAG#location",
                'SK': f"TAG#{main_region_id}",
                'tag_id': main_region_id,
                'category': 'location',
                'name': main_region_name,  # 예: '서울전체', '경기전체', '인천전체'
                'level': 1,
                'parent_id': None,
                'count': 1,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'GSI1PK': "TAG#ALL",
                'GSI1SK': f"1#{main_region_id}"
            }
            self.tag_repo.save(main_tag_data)
            tags.append(main_region_id)
            
            if len(parts) > 1:
                district = parts[1]
                district_full_name = f"{main_region} {district}"
                district_id = self._generate_hash(f"location_{district_full_name}")
                
                district_tag_data = {
                    'PK': f"TAG#location",
                    'SK': f"TAG#{district_id}",
                    'tag_id': district_id,
                    'category': 'location',
                    'name': district_full_name,
                    'level': 2,
                    'parent_id': main_region_id,
                    'count': 1,
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat(),
                    'GSI1PK': "TAG#ALL",
                    'GSI1SK': f"2#{district_id}"                    
                }
                self.tag_repo.save(district_tag_data)
                tags.append(district_id)
                
            return tags
        except Exception as e:
            self.logger.error(f"위치 태그 처리 중 오류 ({location}): {str(e)}")
            return tags

    def _process_tags(self, job_data: Dict) -> None:
        # 2. 모든 태그 처리 
        tags = []
        
        # (1) 직무분야 태그 처리
        if job_data.get('직무분야'):
            position_tags = self._process_position_tags(job_data['직무분야'])
            tags.extend(position_tags)
            
        # (2) 경력/고용형태 태그 처리
        if job_data.get('경력/고용형태'):
            career_type_tags = self._process_career_type_tags(job_data['경력/고용형태'])
            tags.extend(career_type_tags)
            
        # (3) 학력 태그 처리 
        if job_data.get('학력'):
            education_tag = self._process_education_tag(job_data['학력'])
            if education_tag:
                tags.append(education_tag)

        # (4) 지역 태그 처리 
        if job_data.get('근무지'):
            location_tags = self._process_location_tag(job_data['근무지'])
            tags.extend(location_tags)
        
        return tags
    
    def _process_position_tags(self, position_str: str) -> List[str]:
        # 직무분야 태그 처리 
        tags = []
        if not position_str:
            return tags
        
        positions = [pos.strip() for pos in position_str.split(',')]
        
        for position in positions:
            if not position:
                continue
        
            tag_id = self._generate_hash(f"position_{position}")
            tag_data = {
                'PK': f"TAG#position",
                'SK': f"TAG#{tag_id}",
                'tag_id': tag_id,
                'category': 'position',
                'name': position,
                'level': 1,
                'parent_id': None,
                'count': 1,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'GSI1PK': "TAG#ALL",
                'GSI1SK': f"1#{tag_id}"
            }
            self.tag_repo.save(tag_data)
            tags.append(tag_id)
    
        return tags
    
    def _process_career_type_tags(self, career_type_str: str) -> List[str]:
        #  경력/고용형태 태그 처리
        tags = []
        if not career_type_str:
            return tags

        career_types = [ct.strip() for ct in career_type_str.split(' · ')]
        
        for career_type in career_types:
            career_type = career_type.replace(' 외', '').strip()
            if not career_type:
                continue
    
            tag_id = self._generate_hash(f"skill_{career_type}")
            tag_data = {
                'PK': f"TAG#skill",
                'SK': f"TAG#{tag_id}",
                'tag_id': tag_id,
                'category': 'skill',
                'name': career_type,
                'level': 1,
                'parent_id': None,
                'count': 1,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'GSI1PK': "TAG#ALL",
                'GSI1SK': f"1#{tag_id}"
            }
            self.tag_repo.save(tag_data)
            tags.append(tag_id)
        
        return tags            
            
    def _process_education_tag(self, education_str: str) -> Optional[str]:
        if not education_str: 
            return None
        
        education = education_str.replace('↑', '').strip()
        if not education:
            return None

        tag_id = self._generate_hash(f"skill_{education}")
        tag_data = {
            'PK': f"TAG#skill",
            'SK': f"TAG#{tag_id}",
            'tag_id': tag_id,
            'category': 'skill',
            'name': education,
            'level': 1,
            'parent_id': None,
            'count': 1,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'GSI1PK': "TAG#ALL",
            'GSI1SK': f"1#{tag_id}"
        }
        self.tag_repo.save(tag_data)
        return tag_id

    def _save_job_posting(self, company_id: str, post_id: str, job_data: Dict) -> None:
        # 3. 채용 공고 저장
        deadline_str = self._parse_deadline(job_data['마감일'])
        rec_idx = self._extract_rec_idx(job_data['공고URL'])
        
        job_data_processed = {
            'PK': f"COMPANY#{company_id}",
            'SK': f"JOB#{post_id}",
            'post_id': post_id,
            'post_name': job_data['공고제목'],
            'company_id': company_id,
            'company_name': job_data['회사명'],
            'is_closed': deadline_str,
            'post_url': job_data['공고URL'],
            'rec_idx': rec_idx,
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
            
    def _parse_deadline(self, deadline_str: str) -> str:
        from common.utils import parsse_deadline_date
        return parsse_deadline_date(deadline_str)

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
    
    def _extract_rec_idx(self, url:str) -> Optional[str]:
        try:
            from urllib.parse import urlparse, parse_qs
            parsed_url = urlparse(url)
            params = parse_qs(parsed_url.query)
            rec_idx = params.get('rec_idx', [None])[0]
            return rec_idx
        except Exception as e:
            self.logger.error(f"rec_idx 추출 실패 ({url}: {str(e)})")
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
        saramin_list = []
        max_pages = 2
        
        for page in range(1, max_pages + 1):
            try:
                if page > 1:
                    try:
                        # 페이지네이션 영역 찾기
                        pagination = self.wait_for_element(By.CLASS_NAME, "PageBox")
                        if pagination:
                            # 다음 페이지 버튼 찾기 (page 속성값으로 찾기)
                            next_page_button = self.driver.find_element(
                                By.CSS_SELECTOR, 
                                f"button.BtnType.SizeS[page='{page}']"
                            )
                            
                            # 버튼이 보이도록 스크롤
                            self.driver.execute_script(
                                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
                                next_page_button
                            )
                            self.wait_random(1, 2)  # 스크롤 후 자연스러운 대기
                            
                            # 클릭 전 약간의 지연
                            self.wait_random(0.5, 1)
                            
                            # 버튼 클릭
                            next_page_button.click()
                            
                            # 페이지 로딩 대기
                            self.wait_random(2, 3)
                            
                            # 새 페이지의 컨텐츠가 로드될 때까지 대기
                            if not self.wait_for_element(By.CLASS_NAME, "box_item"):
                                self.logger.warning(f"페이지 {page}의 컨텐츠를 찾을 수 없습니다.")
                                continue
                                
                        else:
                            self.logger.warning(f"페이지 {page}의 페이지네이션을 찾을 수 없습니다.")
                            continue
                    
                    except Exception as e:
                        self.logger.error(f"페이지 {page} 이동 중 오류 발생: {str(e)}")
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
            if not os.path.exists(self.output_dir):
                os.mkdir(self.output_dir)
                print(f"출력 디렉토리 생성: {self.output_dir}")

            self.driver.get(self.url)
            print("URL 접속 시도:", self.url)
            
            # 초기 페이지 로딩 대기
            if not self.wait_for_element(By.CSS_SELECTOR, "div.box_item"):
                raise TimeoutException("초기 페이지 로딩 실패")
            print("페이지 로딩 완료")
            
            # 채용공고 크롤링 
            saramin_data = self.crawl_jobs()
            print(f"크롤링된 데이터 수: {len(saramin_data)}")
            
            if saramin_data:
                print("데이터 처리 시작")
                try: 
                    # CSV 파일 저장
                    output_file = os.path.join(self.output_dir, 'saramin_job.csv')
                    save_to_csv(saramin_data, output_file)
                    print(f"CSV 파일 저장 완료: {output_file}")
                    
                    # DynamoDB에 데이터 저장
                    print("DynamoDB 저장 시작")
                    self.process_and_save_data(saramin_data)
                    print("DynamoDB 저장 완료")
                except PermissionError as e:
                    print(f"파일 저장 권한 오류: {str(e)}")
                    print("DynamoDB 저장 시작")
                    self.process_and_save_data(saramin_data)
                    print("DynamoDB 저장 완료")
                except Exception as e:
                    print(f"데이터 처리 중 오류 발생: {str(e)}")
                    raise
                
                print(f"사람인 공고 크롤링이 완료되었습니다. 총 {len(saramin_data)}개의 공고가 수집되었습니다.")
            else:
                print("크롤링된 데이터가 없습니다.")
                
        except TimeoutException:
            self.logger.error("페이지 로딩 시간 초과. 네트워크 상태를 확인하세요.")
        except Exception as e:
            self.logger.error(f"크롤링 중 오류 발생: {str(e)}")
        finally:
            self.cleanup()