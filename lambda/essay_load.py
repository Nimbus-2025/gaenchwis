import boto3
import json
from datetime import datetime
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')

def essay_load(event, context):
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

    post_id = head.get('post_id', None)
    user_id = head['user_id']
    applies = bool(head.get('applies', None))

    try:
        TABLE_NAME = "essays"
        table = dynamodb.Table(TABLE_NAME)

        response = table.query(
            KeyConditionExpression="PK = :pk",
            ExpressionAttributeValues={
                ":pk": "USER#"+user_id
            }
        )
        print(response)
        if response["Items"]:
            post=[]
            title=[]
            content=[]
            date=[]

            if applies:
                job_table = dynamodb.Table("job_postings")
                get_job = job_table.query(
                    IndexName="RecIdx",
                    KeyConditionExpression="rec_idx = :rec_idx",
                    ExpressionAttributeValues={
                        ":rec_idx": post_id
                    }
                )
                p_id=get_job["Items"][0].get("post_id")
            else:
                p_id=None
            
            for essays in response["Items"]:
                essay_post=applies_essay(essays["SK"], p_id)
                if (applies and essay_post==p_id) or not applies:
                    date_time=datetime.strptime(essays["updated_at"], '%Y-%m-%dT%H:%M:%S.%f')
                    post.append(get_job["Items"][0].get("post_name") if p_id else load_post(essay_post))
                    title.append(essays["essay_ask"])
                    content.append(essays["essay_content"])
                    date.append(date_time.strftime('%Y-%m-%d %H:%M'))
            return {
                'statusCode': 200,
                'headers': header,
                'body': json.dumps({
                    "message":'Essay Loaded',
                    "post":post,
                    "title": title,
                    "content": content,
                    "date": date
                })
            }
        else:
            print('Essay not found.')
            return {
                'statusCode': 404,
                'headers': header,
                'body': json.dumps({"message":'Essay not found.'})
            }

    except ClientError as e:
        print(f"Error fetching data: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'headers': header,
            'body': json.dumps({"message":f"Error fetching data: {e.response['Error']['Message']}"})
        }
    
def load_post(post_id):
    TABLE_NAME = "job_postings"
    table = dynamodb.Table(TABLE_NAME)
    if not post_id:
        return None
    response = table.query(
        IndexName="JobPostId",
        KeyConditionExpression="post_id = :post_id",
        ExpressionAttributeValues={
            ":post_id": post_id
        }
    )
    return response["Items"][0]["post_name"]

def applies_essay(essay_id, post_id=None):
    TABLE_NAME = "essay_job_postings"
    table = dynamodb.Table(TABLE_NAME)
    if post_id:
        essay_job = table.get_item(Key={
            'PK': essay_id,
            'SK': "JOB#"+post_id
        })
        return essay_job["Item"]["post_id"] if "Item" in essay_job else None
    else:
        essay_job = table.query(
            KeyConditionExpression="PK = :pk",
            ExpressionAttributeValues={
                ":pk": essay_id
            }
        )
        return essay_job["Items"][0]["post_id"] if essay_job["Items"] else None

      