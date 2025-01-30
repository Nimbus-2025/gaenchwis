import boto3
import json
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
        client = boto3.client("sagemaker-runtime")
        response = client.invoke_endpoint(
            EndpointName="gaenchwis-sagemaker-recommendation",
            ContentType="application/json",
            Body=json.dumps({
                "logic_type": "UserRecommendation",
                "payload": user_id
            })
        )
        data=json.loads(response['Body'].read().decode("utf-8"))
        print(data)
        return {
            'statusCode': 200,
            'headers': header,
            'body': json.dumps({
                "message":'Recommendation Loaded',
                "data":data
            })
        }
    except ClientError as e:
        print(f"Error fetching data: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'headers': header,
            'body': json.dumps({"message":f"Error fetching data: {e.response['Error']['Message']}"})
        }