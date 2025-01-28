from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)
CORS(app)  # Flask 애플리케이션 인스턴스 생성

def get_all_jobs():
    try:
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
        table = dynamodb.Table('job_postings')
        
        # 기본 job 정보 가져오기
        response = table.scan(
            ProjectionExpression='PK, SK, post_id, company_name, post_name, post_url'
        )
        items = response.get('Items', [])
        
        # 각 job에 대한 태그 정보 추가
        for item in items:
            # job_tags 테이블에서 태그 정보 가져오기
            job_tags_table = dynamodb.Table('job_tags')
            job_tags_response = job_tags_table.query(
                KeyConditionExpression='PK = :PK',
                ExpressionAttributeValues={
                    ':PK': item['SK']
                }
            )
            
            # 태그 이름 가져오기
            job_tags = job_tags_response.get('Items', [])
            tag_names = get_tag_names(job_tags, dynamodb)
            
            # 결과에 태그 추가
            item['tags'] = tag_names
            
        return items
    except ClientError as e:
        print(f"Error fetching jobs: {str(e)}")
        return []
def get_tag_names(job_tags, dynamodb):
    try:
        tags_table = dynamodb.Table('tags')
        tag_names = []
        
        for tag in job_tags:
            response = tags_table.query(
                KeyConditionExpression='PK = :PK',
                ExpressionAttributeValues={
                    ':PK': tag['SK']
                }
            )
            tag_names.extend([item['name'] for item in response.get('Items', [])])
            
        return tag_names
    except ClientError as e:
        print(f"Error fetching tags: {str(e)}")
        return []
def get_filtered_jobs(query):
    try:
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
        table = dynamodb.Table('job_postings')
        
        # 전체 데이터를 가져온 후 필터링
        response = table.scan()
        items = response.get('Items', [])
        
        # 검색어로 필터링하고 태그 정보 추가
        filtered_items = []
        for item in items:
            if (query.lower() in item.get('company_name', '').lower() or 
                query.lower() in item.get('post_name', '').lower()):
                
                # job_tags 테이블에서 태그 정보 가져오기
                job_tags_table = dynamodb.Table('job_tags')
                job_tags_response = job_tags_table.query(
                    KeyConditionExpression='PK = :PK',
                    ExpressionAttributeValues={
                        ':PK': item['SK']  # 또는 적절한 job_id 필드
                    }
                )
                
                # 태그 이름 가져오기
                job_tags = job_tags_response.get('Items', [])
                tag_names = get_tag_names(job_tags, dynamodb)
                
                # 결과에 태그 추가
                item['tags'] = tag_names
                filtered_items.append(item)
        
        return filtered_items

    except ClientError as e:
        print(f"Error in get_filtered_jobs: {str(e)}")
        return []


@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    try:
        query = request.args.get('query', '')  # URL에서 검색어 파라미터 가져오기
        
        if query:  # 검색어가 있는 경우
            jobs = get_filtered_jobs(query)
        else:  # 검색어가 없는 경우
            jobs = get_all_jobs()
            
        return jsonify(jobs)
    except Exception as e:
        print(f"Error in get_jobs: {str(e)}")
        return jsonify({"error": str(e)}), 500



@app.route('/api/tags/education', methods=['GET'])
def get_education_tags():
    try:
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
        table = dynamodb.Table('tags')
        
        response = table.scan(
            FilterExpression='SK = :sk_value',
            ExpressionAttributeValues={
                ':sk_value': 'TAG#education'
            },
             ExpressionAttributeNames={
        '#n': 'name'  # name을 #n으로 별칭 지정
    },
    ProjectionExpression='#n'  # 별칭 사용
)
        
        tag_names = [item['name'] for item in response.get('Items', [])]
        print("Retrieved education tags:", tag_names)  # 디버깅용 로그
        return jsonify(tag_names)
        
    except ClientError as e:
        print(f"Error fetching education tags: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)