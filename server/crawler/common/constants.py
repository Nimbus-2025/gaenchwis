# 공통으로 사용되는 상수들 
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59'
]

# 크롤링 결과 저장 경로 
OUTPUT_DIRS = {
    'saramin': 'saramin_crawling_results',
    'jobkorea': 'jobkorea_crawling_results'
}

# URL 상수
URLS = {
    'saramin': 'https://www.saramin.co.kr/zf_user/jobs/list/job-category?cat_mcls=2&loc_mcd=101000&panel_type=&search_optional_item=n&search_done=y&panel_count=y&preview=y',
    'jobkorea': 'https://www.jobkorea.co.kr/recruit/joblist?menucode=duty'
}