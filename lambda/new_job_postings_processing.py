import boto3
import json

dynamodb = boto3.client('dynamodb')

TABLE_NAME = 'job_postings'

def new_job_postings_processing(event, context):
    try:
        for record in event['Records']:
            if record['eventName'] == 'INSERT':
                new_image = record['dynamodb']['NewImage']
                pk = new_image['PK']['S']
                sk = new_image['SK']['S']
                
                print(f"Processing new item with PK: {pk}, SK: {sk}")
                
                learning_value_1 = "a"
                learning_value_2 = "b"
                learning_value_3 = "c"
                
                update_dynamodb_item(pk, sk, learning_value_1, learning_value_2, learning_value_3)
                
        return {
            'statusCode': 200,
            'body': json.dumps('Stream processed successfully!')
        }
    
    except Exception as e:
        print(f"Error processing stream: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing stream')
        }

def update_dynamodb_item(pk, sk, value1, value2, value3):
    try:
        response = dynamodb.update_item(
            TableName=TABLE_NAME,
            Key={
                'PK': {'S': pk},
                'SK': {'S': sk}
            },
            UpdateExpression="SET learning_value_1 = :val1, learning_value_2 = :val2, learning_value_3 = :val3",
            ExpressionAttributeValues={
                ':val1': {'N': str(value1)},
                ':val2': {'N': str(value2)},
                ':val3': {'N': str(value3)}
            }
        )
        print(f"Item with PK: {pk}, SK: {sk} updated successfully: {response}")
    except Exception as e:
        print(f"Error updating item with PK: {pk}, SK: {sk}: {e}")
