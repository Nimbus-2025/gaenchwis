import boto3
import json
import re

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
        "위촉직"
    ])

    for item in data:
        category=item.get('tag_category')
        if category!="position":
            tags[category].append(item.get('tag_name'))
    
    tags["skill_num"]=len(tags["skill"])
    tags["location_num"]=len(tags["location"])
    tags["education_num"]=len(tags["education"])
    tags["position_num"]=len(tags["position"])

    with open("tags.json", 'w') as json_file:
        json.dump(tags, json_file, indent=2)
    
    s3 = boto3.client('s3',
        aws_access_key_id="AKIAWX2IF5YDAMM7FH4V",
        aws_secret_access_key="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",
        region_name="ap-northeast-2"
    )
    bucket_name = "gaenchwis-sagemaker"

    s3.upload_file("tags.json", bucket_name, "tags.json")
    
    return tags

def get_tags_json():
    s3 = boto3.client('s3',
        aws_access_key_id="AKIAWX2IF5YDAMM7FH4V",
        aws_secret_access_key="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",
        region_name="ap-northeast-2"
    )
    bucket_name = "gaenchwis-sagemaker"

    def s3_file_exists(bucket, key):
        try:
            s3.head_object(Bucket=bucket, Key=key)
            return True
        except s3.exceptions.ClientError:
            return False
    
    if s3_file_exists(bucket_name, "tags.json"):
        s3.download_file(bucket_name, "tags.json", "tags.json")
        with open("tags.json", 'r') as json_file:
            return json.load(json_file)
    else:
        print("Tag Json does not exist.")
        return tags_json_init()

def tags_json_update(new_tags):
    tags = get_tags_json()
    for category in new_tags:
        for new_tag in tags[category]:
            if new_tag not in tags[category]:
                tags[category].append(new_tag)
    
    tags["skill_num"]=len(tags["skill"])
    tags["location_num"]=len(tags["location"])
    tags["education_num"]=len(tags["education"])
    tags["position_num"]=len(tags["position"])

    with open("tags.json", 'w') as json_file:
        json.dump(tags, json_file, indent=2)

    s3 = boto3.client('s3',
        aws_access_key_id="AKIAWX2IF5YDAMM7FH4V",
        aws_secret_access_key="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",
        region_name="ap-northeast-2"
    )
    bucket_name = "gaenchwis-sagemaker"

    s3.upload_file("tags.json", bucket_name, "tags.json")

    return tags
    
def new_tag_add(category, tag_name, tags_json, tags_group):
    if tag_name not in tags_json[category]:
        new_tags = {
            category: [tag_name]
        }
        tags_json = tags_json_update(new_tags)
    tags_group[category].append(tag_name)
    
    return tags_json, tags_group

def train_tags_group():
    dynamodb = boto3.resource('dynamodb')
    job_postings_table = dynamodb.Table("job_postings")

    tags_groups = []

    job_postings = job_postings_table.query(
        IndexName="StatusIndex",
        KeyConditionExpression="GSI1PK = :gsi1pk",
        ExpressionAttributeValues={
            ":gsi1pk": "STATUS#active"
        }
    )

    for job_postings_item in job_postings["Items"]:
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
    users_table = dynamodb.Table("users")

    user = users_table.get_item(Key={'PK': "USER#"+user_id})

    user_tags_table = dynamodb.Table("user_tags")

    user_tags = user_tags_table.query(
        KeyConditionExpression="PK = :pk",
        ExpressionAttributeValues={
            ":pk": user["PK"]
        }
    )

    tags_group = {
        'skill': [],
        'location': [],
        'education': [],
        'position': []
    }

    for user_tag in user_tags["Items"]:
        tags_table = dynamodb.Table("tags")

        tags = tags_table.query(
            KeyConditionExpression="PK = :pk",
            ExpressionAttributeValues={
                ":pk": user_tag["SK"]
            }
        )
        tags_group[tags["Items"][0]["tag_category"]].append(tags["Items"][0]["tag_name"])
        
    for category in tags_group:
        if not tags_group[category]:
            tags_group[category].append(None)
    
    return tags_group