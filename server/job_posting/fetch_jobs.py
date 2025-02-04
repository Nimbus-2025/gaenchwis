from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os 
import logging
load_dotenv()


app = Flask(__name__)
CORS(app, 
     resources={r"/api/*": {
         "origins": ["*"],
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         "allow_headers": ["Content-Type", "user_id", "id_token", "access_token"]
     }})


# aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
# aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')

dynamodb = boto3.resource(
    'dynamodb',
    region_name=aws_region,
    # aws_access_key_id=aws_access_key_id,
    # aws_secret_access_key=aws_secret_access_key
)

# 테이블 초기화 - 별도로 선언
user_tags_table = dynamodb.Table('user_tags')

def get_current_user_id():
    # 요청 헤더에서 user_id 가져오기
    user_id = request.headers.get('user_id')
    if not user_id:
        raise Exception("User ID not found")
    return user_id

# 태그 관련 함수들
class UserTagService:
    @staticmethod
    def update_user_tags(user_id: str, tag_type: str, tags: list):
        try:
            print(f"Updating tags for user {user_id} with tags: {tags}")

            # 1. 기존 태그 모두 삭제
            existing_tags = user_tags_table.query(
                KeyConditionExpression='PK = :pk AND begins_with(SK, :sk)',
                ExpressionAttributeValues={
                    ':pk': f"USER#{user_id}",
                    ':sk': f"{tag_type}#"  # tag_type은 그대로 사용
                }
            ).get('Items', [])

            print(f"Existing tags for user {user_id}: {existing_tags}")

            # 기존 태그 삭제를 먼저 수행
            for tag in existing_tags:
                user_tags_table.delete_item(
                    Key={
                        'PK': tag['PK'],
                        'SK': tag['SK']
                    }
                )

            # 2. 새로운 태그 추가
            now = datetime.utcnow().isoformat()
            for tag in tags:
                print(f"Processing tag: {tag}")
                user_tags_table.put_item(
                    Item={
                        'PK': f"USER#{user_id}",
                        'SK': f"{tag_type}#{tag['tag_name']}",  # tag_type과 tag_name 사용
                        'GSI1PK': f"TAG#{tag_type}",
                        'GSI1SK': f"USER#{user_id}",
                        'tag_name': tag['tag_name'],
                        'tag_type': tag_type,
                        'tag_category': tag_type,
                        'created_at': now,
                        'updated_at': now
                    }
                )

            return True
        except Exception as e:
            logging.error(f"Error updating tags: {str(e)}")
            return False

    @staticmethod
    def get_user_tags(user_id: str, tag_type: str = None):
        try:
            if tag_type:
                response = user_tags_table.query(
                    KeyConditionExpression='PK = :pk AND begins_with(SK, :sk)',
                    ExpressionAttributeValues={
                        ':pk': f"USER#{user_id}",
                        ':sk': f"{tag_type}#"  # tag_type은 그대로 사용
                    }
                )
            else:
                response = user_tags_table.query(
                    KeyConditionExpression='PK = :pk',
                    ExpressionAttributeValues={
                        ':pk': f"USER#{user_id}"
                    }
                )
            return response.get('Items', [])
        except Exception as e:
            logging.error(f"Error getting tags: {str(e)}")
            return []

# API 엔드포인트



