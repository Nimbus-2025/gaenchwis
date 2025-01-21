import boto3
import json
import requests
from datetime import datetime
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')

def post_applies(event, context):
    print(f"Event received: {event}")

    header = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, access_token, id_token, user_id, post_id, applies"
    }

    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': header
        }

    head = event["headers"]
    body = json.loads(event['body'])

    post_id = head['post_id']
    user_id = head['user_id']
    title = body.get('title',None)
    content = body.get('content',None)
    post_name = body['post_name']
    deadline_date = body['deadline_date']
    time = datetime.utcnow().isoformat()

    try:
        TABLE_NAME = "job_postings"
        table = dynamodb.Table(TABLE_NAME)
        get_post = table.query(
            IndexName="RecIdx",
            KeyConditionExpression="rec_idx = :rec_idx",
            ExpressionAttributeValues={
                ":rec_idx": post_id
            }
        )

        TABLE_NAME = "applies"
        table = dynamodb.Table(TABLE_NAME)
        applies = {
            'PK': "USER#"+user_id,
            'SK': "APPLY#"+get_post["Items"][0].get("post_id"),
            'post_name': post_name,
            'deadline_date': deadline_date,
            'post_id':get_post["Items"][0].get("post_id"),
            'user_id':user_id,
            'post_name':get_post["Items"][0].get("post_name"),
            'apply_date': time,
            'created_at': time,
            'updated_at': time,
            'GSI1PK':"POST#"+get_post["Items"][0].get("post_id"),
            'GSI1SK':"abc"
        }
        table.put_item(Item=applies)
        if title:
            requests.post(
                "https://gaenchwis.click/chrome_extension/essay_save",
                headers={
                    "Content-Type": "application/json",
                    "user_id":user_id,
                    "post_id":post_id,
                },
                data=json.dumps({
                "title":title,
                "content":content
                })
            )
        response=requests.get(
            "https://gaenchwis.click/chrome_extension/post_load",
            headers={
                "Content-Type": "application/json",
                "user_id":user_id,
                "post_id":post_id,
            }
        )
        print(response.json())
        return {
                'statusCode': 200,
                'headers': header,
                'body': json.dumps({
                    "message": "Job Apply add successfully",
                    "data":response.json()
                })
            }
    except ClientError as e:
        return {
            'statusCode': 500,
            'headers': header,
            'body': json.dumps({"error": "Failed to update item", "details": e.response["Error"]["Message"]})
        }