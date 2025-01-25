import boto3
import json
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = "users"
table = dynamodb.Table(TABLE_NAME)

def user_load(event, context):
    print(f"Event received: {event}")

    header = {
        "Content-Type": "application/json",
    }

    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': header
        }

    head = event["headers"]

    user_id = head['user_id']

    try:
        if not user_id:
            print('Missing userId in the request.')
            return {
                'statusCode': 400,
                'headers': header,
                'body': json.dumps({"message":'Missing userId in the request.'})
            }
        response = table.get_item(Key={'PK': "USER#"+user_id})
        
        if 'Item' in response:
            return {
                'statusCode': 200,
                'headers': header,
                'body': json.dumps({
                    "message":'User Loaded',
                    "name":response["Item"].get("user_name"),
                    "email":response["Item"].get("user_email"),
                    "phone":response["Item"].get("user_phone")
                })
            }
        else:
            print('User not found.')
            return {
                'statusCode': 404,
                'headers': header,
                'body': json.dumps({"message":'User not found.'})
            }

    except ClientError as e:
        print(f"Error fetching data: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'headers': header,
            'body': json.dumps({"message":f"Error fetching data: {e.response['Error']['Message']}"})
        }