@app.route("/api/v1/user/tags/<tag_type>/<user_id>", methods=['PUT'])
def update_tags(tag_type, user_id):
    try:
        request_data = request.get_json()

        print(f"\n=== 태그 업데이트 요청 정보 ===")
        print(f"User ID: {user_id}")
        print(f"Tag Type: {tag_type}")
        print(f"Request Data: {request_data}")
        print(f"Tags to Update: {request_data['tags']}")

        
        
        success = UserTagService.update_user_tags(
            user_id=user_id,
            tag_type=tag_type,
            tags=request_data['tags']
        )
        
        if success:
            updated_tags = UserTagService.get_user_tags(user_id, tag_type)
            return jsonify({
                "message": "태그가 성공적으로 업데이트되었습니다.", 
                "tags": updated_tags
            })
        else:
            return jsonify({"error": "태그 업데이트 실패"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/user/tags/<tag_type>/<user_id>', methods=['GET'])
def get_user_tags(tag_type, user_id):
    try:
        print(f"Received user_id: {user_id}")
        
        if not user_id:
            return jsonify({"error": "User ID not provided"}), 400

        # DynamoDB에서 해당 사용자의 태그 조회
        response = user_tags_table.query(
            KeyConditionExpression='PK = :pk AND begins_with(SK, :sk)',
            ExpressionAttributeValues={
                ':pk': f"USER#{user_id}",
                ':sk': f"{tag_type}#"
            }
        )
        
        print(f"DynamoDB response: {response}")
        
        items = response.get('Items', [])
        print(f"Retrieved tags: {items}")
        
        # 태그 데이터 변환
        formatted_tags = []
        for item in items:
            formatted_tags.append({
                'tag_id': item.get('SK', '').split('#')[1],
                'tag_name': item.get('tag_name', ''),
                'tag_type': tag_type
            })
        
        return jsonify({
            "status": "success",
            "tags": formatted_tags,
            "message": f"{tag_type} 태그 조회 성공"
        })
        
    except Exception as e:
        print(f"태그 조회 중 에러 발생: {str(e)}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "message": f"{tag_type} 태그 조회 실패"
        }), 500
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
            ProjectionExpression='PK, SK, post_id, company_name, post_name, post_url, is_closed, company_id, deadline'
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
                ProjectionExpression='PK, SK, post_id, company_name, post_name, post_url, is_closed, deadline'
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
        print(items)
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

        matching_job_ids = set()
        
        # Step 1: 먼저 카테고리 필터링 수행
        if selected_categories:
            category_job_ids = None
            
            for category, values in selected_categories.items():
                category_sk = {
                    '직무': 'TAG#position',
                    '학력': 'TAG#education',
                    '지역': 'TAG#location',
                    '경력': 'TAG#position'
                }.get(category)

                if not category_sk:
                    continue

                current_category_ids = set()

                if category == '경력' and '신입' in values:
                    values.append('경력무관')

                for value in values:
                    # 해당 카테고리의 태그 찾기
                    tag_response = tags_table.scan(
                        FilterExpression='SK = :sk AND contains(tag_name, :value)',
                        ExpressionAttributeValues={
                            ':sk': category_sk,
                            ':value': value
                        }
                    )

                    for tag_item in tag_response['Items']:
                        tag_pk = tag_item['PK']
                        job_tags_response = job_tags_table.query(
                            IndexName="JobTagInverseIndex",
                            KeyConditionExpression='GSI1PK = :gsi1pk',
                            ExpressionAttributeValues={
                                ':gsi1pk': tag_pk
                            }
                        )
                        current_category_ids.update(
                            job_tag_item['PK'] for job_tag_item in job_tags_response['Items']
                        )

                if category_job_ids is None:
                    category_job_ids = current_category_ids
                else:
                    category_job_ids.intersection_update(current_category_ids)

            matching_job_ids = category_job_ids or set()

        # Step 2: 텍스트 검색 수행
        if query:
            text_search_ids = set()
            
            # 공고 제목 및 기업명 검색
            response = job_postings_table.scan(
                FilterExpression='contains(#company, :query) or contains(#post, :query)',
                ExpressionAttributeNames={
                    '#company': 'company_name',
                    '#post': 'post_name'
                },
                ExpressionAttributeValues={
                    ':query': query.lower()
                }
            )
            text_search_ids.update(item['SK'] for item in response.get('Items', []))

            # 태그명 검색
            tag_response = tags_table.scan(
                FilterExpression='contains(tag_name, :query)',
                ExpressionAttributeValues={
                    ':query': query.lower()
                }
            )

            for tag_item in tag_response['Items']:
                job_tags_response = job_tags_table.query(
                    IndexName="JobTagInverseIndex",
                    KeyConditionExpression='GSI1PK = :gsi1pk',
                    ExpressionAttributeValues={
                        ':gsi1pk': tag_item['PK']
                    }
                )
                text_search_ids.update(
                    job_tag_item['PK'] for job_tag_item in job_tags_response['Items']
                )

            # 카테고리 필터링 결과가 있으면 교차, 없으면 텍스트 검색 결과 사용
            if matching_job_ids:
                matching_job_ids.intersection_update(text_search_ids)
            else:
                matching_job_ids = text_search_ids

        # 최종 결과 가져오기
        items = []
        if matching_job_ids:
            # 모든 job posting을 가져와서 필터링
            scan_response = job_postings_table.scan()
            all_items = scan_response['Items']
            
            # matching_job_ids에 있는 SK를 가진 항목만 필터링
            items = [item for item in all_items if item['SK'] in matching_job_ids]

        # 디버깅을 위한 로깅
        print(f"Matching job IDs: {matching_job_ids}")
        print(f"Number of items found: {len(items)}")

        # 페이징 처리
        total_items = len(items)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_items = items[start_idx:end_idx]

        # 태그 정보 추가
        for item in paginated_items:
            job_tags_response = job_tags_table.query(
                KeyConditionExpression='PK = :job_id',
                ExpressionAttributeValues={
                    ':job_id': item['SK']
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



def organize_position_tags(tags):
    position_categories = {
        "개발자": [],
        "디자이너": [],
        "기획자": [],
        "엔지니어": [],
        "데이터": [],
        "보안": []
    }



    
    for tag in tags:
        # 개발자 관련 태그
        if "개발자" in tag or "프론트엔드" in tag or "백엔드" in tag or "프로그래머" in tag or "개발" in tag:
            position_categories["개발자"].append(tag)
        # 디자이너 관련 태그
        elif "디자이너" in tag or "디자인" in tag:
            position_categories["디자이너"].append(tag)
        # 기획자 관련 태그
        elif "기획" in tag or "매니저" in tag or "PM" in tag:
            position_categories["기획자"].append(tag)
        elif "엔지니어" in tag or "SE" in tag:
            position_categories["엔지니어"].append(tag)
        elif "데이터" in tag or "인공지능" in tag or "사이언티스트" in tag:
            position_categories["데이터"].append(tag)
        elif "보안" in tag or "정보보호" in tag:
            position_categories["보안"].append(tag)
    
    return position_categories


def organize_skill_tags(tags):
    skill_categories = {
        "개발": [],
        "디자인": [],
        "데이터": [],
        "서버/네트워크": [],
        "일반": []
    }
    
    for tag in tags:
        # 개발 관련 스킬
        if "java" in tag.lower() or "python" in tag.lower() or "javascript" in tag.lower() or "react" in tag.lower() or \
           "node" in tag.lower() or "spring" in tag.lower() or "mysql" in tag.lower() or "mongodb" in tag.lower() or \
           "php" in tag.lower() or "html" in tag.lower() or "css" in tag.lower() or "aws" in tag.lower() or \
           "docker" in tag.lower() or "kubernetes" in tag.lower() or "git" in tag.lower() or "c++" in tag.lower() or \
           "파이썬" in tag.lower():
            skill_categories["개발"].append(tag)
            
        # 디자인 관련 스킬
        elif "figma" in tag.lower() or "adobe" in tag.lower() or "photoshop" in tag.lower() or \
             "illustrator" in tag.lower() or "ui" in tag.lower() or "ux" in tag.lower() or \
             "웹디자인" in tag.lower() or "sketch" in tag.lower() or "xd" in tag.lower() or \
             "premiere" in tag.lower() or "after effects" in tag.lower() or "어도비" in tag.lower() or \
             "포토샵" in tag.lower():
            skill_categories["디자인"].append(tag)
            
        # 데이터 관련 스킬
        elif "sql" in tag.lower() or "python" in tag.lower() or \
             "tableau" in tag.lower() or "power bi" in tag.lower() or "데이터" in tag.lower() or \
             "머신러닝" in tag.lower() or "통계" in tag.lower() or "분석" in tag.lower() or \
             "빅데이터" in tag.lower() or "hadoop" in tag.lower() or "spark" in tag.lower():
            skill_categories["데이터"].append(tag)
            
        # 서버/네트워크 관련 스킬
        elif "linux" in tag.lower() or "ubuntu" in tag.lower() or "centos" in tag.lower() or \
             "docker" in tag.lower() or "kubernetes" in tag.lower() or "aws" in tag.lower() or \
             "azure" in tag.lower() or "네트워크" in tag.lower() or "무선" in tag.lower() or \
             "유선" in tag.lower() or "서버" in tag.lower() or "클라우드" in tag.lower() or \
             "devops" in tag.lower() or "ci/cd" in tag.lower() or "jenkins" in tag.lower() or \
             "apache" in tag.lower() or "nginx" in tag.lower() or "보안" in tag.lower() or \
             "방화벽" in tag.lower() or "시스템관리" in tag.lower() or "인프라" in tag.lower() or \
             "vmware" in tag.lower() or "가상화" in tag.lower():
            skill_categories["서버/네트워크"].append(tag)
            
        # 일반 스킬
        elif "office" in tag.lower() or "excel" in tag.lower() or "powerpoint" in tag.lower() or \
             "word" in tag.lower() or "문서" in tag.lower() or "한글" in tag.lower() or \
             "기획" in tag.lower() or "보고서" in tag.lower() or "커뮤니케이션" in tag.lower():
            skill_categories["일반"].append(tag)
    
    return skill_categories

    

def organize_location_tags(tags):
    organized = {
        "서울": [],
        "경기": [],
        "인천": []
    }
    
    for tag in tags:
        if tag.startswith("서울"):
            organized["서울"].append(tag)
        elif tag.startswith("경기"):
            organized["경기"].append(tag)
        elif tag.startswith("인천"):
            organized["인천"].append(tag)
    
    return organized

@app.route('/api/v1/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    try:
        query = request.args.get('query', '')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # 카테고리 파라미터 파싱
        categories = {}
        for key in ['경력', '직무', '학력', '지역']:
            value = request.args.get(f'categories[{key}]')
            if value:
                categories[key] = [value]
        
        print(f"Query: {query}")
        print(f"Categories: {categories}")
        
        if query or categories:
            result = get_filtered_jobs(query, page, per_page, categories)
        else:
            result = get_all_jobs(page, per_page)
            
        print(f"Result: {result}")
        
        return jsonify({
            'items': result['items'],
            'total_items': result['total_items'],
            'total_pages': result['total_pages'],
            'current_page': page
        })
    except Exception as e:
        print(f"Error in get_jobs: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/tags/<tag_type>', methods=['GET'])
def get_tags(tag_type):
    try:
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
        table = dynamodb.Table('tags')
        
        tag_types = {
            'education': 'TAG#education',
            'location': 'TAG#location',
            'position': 'TAG#skill',
            'skill': 'TAG#skill'
        }
        
        if tag_type not in tag_types:
            return jsonify({"error": "Invalid tag type"}), 400
            
        response = table.scan(
            FilterExpression='SK = :sk_value',
            ExpressionAttributeValues={
                ':sk_value': tag_types[tag_type]
            },
            ExpressionAttributeNames={
                '#n': 'tag_name'
            },
            ProjectionExpression='#n'
        )
        
        tag_names = [item['tag_name'] for item in response.get('Items', [])]
        print(f"Retrieved {tag_type} tags:", tag_names)  # 디버깅용

        if tag_type == 'position':
            return jsonify(organize_position_tags(tag_names))
        elif tag_type == 'skill':
            return jsonify(organize_skill_tags(tag_names))
        elif tag_type == 'location':
            return jsonify(organize_location_tags(tag_names))
        else:
            return jsonify(tag_names)
        
    except Exception as e:
        print(f"Error in get_tags: {str(e)}")  # 에러 로깅
        return jsonify({"error": str(e)}), 500


@app.route('/*', methods=['OPTIONS'])
def preflight():
    return jsonify({"status": "healthy"}), 200
# 서버 실행

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8003)