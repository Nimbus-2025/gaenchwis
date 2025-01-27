import re
from datetime import datetime, timedelta
from typing import Optional
import os
import pandas as pd

# 크롤링 결과 저장 디렉토리 
def create_directory(directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"'{directory}' 디렉토리가 생성되었습니다.")

# 마감일 문자열을 변환 
def parsse_deadline_date(deadline_str: str) -> str:
    WEEKDAY_MAP = {
        0: '월',
        1: '화',
        2: '수',
        3: '목',
        4: '금',
        5: '토',
        6: '일'
    }
    
    try: 
        deadline_str = deadline_str.strip()
        
        # '상시채용' 또는 '채용시' 또는 파싱할 수 없는 경우
        if '상시' in deadline_str or '채용시' in deadline_str or not deadline_str:
            return '채용시'
            
        # 이미 'MM.DD(요일)' 형식인 경우
        pattern = r'(\d{2})\.(\d{2})\(([월화수목금토일])\)'
        if re.match(pattern, deadline_str):
            return deadline_str
            
        # ~01.21(화) 형식인 경우
        pattern = r'~?(\d{2})\.(\d{2})\(([월화수목금토일])\)' 
        match = re.match(pattern, deadline_str)
        if match:
            return f"{match.group(1)}.{match.group(2)}({match.group(3)})"
            
        # D-day 형식인 경우
        if 'D-' in deadline_str:
            days = int(deadline_str.replace('D-', ''))
            target_date = datetime.now() + timedelta(days=days)
            weekday_str = WEEKDAY_MAP[target_date.weekday()]
            return target_date.strftime(f"%m.%d({weekday_str})")
            
        # 그 외 모든 경우
        return '채용시'
            
    except Exception as e:
        print(f"마감일 파싱 중 오류 발생: {str(e)}")
        return '채용시'