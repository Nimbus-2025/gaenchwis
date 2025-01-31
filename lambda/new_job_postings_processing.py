import boto3
import json
import requests

dynamodb = boto3.client('dynamodb')

TABLE_NAME = 'job_postings'

def new_job_postings_processing(event, context):
    print(event)
    try:
        for record in event['Records']:
            if record['eventName'] == 'MODIFY':
                new_image = record['dynamodb']['NewImage']
                pk = new_image['PK']['S']
                sk = new_image['SK']['S']
                if new_image.get('recommend_vector_a'):
                    print("Exists Records")
                    break
                
                print(f"Processing new item with PK: {pk}, SK: {sk}")
                clean_data = clean_dynamodb_image(new_image)
                print(clean_data)
                client = boto3.client("sagemaker-runtime")
                response = client.invoke_endpoint(
                    EndpointName="gaenchwis-recommendation",
                    ContentType="application/json",
                    Body=json.dumps({
                        "logic_type": "NewJobPostingTrain",
                        "payload": clean_data
                    })
                )
                data=json.loads(response['Body'].read().decode("utf-8"))
                print(data)
                recommend_vector_a = float(data[0])
                recommend_vector_b = float(data[1])
                recommend_vector_c = float(data[2])
                recommend_vector_d = float(data[3])
                
                update_dynamodb_item(pk, sk, recommend_vector_a, recommend_vector_b, recommend_vector_c, recommend_vector_d)
                
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

def clean_dynamodb_image(dynamodb_image):
    def clean_value(value):
        if isinstance(value, dict):
            key, val = next(iter(value.items()))
            if key == "M":
                return {k: clean_value(v) for k, v in val.items()}
            elif key == "L":
                return [clean_value(v) for v in val]
            else:
                return val
        return value

    return {key: clean_value(value) for key, value in dynamodb_image.items()}


def update_dynamodb_item(pk, sk, value1, value2, value3, value4):
    try:
        response = dynamodb.update_item(
            TableName=TABLE_NAME,
            Key={
                'PK': {'S': pk},
                'SK': {'S': sk}
            },
            UpdateExpression="SET recommend_vector_a = :val1, recommend_vector_b = :val2, recommend_vector_c = :val3, recommend_vector_d = :val4",
            ExpressionAttributeValues={
                ':val1': {'S': str(value1)},
                ':val2': {'S': str(value2)},
                ':val3': {'S': str(value3)},
                ':val4': {'S': str(value4)}
            }
        )
        print(f"Item with PK: {pk}, SK: {sk} updated successfully: {response}")
    except Exception as e:
        print(f"Error updating item with PK: {pk}, SK: {sk}: {e}")
