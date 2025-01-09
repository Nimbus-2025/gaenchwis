import os
import pandas as pd

# 크롤링 결과 저장 디렉토리 
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"'{directory}' 디렉토리가 생성되었습니다.")

# 데이터를 CSV 파일로 저장 
def save_to_csv(data, filename):
    # 모든 필드의 따옴표 제거
    for item in data:
        for key in item:
            if isinstance(item[key], str):
                item[key] = item[key].replace('"', '').replace("'", '')
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"데이터가 {filename}에 저장되었습니다.")