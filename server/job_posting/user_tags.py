from flask import Flask, request, jsonify
from typing import List
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key
import logging
from flask_cors import CORS
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
CORS(app)  # CORS 설정

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'ap-northeast-2')  
CORS(app, 
     resources={r"/api/*": {
         "origins": ["http://localhost:3000"],  # 프론트엔드 주소
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization", "User-Id"],
         "supports_credentials": True  # 이 부분이 중요!
     }})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,User-Id')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')  # 이 부분이 중요!
    return response


# DynamoDB 클라이언트 설정
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)
# DynamoDB 설정
dynamodb = boto3.resource('dynamodb')
user_tags_table = dynamodb.Table('user_tags')

# 사용자 ID 가져오기 (실제 인증 로직으로 대체 필요)
def get_current_user_id():
    # 요청 헤더에서 user_id 가져오기
    user_id = request.headers.get('User-Id')
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
@app.route("/api/v1/user/tags/<tag_type>", methods=['PUT'])
def update_tags(tag_type):
    try:
        user_id = get_current_user_id()
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

@app.route('/api/v1/user/tags/<tag_type>', methods=['GET'])
def get_user_location_tags(tag_type):
    try:
        user_id = request.headers.get('User-Id')
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
        
        return jsonify({"tags": items})
        
    except Exception as e:
        print(f"Error fetching user location tags: {str(e)}")
        return jsonify({"error": str(e)}), 500
# 서버 실행
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8005, debug=True)