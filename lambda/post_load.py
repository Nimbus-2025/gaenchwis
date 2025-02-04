import boto3
import json
import requests
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')

def post_load(event, context):
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

    post_id = head['post_id']
    user_id = head['user_id']

    try:
        TABLE_NAME = "job_postings"
        table = dynamodb.Table(TABLE_NAME)

        response = table.query(
            IndexName="RecIdx",
            KeyConditionExpression="rec_idx = :rec_idx",
            ExpressionAttributeValues={
                ":rec_idx": post_id
            }
        )

        if response["Items"]:
            applies = check_applies(user_id, response["Items"][0].get("post_id"))

            if applies:
                print("load essay")
                essays = requests.get(
                    "https://gaenchwis.click/chrome_extension/essay_load",
                    headers={
                        "Content-Type": "application/json",
                        "user_id":user_id,
                        "post_id":post_id,
                        "applies":str(applies)
                    }
                )
                essays = essays.json()
                print(essays)
            else:
                essays = None
            return {
                'statusCode': 200,
                'headers': header,
                'body': json.dumps({
                    "message":'Post Loaded',
                    "company_name":response["Items"][0].get("company_name"),
                    "post_name":response["Items"][0].get("post_name"),
                    "post_url":response["Items"][0].get("post_url"),
                    "status":response["Items"][0].get("status"),
                    "deadline":response["Items"][0].get("deadline"),
                    "applies":applies,
                    "essays":essays
                })
            }
        else:
            print('Post not found.')
            return {
                'statusCode': 404,
                'headers': header,
                'body': json.dumps({"message":'Post not found.'})
            }

    except ClientError as e:
        print(f"Error fetching data: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'headers': header,
            'body': json.dumps({"message":f"Error fetching data: {e.response['Error']['Message']}"})
        }

def check_applies(user_id, post_id):
    TABLE_NAME = "applies"
    table = dynamodb.Table(TABLE_NAME)

    user_applies = table.get_item(Key={
        'PK': "USER#"+user_id,
        'SK': "APPLY#"+post_id
    })
    if 'Item' in user_applies:
        return True
    else:
        return False