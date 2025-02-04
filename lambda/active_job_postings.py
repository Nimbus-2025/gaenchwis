import boto3
from datetime import date, datetime

dynamodb = boto3.resource('dynamodb')

def active_job_postings(event, context):
    table = dynamodb.Table("job_postings")

    today = date.today()

    items = []
    last_evaluated_key = None
    while True:
        scan_kwargs = {}
        if last_evaluated_key:
            scan_kwargs['ExclusiveStartKey'] = last_evaluated_key

        response = table.scan(**scan_kwargs)
        items.extend(response.get('Items', []))

        last_evaluated_key = response.get('LastEvaluatedKey')
        if not last_evaluated_key:
            break

    for item in items:
        expiration_date = item.get('deadline')
        if expiration_date != "채용시":
            month, day = map(int, expiration_date.split('(')[0].split('.'))
            item_date = date(today.year, month, day)

            if item_date < today:
                table.update_item(
                    Key={
                        'PK': item['PK'],
                        'SK': item['SK']
                    },
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
