import os
import sys

# 현재 스크립트의 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from crawlers.jobkorea_crawler import JobKoreaCrawler
from crawlers.saramin_crawler import SaraminCrawler
from common.constants import OUTPUT_DIRS

def run_crawler(crawler_name):
    crawlers = {
        'jobkorea': lambda: JobKoreaCrawler(OUTPUT_DIRS['jobkorea']),
        'saramin': lambda: SaraminCrawler(OUTPUT_DIRS['saramin']),
    }
    
    if crawler_name not in crawlers:
        print(f"지원하지 않는 크롤러입니다. 지원 크롤러: {', '.join(crawlers.keys())}")
        return
        
    crawler = crawlers[crawler_name]()
    try:
        crawler.initialize()
        crawler.crawl()
    finally:
        crawler.cleanup()

def main():
    # 명령줄 인자 처리
    if len(sys.argv) < 2:
        print("사용법: python main.py [jobkorea|saramin|all]")
        return
        
    crawler_name = sys.argv[1].lower()
    
    if crawler_name == 'all':
        for name in ['jobkorea', 'saramin']:
            print(f"\n=== {name} 크롤링 시작 ===")
            run_crawler(name)
    else:
        run_crawler(crawler_name)

if __name__ == "__main__":
    main()