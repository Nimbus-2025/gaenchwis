import boto3
import json
from datetime import datetime
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = "users"
table = dynamodb.Table(TABLE_NAME)

def user_load(event, context):
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

    try:
        head = event["headers"]
        body = json.loads(event['body'])

        userid = head.get('user_id')
        user_name = body.get('user_name')
        user_email = body.get('user_email')
        user_phone = body.get('user_phone')

        if not userid or not (user_name or user_email or user_phone):
            return {
                'statusCode': 400,
                'headers': header,
                'body': json.dumps({"error": "Missing required fields: 'userid' and at least one of 'user_name', 'user_email', or 'user_phone'"})
            }
    except (json.JSONDecodeError, KeyError) as e:
        return {
            'statusCode': 400,
            'headers': header,
            'body': json.dumps({"error": "Invalid request body", "details": str(e)})
        }

    update_expression = "SET "
    expression_attribute_values = {}
    expression_attribute_names = {}

    update_expression += "#user_name = :user_name, "
    expression_attribute_names["#user_name"] = "user_name"
    expression_attribute_values[":user_name"] = user_name

    update_expression += "#user_email = :user_email, "
    expression_attribute_names["#user_email"] = "user_email"
    expression_attribute_values[":user_email"] = user_email

    update_expression += "#user_phone = :user_phone, "
    expression_attribute_names["#user_phone"] = "user_phone"
    expression_attribute_values[":user_phone"] = user_phone

    update_expression += "#updated_at = :updated_at, "
    expression_attribute_names["#updated_at"] = "updated_at"
    expression_attribute_values[":updated_at"] = datetime.utcnow().isoformat()

    update_expression = update_expression.rstrip(", ")

    try:
        table.update_item(
            Key={"PK": userid},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW",
        )
        return {
            'statusCode': 200,
            'headers': header,
            'body': json.dumps({
                "message": "Item updated successfully"
            })
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'headers': header,
            'body': json.dumps({"error": "Failed to update item", "details": e.response["Error"]["Message"]})
        }