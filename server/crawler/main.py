from flask import Flask, jsonify
import os
import sys
from typing import Dict, Any

# 현재 스크립트의 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from crawlers.jobkorea_crawler import JobKoreaCrawler
from crawlers.saramin_crawler import SaraminCrawler
from common.constants import OUTPUT_DIRS


app = Flask(__name__)

# 크롤러 실행 로직 
def execute_crawler(crawler_name: str) -> Dict[str, Any]:
    crawlers = {
        'jobkorea': lambda: JobKoreaCrawler(OUTPUT_DIRS['jobkorea']),
        'saramin': lambda: SaraminCrawler(OUTPUT_DIRS['saramin']),
    }
    
    if crawler_name not in crawlers:
        raise ValueError(f"지원하지 않는 크롤러입니다. 지원 크롤러: {', '.join(crawlers.keys())}")        

    crawler = crawlers[crawler_name]()
    crawler.initialize()
    result = crawler.crawl()
    crawler.cleanup()
    
    return result    

#웹 API 엔드 포인트
@app.route('/crawl/<crawler_name>')
def run_crawler(crawler_name: str) -> Dict[str, Any]:
    try:
        result = execute_crawler(crawler_name)
        return jsonify({
            "status": "success",
            "crawler": crawler_name,
            "result": result
        })
    except ValueError as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# CLI 인터페이스 
def main():
    # 명령줄 인자 처리
    if len(sys.argv) < 2:
        print("사용법: python main.py [jobkorea|saramin|all]")
        return
        
    crawler_name = sys.argv[1].lower()
    
    try: 
        if crawler_name == 'all':
            for name in ['jobkorea', 'saramin']:
                print(f"\n=== {name} 크롤링 시작 ===")
                result = execute_crawler(name)
                print(f"크롤링 완료: {result}")
        else:
            result = execute_crawler(crawler_name)
            print(f"크롤링 완료: {result}")
    except Exception as e:
        print(f"에러 발생: {str(e)}")
        sys.exit(1)
        
@app.route('/healthcheck')
def healthcheck():
    return jsonify({"status": "healthy"})
        
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['--server', '-s']:
        # 서버 모드로 실행 
        port = int(os.environ.get('PORT', 8000))
        # 프로덕션 환경에서는 debug = False로 설정
        debug = os.environ.get('FLASK_ENV') == 'development'
        app.run(
            host='0.0.0.0',
            port=port,
            debug=debug
        )
    else: 
        # CLI 모드로 실행
        main()