import boto3
import Tag
import Training
import Layer

def NewJobPosting(job_postings_item):
    tags_group=Tag.MakeTagGroup(job_postings_item)
    position_model, location_model, education_model, skill_model = Training.StartTrain([tags_group])

    position_model.eval()
    location_model.eval()
    education_model.eval()
    skill_model.eval()

    result = Layer.Vector(tags_group, position_model, location_model, education_model, skill_model)

    return result.tolist()

def InitJobPosting():
    dynamodb = boto3.resource('dynamodb')
    job_postings_table = dynamodb.Table("job_postings")


    job_postings = job_postings_table.query(
        IndexName="StatusIndex",
        KeyConditionExpression="GSI1PK = :gsi1pk",
        ExpressionAttributeValues={
            ":gsi1pk": "STATUS#active"
        }
    )

    for job_postings_item in job_postings["Items"]:
        if not job_postings_item.get('recommend_vector_a'):
            print(job_postings_item.get('recommend_vector_a'))
            a,b,c,d = NewJobPosting(job_postings_item)
            job_postings_table.update_item(
                Key={
                    'PK': job_postings_item['PK'],
                    'SK': job_postings_item['SK']
                },
                UpdateExpression="""
                    SET #recommend_vector_a = :recommend_vector_a,
                        #recommend_vector_b = :recommend_vector_b,
                        #recommend_vector_c = :recommend_vector_c,
                        #recommend_vector_d = :recommend_vector_d
                """,
                ExpressionAttributeNames={
                    '#recommend_vector_a': 'recommend_vector_a',
                    '#recommend_vector_b': 'recommend_vector_b',
                    '#recommend_vector_c': 'recommend_vector_c',
                    '#recommend_vector_d': 'recommend_vector_d'
                },
                ExpressionAttributeValues={
                    ':recommend_vector_a': str(a),
                    ':recommend_vector_b': str(b),
                    ':recommend_vector_c': str(c),
                    ':recommend_vector_d': str(d)
                }
            )