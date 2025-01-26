from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os 

load_dotenv()


app = Flask(__name__)
CORS(app)

# aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
# aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')

dynamodb = boto3.resource(
    'dynamodb',
    region_name=aws_region,
    # aws_access_key_id=aws_access_key_id,
    # aws_secret_access_key=aws_secret_access_key
)

def get_tag_names(job_tags, dynamodb):
    try:
        tags_table = dynamodb.Table('tags')
        # 카테고리별로 태그를 저장할 딕셔너리
        categorized_tags = {
            'TAG#location': [],    # 지역
            'TAG#position': [],    # 직무
            'TAG#job_type': [],    # 고용형태
            'TAG#position': [],
            'TAG#skill': [],     # 경력
            'TAG#education': []
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
                    categorized_tags[tag_category].append(item['tag_name'])
        
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





def get_filtered_jobs(query, page, per_page, selected_categories=None):
    try:
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
        job_postings_table = dynamodb.Table('job_postings')
        job_tags_table = dynamodb.Table('job_tags')
        tags_table = dynamodb.Table('tags')

        # Step 1: 텍스트 검색 (공고 제목 및 기업명)
        filter_expressions = []
        expression_attribute_values = {}

        if query:
            filter_expressions.append('(contains(#company, :query) or contains(#post, :query))')
            expression_attribute_values[':query'] = query.lower()

            filter_expression = ' and '.join(filter_expressions) if filter_expressions else None

            response = job_postings_table.scan(
                FilterExpression=filter_expression,
                ExpressionAttributeNames={
                    '#company': 'company_name',
                    '#post': 'post_name'
                },
                ExpressionAttributeValues=expression_attribute_values if filter_expressions else None
            )

            items = response.get('Items', [])
            matching_job_ids = set(item['SK'] for item in items)

            # 태그명 검색 추가
            tag_response = tags_table.scan(
                FilterExpression='contains(tag_name, :query)',
                ExpressionAttributeValues={
                    ':query': query.lower()
                }
            )
            
            print(f"Tag response for query '{query}': {tag_response['Items']}")

            for tag_item in tag_response['Items']:
                tag_pk = tag_item['PK']
                # print(f"Found tag PK: {tag_pk} for query: {query}")

                # 해당 태그에 연결된 job_id를 찾기
                job_tags_response = job_tags_table.query(
                    IndexName="JobTagInverseIndex",
                    KeyConditionExpression='GSI1PK = :gsi1pk',
                    ExpressionAttributeValues={
                        ':gsi1pk': tag_pk
                    }
                )
                print(f"Job tags response for tag PK '{tag_pk}': {job_tags_response['Items']}")

                # 태그로 찾은 job_id 출력
                for job_tag_item in job_tags_response['Items']:
                    job_id = job_tag_item['PK']
                    print(f"Found job_id: {job_id} for tag PK: {tag_pk}")
                    matching_job_ids.add(job_id)

        # Step 2: 선택한 카테고리 필터링 적용
        if selected_categories:
            filtered_job_ids = set(matching_job_ids)

            for category, values in selected_categories.items():
                category_sk = {
                    '직무': 'TAG#position',
                    '학력': 'TAG#education',
                    '지역': 'TAG#location',
                    '경력': 'TAG#position'
                }.get(category)

                if not category_sk:
                    continue

                category_filtered_job_ids = set()

                if '신입' in values:
                    values.append('경력무관')

                for value in values:
                    tag_response = tags_table.scan(
                        FilterExpression='SK = :sk AND contains(tag_name, :value)',
                        ExpressionAttributeValues={
                            ':sk': category_sk,
                            ':value': value
                        }
                    )

                    for tag_item in tag_response['Items']:
                        tag_pk = tag_item['PK']
                        

                        # 해당 태그에 연결된 job_id를 찾기
                        job_tags_response = job_tags_table.query(
                            IndexName="JobTagInverseIndex",
                            KeyConditionExpression='GSI1PK = :gsi1pk',
                            ExpressionAttributeValues={
                                ':gsi1pk': tag_pk
                            }
                        )

                        category_filtered_job_ids.update(
                            job_tag_item['PK'] for job_tag_item in job_tags_response['Items']
                        )

                # 각 카테고리의 필터링 결과를 교차
                filtered_job_ids.intersection_update(category_filtered_job_ids)
        else:
            # 선택된 카테고리가 없을 때 모든 job_id를 포함
            filtered_job_ids = matching_job_ids
            print(f"Filtered job IDs (no category selected): {filtered_job_ids}")
            print(f"Total items: {len(items)}")
        
        # Step 3: 최종 결과 페이징 처리 
        items = job_postings_table.scan().get('Items', [])
        final_items = [item for item in items if item['SK'] in filtered_job_ids]

        print("Final items after filtering:")
        for item in final_items:    
            print(item)  # 각 item의 전체 내용을 출력

        total_items = len(final_items)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_items = final_items[start_idx:end_idx]

        for item in paginated_items:
            job_tags_response = job_tags_table.query(
                KeyConditionExpression='PK = :job_id',
                ExpressionAttributeValues={
                    ':job_id': item['SK']
                }
            )
            job_tags = job_tags_response.get('Items', [])
            item['tags'] = get_tag_names(job_tags, dynamodb)
            print(f"Tags for job ID {item['SK']}: {item['tags']}")

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
        
        # 카테고리 선택값들을 딕셔너리로 받기
        selected_categories = {
            '직무': request.args.getlist('직무'),
            '학력': request.args.getlist('학력'),
            '지역': request.args.getlist('지역'),
            '경력': request.args.getlist('경력')
        }
        
        # 선택된 값이 있는 카테고리만 필터링에 사용
        selected_categories = {k: v for k, v in selected_categories.items() if v}
        
        if query or selected_categories:
            result = get_filtered_jobs(query, page, per_page, selected_categories)
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
        return jsonify({"error": str(e)}), 50

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
                '#n': 'tag_name'
            },
            ProjectionExpression='#n'
        )
        
        tag_names = [item['tag_name'] for item in response.get('Items', [])]
        return jsonify(tag_names)
        
    except ClientError as e:
        print(f"Error fetching education tags: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({
        'message': "Clear"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8003)  # host='0.0.0.0' 추가