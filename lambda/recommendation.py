import boto3
import json
import requests
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')

def recommendation(event, context):
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
        response=requests.post(
            "https://runtime.sagemaker.ap-northeast-2.amazonaws.com/endpoints/gaenchwis-sagemaker-recommendation/invocations",
            data=json.dumps({
                "logic_type": "UserRecommendation",
                "payload": user_id
            })
        )
        print(response)
        return {
            'statusCode': 200,
            'headers': header,
            'body': json.dumps({
                "message":'Recommendation Loaded',
                "data":response
            })
        }
    except ClientError as e:
        print(f"Error fetching data: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'headers': header,
            'body': json.dumps({"message":f"Error fetching data: {e.response['Error']['Message']}"})
        }