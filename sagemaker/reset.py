import boto3

dynamodb = boto3.resource("dynamodb")
table_name = "job_postings"
table = dynamodb.Table(table_name)

columns_to_remove = ["recommend_vector_a", "recommend_vector_b", "recommend_vector_c", "recommend_vector_d"]


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
    primary_key = {"PK": item["PK"],
                    "SK": item["SK"]
                  }
    update_expression = "REMOVE " + ", ".join(columns_to_remove)

    table.update_item(
        Key=primary_key,
        UpdateExpression=update_expression
    )

print("✅ 테이블 전체 컬럼 삭제 완료")