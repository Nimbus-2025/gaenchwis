from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os 

load_dotenv()

app = Flask(__name__)
CORS(app)

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')

dynamodb = boto3.resource(
    'dynamodb',
    region_name=aws_region,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

def get_tag_names(job_tags, dynamodb):
    try:
        tags_table = dynamodb.Table('tags')
        # 카테고리별로 태그를 저장할 딕셔너리
        categorized_tags = {
            'TAG#location': [],    # 지역
            'TAG#position': [],    # 직무
            'TAG#job_type': [],    # 고용형태
            'TAG#education': [],   # 학력
            'TAG#skill': [],       # 스킬
            'TAG#career': [],      # 경력
        }
        
        for tag in job_tags:
            response = tags_table.query(
                KeyConditionExpression='PK = :PK',
                ExpressionAttributeValues={
                    ':PK': tag['SK']
                }
            )
            
            # 각 태그를 해당 카테고리에 추가
            for item in response.get('Items', []):
                tag_category = item.get('SK', '')  # 태그의 카테고리(SK) 가져오기
                if tag_category in categorized_tags:
                    categorized_tags[tag_category].append(item['name'])
        
        # 정해진 순서대로 태그들을 합치기
        ordered_tags = []
        for category in categorized_tags.keys():
            ordered_tags.extend(categorized_tags[category])
            
        return ordered_tags
        
    except ClientError as e:
        print(f"Error fetching tags: {str(e)}")
        return []

def get_all_jobs(page, per_page):
    try:
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
        table = dynamodb.Table('job_postings')
        
        # Scan with pagination
        response = table.scan(
            Limit=per_page,
            ProjectionExpression='PK, SK, post_id, company_name, post_name, post_url, is_closed'
        )
        
        items = response.get('Items', [])
        total_items = table.scan(Select='COUNT')['Count']
        
        # Get to the requested page
        for _ in range(page - 1):
            if 'LastEvaluatedKey' not in response:
                break
            response = table.scan(
                Limit=per_page,
                ExclusiveStartKey=response['LastEvaluatedKey'],
                ProjectionExpression='PK, SK, post_id, company_name, post_name, post_url, is_closed'
            )
            items = response.get('Items', [])

        # Add tags only for the current page items
        for item in items:
            job_tags_table = dynamodb.Table('job_tags')
            job_tags_response = job_tags_table.query(
                KeyConditionExpression='PK = :PK',
                ExpressionAttributeValues={
                    ':PK': item['SK']
                }
            )
            job_tags = job_tags_response.get('Items', [])
            item['tags'] = get_tag_names(job_tags, dynamodb)

        return {
            'items': items,
            'total_items': total_items,
            'total_pages': (total_items + per_page - 1) // per_page,
            'has_more': 'LastEvaluatedKey' in response
        }
        
    except ClientError as e:
        print(f"Error fetching jobs: {str(e)}")
        return {'items': [], 'total_items': 0, 'total_pages': 0, 'has_more': False}

def get_filtered_jobs(query, page, per_page):
    try:
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
        table = dynamodb.Table('job_postings')
        
        # Scan with a filter
        response = table.scan(
            FilterExpression='contains(#company, :query) or contains(#post, :query)',
            ExpressionAttributeNames={
                '#company': 'company_name',
                '#post': 'post_name'
            },
            ExpressionAttributeValues={
                ':query': query.lower()
            }
        )
        
        items = response.get('Items', [])
        
        # Calculate pagination
        total_items = len(items)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_items = items[start_idx:end_idx]
        
        # Add tags only for paginated items
        for item in paginated_items:
            job_tags_table = dynamodb.Table('job_tags')
            job_tags_response = job_tags_table.query(
                KeyConditionExpression='PK = :PK',
                ExpressionAttributeValues={
                    ':PK': item['SK']
                }
            )
            job_tags = job_tags_response.get('Items', [])
            item['tags'] = get_tag_names(job_tags, dynamodb)
        
        return {
            'items': paginated_items,
            'total_items': total_items,
            'total_pages': (total_items + per_page - 1) // per_page
        }

    except ClientError as e:
        print(f"Error in get_filtered_jobs: {str(e)}")
        return {'items': [], 'total_items': 0, 'total_pages': 0}

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    try:
        query = request.args.get('query', '')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        if query:
            result = get_filtered_jobs(query, page, per_page)
        else:
            result = get_all_jobs(page, per_page)
        
        return jsonify({
            'items': result['items'],
            'total_items': result['total_items'],
            'total_pages': result['total_pages'],
            'current_page': page
        })
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
                '#n': 'name'
            },
            ProjectionExpression='#n'
        )
        
        tag_names = [item['name'] for item in response.get('Items', [])]
        return jsonify(tag_names)
        
    except ClientError as e:
        print(f"Error fetching education tags: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)