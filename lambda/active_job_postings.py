import boto3
from datetime import date, datetime

dynamodb = boto3.resource('dynamodb')

def active_job_postings(event, context):
    table = dynamodb.Table("job_postings")

    today = date.today()

    response = table.query(
        IndexName="StatusIndex",
        KeyConditionExpression="GSI1PK = :gsi1pk",
        ExpressionAttributeValues={
            ":gsi1pk": "STATUS#active"
        }
    )
    items = response.get('Items', [])

    for item in items:
        expiration_date = item.get('deadline')
        if expiration_date != "채용시":
            month, day = map(int, expiration_date.split('(')[0].split('.'))
            item_date = date(today.year, month, day)

            if item_date < today:
                table.update_item(
                    Key={'PK': item['PK']},
                    UpdateExpression="""
                        SET #status = :new_status,
                            #gsi1pk = :new_gsi1pk,
                            updated_at = :current_time
                    """,
                    ExpressionAttributeNames={
                        '#status': 'status',
                        '#gsi1pk': 'GSI1PK'
                    },
                    ExpressionAttributeValues={
                        ':new_status': 'inactive',
                        ':new_gsi1pk': 'STATUS#inactive',
                        ':current_time': datetime.utcnow().isoformat()
                    }
                )
