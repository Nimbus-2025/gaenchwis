from base.base_crawler import BaseCrawler
import os
import time
import random
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from common.utils import save_to_csv
from common.constants import URLS

class SaraminCrawler(BaseCrawler):
    def __init__(self, output_dir):
        super().__init__(output_dir)
        self.url = URLS['saramin']
        
    def crawl_jobs(self):
        saramin_list = []
        max_retries = 3
        max_pages = 10
        
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
            
            # 초기 페이지 로딩 대기
            if not self.wait_for_element(By.CSS_SELECTOR, "div.box_item"):
                raise TimeoutException("초기 페이지 로딩 실패")
            
            saramin_data = self.crawl_jobs()
            
            if saramin_data:
                output_file = os.path.join(self.output_dir, 'saramin_job.csv')
                save_to_csv(saramin_data, output_file)
                print(f"사람인 공고 크롤링이 완료되었습니다. 총 {len(saramin_data)}개의 공고가 수집되었습니다.")
            else:
                print("크롤링된 데이터가 없습니다.")
                
        except TimeoutException:
            print("페이지 로딩 시간이 초과되었습니다. 네트워크 상태를 확인해주세요.")
        except Exception as e:
            print(f"크롤링 중 오류 발생: {e}")