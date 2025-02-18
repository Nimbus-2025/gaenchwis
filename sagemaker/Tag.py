import boto3
import json
import re

def get_job_posting_tag(job_postings_sk):
    dynamodb = boto3.resource('dynamodb')
    job_tags_table = dynamodb.Table("job_tags")

    job_tags = job_tags_table.query(
        KeyConditionExpression="PK = :pk",
        ExpressionAttributeValues={
            ":pk": job_postings_sk
        }
    )

    tags_name=[]

    for job_tag in job_tags["Items"]:
        tags_table = dynamodb.Table("tags")
        tags = tags_table.query(
            KeyConditionExpression="PK = :pk",
            ExpressionAttributeValues={
                ":pk": job_tag["SK"]
            }
        )
        tags_name.append(tags["Items"][0]["tag_name"])
    
    return tags_name

def tags_json_init():
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table("tags")
    response = table.scan()
    data = response['Items']


    tags = {
        'skill_num': 0,
        'location_num': 0,
        'education_num': 0,
        'position_num': 0,
        'skill': [None],
        'location': [None],
        'education': [None],
        'position': [None]
    }
    for i in range(20):
        tags["position"].append(i+1)

    tags['position'].extend([
        "신입",
        "정규직",
        "인턴직",
        "프리랜서",
        "계약직",
        "파견직",
        "위촉직",
        "아르바이트"
    ])

    for item in data:
        category=item.get('tag_category')
        if category!="position":
            tags[category].append(item.get('tag_name'))
    
    tags["skill_num"]=len(tags["skill"])
    tags["location_num"]=len(tags["location"])
    tags["education_num"]=len(tags["education"])
    tags["position_num"]=len(tags["position"])

    with open("tags.json", 'w', encoding="utf-8") as json_file:
        json.dump(tags, json_file, indent=2, ensure_ascii=False)

    s3 = boto3.client('s3')
    bucket_name = "gaenchwis-sagemaker"

    s3.upload_file("tags.json", bucket_name, "tags.json")

    return tags

def get_tags_json():
    s3 = boto3.client('s3')
    bucket_name = "gaenchwis-sagemaker"

    def s3_file_exists(bucket, key):
        try:
            s3.head_object(Bucket=bucket, Key=key)
            return True
        except s3.exceptions.ClientError:
            return False
    
    if s3_file_exists(bucket_name, "tags.json"):
        s3.download_file(bucket_name, "tags.json", "tags.json")
        try:
            with open("tags.json", 'r', encoding="utf-8") as json_file:
                return json.load(json_file)
        except:
            return tags_json_init()
    else:
        print("Tag Json does not exist.")
        return tags_json_init()

def tags_json_update(new_tags):
    tags = get_tags_json()
    for category in new_tags:
        for new_tag in new_tags[category]:
            if new_tag not in tags[category]:
                tags[category].append(new_tag)
    
    tags["skill_num"]=len(tags["skill"])
    tags["location_num"]=len(tags["location"])
    tags["education_num"]=len(tags["education"])
    tags["position_num"]=len(tags["position"])

    with open("tags.json", 'w', encoding="utf-8") as json_file:
        json.dump(tags, json_file, indent=2, ensure_ascii=False)

    s3 = boto3.client('s3')
    bucket_name = "gaenchwis-sagemaker"

    s3.upload_file("tags.json", bucket_name, "tags.json")

    return tags
    
def new_tag_add(category, tag_name, tags_json, tags_group):
    if tag_name not in tags_json[category]:
        new_tags = {
            category: [tag_name]
        }
        tags_json = tags_json_update(new_tags)
        with open("tags.json", 'w', encoding="utf-8") as json_file:
            json.dump(tags_json, json_file, indent=2, ensure_ascii=False)

        s3 = boto3.client('s3')
        bucket_name = "gaenchwis-sagemaker"

        s3.upload_file("tags.json", bucket_name, "tags.json")

    tags_group[category].append(tag_name)

    return tags_json, tags_group

def train_tags_group():
    dynamodb = boto3.resource('dynamodb')
    job_postings_table = dynamodb.Table("job_postings")

    tags_groups = []

    job_postings = []

    last_evaluated_key = None
    while True:
        scan_kwargs = {}
        if last_evaluated_key:
            scan_kwargs['ExclusiveStartKey'] = last_evaluated_key

        response = job_postings_table.scan(**scan_kwargs)
        job_postings.extend(response.get('Items', []))

        last_evaluated_key = response.get('LastEvaluatedKey')
        if not last_evaluated_key:
            break
    print(f"Train : {len(job_postings)}")
    for job_postings_item in job_postings:
        tags_group = MakeTagGroup(job_postings_item)
        tags_groups.append(tags_group)
    
    return tags_groups

def MakeTagGroup(job_postings_item):
    dynamodb = boto3.resource('dynamodb')
    job_tags_table = dynamodb.Table("job_tags")

    job_tags = job_tags_table.query(
        KeyConditionExpression="PK = :pk",
        ExpressionAttributeValues={
            ":pk": job_postings_item["SK"]
        }
    )

    tags_group = {
        'skill': [],
        'location': [],
        'education': [],
        'position': []
    }

    tags_json = get_tags_json()

    for job_tags_item in job_tags["Items"]:
        tags_table = dynamodb.Table("tags")
        tags = tags_table.query(
            KeyConditionExpression="PK = :pk",
            ExpressionAttributeValues={
                ":pk": job_tags_item["SK"]
            }
        )
        tag = tags["Items"][0]
        if tag["tag_category"]=="position":
            position_range = [int(num) for num in re.findall(r"\d+", tag["tag_name"])]
            if "↓" in tag["tag_name"]:
                position_range.insert(0, 1)
            elif "↑" in tag["tag_name"]:
                position_range.append(20)
            elif "경력" in tag["tag_name"]:
                position_range = [1, 20]
            
            if len(position_range) == 2:
                tags_group["position"].extend(range(position_range[0], position_range[1]+1))
            else:
                tags_json, tags_group = new_tag_add(tag["tag_category"], tag["tag_name"], tags_json, tags_group)
        else:
            tags_json, tags_group = new_tag_add(tag["tag_category"], tag["tag_name"], tags_json, tags_group)
    
    for category in tags_group:
        if not tags_group[category]:
            tags_group[category].append(None)

    return tags_group

def MakeUserTagGroup(user_id):
    dynamodb = boto3.resource('dynamodb')
    user_tags_table = dynamodb.Table("user_tags")

    user_tags = user_tags_table.query(
        KeyConditionExpression="PK = :pk",
        ExpressionAttributeValues={
            ":pk": "USER#"+user_id
        }
    )

    tags_group = {
        'skill': [],
        'location': [],
        'education': [],
        'position': []
    }

    for tags in user_tags["Items"]:
        if not tags:
            break
        if tags["tag_category"]=="position":
            position_range = [int(num) for num in re.findall(r"\d+", tags["tag_name"])]
            if len(position_range) == 2 or "년" in tags["tag_name"] or "↑" in tags["tag_name"] or "↓" in tags["tag_name"] or "경력" in tags["tag_name"]:
                tags_group["position"].extend(range(1, 21))
            else:
                tags_group[tags["tag_category"]].append(tags["tag_name"])
        else:
            tags_group[tags["tag_category"]].append(tags["tag_name"])

    for category in tags_group:
        if not tags_group[category]:
            tags_group[category].append(None)
        else:
            if category=="position":
                tags_group["position"]=list(dict.fromkeys(tags_group["position"]))
    
    return tags_group