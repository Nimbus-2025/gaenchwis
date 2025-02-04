import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = "users"
table = dynamodb.Table(TABLE_NAME)

def login(event, context):
    print(f"Event received: {event}")
    
    user_id = event['userName']
    user_attributes = event['request']['userAttributes']
    
    email = user_attributes.get('email', None)
    name = user_attributes.get('name', user_id)
    phone = user_attributes.get('phone_number', None)
    if 'Google' in user_id:
        provider = 'Google'
    elif 'Kakao' in user_id:
        provider = 'Kakao'
    elif 'Naver' in user_id:
        provider = 'Naver'
    else:
        provider = 'Others'
    user_data = {
        'PK': "USER#"+user_id,
        'user_id': user_id,
        'user_sns': provider,
        'user_email': email,
        'user_name': name,
        'user_phone': phone,
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }

    try:
        table.put_item(Item=user_data)
        print(f"User saved to DynamoDB: {user_data}")
    except Exception as e:
        print(f"Error saving user to DynamoDB: {e}")

    return event