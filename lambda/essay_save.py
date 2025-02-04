import boto3
import json
import uuid
from datetime import datetime
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')

def essay_save(event, context):
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
    body = json.loads(event['body'])

    post_id = head.get('post_id', None)
    user_id = head['user_id']
    title = body['title']
    content = body['content']
    time = datetime.utcnow().isoformat()
    try:
        if not user_id:
            return {
                'statusCode': 400,
                'headers': header,
                'body': json.dumps({"error": "Missing required fields"})
            }
    except (json.JSONDecodeError, KeyError) as e:
        return {
            'statusCode': 400,
            'headers': header,
            'body': json.dumps({"error": "Invalid request body", "details": str(e)})
        }
    
    essay_list=[]
    essay_post_list=[]

    length=len(title)
    for i in range(length):
        essay_id = str(uuid.uuid4())
        essay = {
            'PK': "USER#"+user_id,
            'SK': "ESSAY#"+essay_id,
            'essay_ask': title[i],
            'essay_content': content[i],
            'created_at': time,
            'updated_at': time,
            'user_id':user_id,
            'essay_id':essay_id,
            'GSI1PK':"ESSAY#ALL",
            'GSI1SK': time
        }
        essay_list.append(essay)
        if post_id:
            TABLE_NAME = "job_postings"
            table = dynamodb.Table(TABLE_NAME)
            response = table.query(
                IndexName="RecIdx",
                KeyConditionExpression="rec_idx = :rec_idx",
                ExpressionAttributeValues={
                    ":rec_idx": post_id
                }
            )
            essay_post = {
                'PK': "ESSAY#"+essay_id,
                'SK': response["Items"][0].get("SK"),
                'created_at': time,
                'user_id':user_id,
                'post_id':response["Items"][0].get("post_id"),
                'GSI1PK':response["Items"][0].get("SK"),
                'GSI1SK':"ESSAY#"+essay_id
            }
            essay_post_list.append(essay_post)

    try:
        length=len(essay_list)
        essay_table = dynamodb.Table("essays")
        essay_post_table = dynamodb.Table("essay_job_postings")
        for i in range(length):
            essay_table.put_item(Item=essay_list[i])
            print(f"Essay saved to DynamoDB: {essay_list[i]}")
            if post_id:
                essay_post_table.put_item(Item=essay_post_list[i])
                print(f"Essay Post saved to DynamoDB: {essay_post_list[i]}")
            
        return {
                'statusCode': 200,
                'headers': header,
                'body': json.dumps({
                    "message": "Essay add successfully",
                    "time": time
                })
            }
    except ClientError as e:
        return {
            'statusCode': 500,
            'headers': header,
            'body': json.dumps({"error": "Failed to update item", "details": e.response["Error"]["Message"]})
        }