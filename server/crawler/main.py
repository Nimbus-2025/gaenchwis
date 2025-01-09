# Python 내장 라이브러리 
from flask import Flask, jsonify, request, Response
import os
import sys
from typing import Dict, Any
from datetime import datetime
import logging 
from functools import wraps
# 현재 스크립트의 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
# 로컬 임포트
from crawlers.jobkorea_crawler import JobKoreaCrawler
from crawlers.saramin_crawler import SaraminCrawler
from common.constants import OUTPUT_DIRS
from common.config import Config


app = Flask(__name__)

class CrawlerExecutor:
    # 크롤러 실행 관리하는 클래스 
    def __init__(self, config: Config):
        self.config = config
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        # 로깅 설정
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        # Docker 환경에서는 stdout으로 로그 출력
        if os.environ.get('DOCKER_CONTAINER'):
            handler = logging.StreamHandler(sys.stdout)
        else:
            # 로컬 환경에서는 파일로 로그 출력
            log_dir = os.path.join(current_dir, 'logs')
            os.makedirs(log_dir, exist_ok=True)
            handler = logging.FileHandler(os.path.join(log_dir, 'crawler_executor.log'))
            
        # 파일 핸들러 추가
        handler = logging.FileHandler('crawler_executor.log')
        handler.setLevel(logging.INFO)
        
        # 포맷터 설정
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger

    def execute_crawler(self, crawler_name: str) -> Dict[str, Any]:
        # 크롤러 실행 로직 
        crawlers = {
            'jobkorea': lambda: JobKoreaCrawler(OUTPUT_DIRS['jobkorea']),
            'saramin': lambda: SaraminCrawler(OUTPUT_DIRS['saramin']),
        }
        
        if crawler_name not in crawlers:
            raise ValueError(f"지원하지 않는 크롤러입니다. 지원 크롤러: {', '.join(crawlers.keys())}")        

        try:
            self.logger.info(f"{crawler_name} 크롤러 실행 시작")
        
            # 크롤러 관련 환경변수 설정
            os.environ['CHROME_DRIVER_PATH'] = self.config.CHROME_DRIVER_PATH
            os.environ['HEADLESS'] = str(self.config.HEADLESS).lower()
        
            crawler = crawlers[crawler_name]()
            crawler.initialize()
            result = crawler.crawl()
            crawler.cleanup()
            self.logger.info(f"{crawler_name} 크롤러 실행 완료")
            return result    
        except Exception as e:
            self.logger.error(f"{crawler_name} 크롤러 실행 중 오류: {str(e)}")
            raise
        
class APIServer:
    # Flask API 서버 클래스
    def __init__(self, config: Config):
        self.app = Flask(__name__)
        self.config = config
        self.crawler_executor = CrawlerExecutor(config)
        self._setup_routes()

    def _setup_routes(self) -> None:
        # API 라우트 설정
        self.app.route('/crawl/<crawler_name>')(self.run_crawler)
        self.app.route('/healthcheck')(self.healthcheck)
        self.app.route('/status')(self.get_status)
        
    def require_api_key(self, f):
        """API 키 검증 데코레이터"""
        @wraps(f)
        def decorated(*args, **kwargs):
            api_key = request.headers.get('X-API-Key')
            if not api_key or api_key != self.config.API_KEY:
                return jsonify({"error": "Invalid API key"}), 401
            return f(*args, **kwargs)
        return decorated    
    
    def run_crawler(self, crawler_name: str) -> Response:
        # 크롤러 실행 API 엔드 포인트
        try:
            start_time = datetime.now()
            result = self.crawler_executor.execute_crawler(crawler_name)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            return jsonify({
                "status": "success",
                "crawler": crawler_name,
                "result": result,
                "metadata": {
                    "start_time": start_time.isoformat(),
                    "end_time": end_time.isoformat(),
                    "duration_seconds": duration,
                    "items_count": len(result.get('jobs', [])) if result.get('jobs') else 0
                }
            })
        except ValueError as e:
            return jsonify({
                "status": "error", 
                "message": str(e),
                "crawler": crawler_name,
                "timestamp": datetime.now().isoformat()
            }), 400
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e),
                "crawler": crawler_name,
                "timestamp": datetime.now().isoformat()
            }), 500

    def healthcheck(self) -> Response:
        # 헬스체크 API 엔드포인트
        return jsonify({"status": "healthy"})

    def get_status(self) -> Response:
        # 서버 상태 API 엔드포인트
        return jsonify({
            "status": "healthy",
            "available_crawlers": ["jobkorea", "saramin"],
            "server_time": datetime.now().isoformat(),
            "environment": os.environ.get('FLASK_ENV', 'production')
        })      
        
    def run(self, host: str = '0.0.0.0', port: int = 8000, debug: bool = False) -> None:
        # 서버 실행
        self.app.run(host=host, port=port, debug=debug)

class CLI:
    # CLI 인터페이스 클래스 
    def __init__(self, config: Config):
        self.config = config
        self.crawler_executor = CrawlerExecutor(config)
    
    def run(self) -> None:
        # 명령줄 인자 처리
        if len(sys.argv) < 2:
            print("사용법: python main.py [jobkorea|saramin|all]")
            return
            
        crawler_name = sys.argv[1].lower()
        
        try: 
            if crawler_name == 'all':
                for name in ['jobkorea', 'saramin']:
                    print(f"\n=== {name} 크롤링 시작 ===")
                    result = self.crawler_executor.execute_crawler(name)
                    print(f"크롤링 완료: {result}")
            else:
                result = self.crawler_executor.execute_crawler(crawler_name)
                print(f"크롤링 완료: {result}")
        except Exception as e:
            print(f"에러 발생: {str(e)}")
            sys.exit(1)
            
def main():
    # 메인 엔트리포인트
    config = Config()
    
    if len(sys.argv) > 1 and sys.argv[1] in ['--server', '-s']:
        # 서버 모드로 실행
        server = APIServer(config)
        port = int(os.environ.get('PORT', 8000))
        debug = os.environ.get('FLASK_ENV') == 'development'
        server.run(port=port, debug=debug)
    else:
        # CLI 모드로 실행
        cli = CLI(config)
        cli.run()
        
if __name__ == "__main__":
    main()