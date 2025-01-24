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
        tags["position"].append((i+1)+"년")

    tags['position'].extend([
        "신입",
        "정규직",
        "인턴직",
        "프리랜서",
        "계약직",
        "파견직"
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
    
    return tags

def tags_json_update(new_tags):
    tags = get_tags_json()
    
    for category in new_tags:
        tags[category].extend(new_tags[category])
    
    tags["skill_num"]=len(tags["skill"])
    tags["location_num"]=len(tags["location"])
    tags["education_num"]=len(tags["education"])
    tags["position_num"]=len(tags["position"])

    with open("tags.json", 'w') as json_file:
        json.dump(tags, json_file, indent=2)

    return tags

def get_tags_json():
    try:
        with open("tags.json", 'r') as json_file:
            print("Tag Json already exist.")
            return json.load(json_file)
    except:
        print("Tag Json does not exist.")
        return tags_json_init()
    
def train_tags_group():
    dynamodb = boto3.resource('dynamodb')
    job_postrings_table = dynamodb.Table("job_postings")

    tags_json = get_tags_json()

    tags_groups = []

    job_postrings = job_postrings_table.query(
        IndexName="StatusIndex",
        KeyConditionExpression="GSI1PK = :gsi1pk",
        ExpressionAttributeValues={
            ":gsi1pk": "STATUS#active"
        }
    )

    def new_tag_add(category, tag_name, tags_json, tags_group):
        if tag_name not in tags_json[category]:
            new_tags = {
                category: [tag_name]
            }
            tags_json = tags_json_update(new_tags)
        tags_group[category].append(tags_json[category].index(tag_name))
        
        return tags_json, tags_group

    for job_postrings_item in job_postrings["Items"]:
        job_tags_table = dynamodb.Table("job_tags")

        job_tags = job_tags_table.query(
            KeyConditionExpression="PK = :pk",
            ExpressionAttributeValues={
                ":pk": job_postrings_item["SK"]
            }
        )

        tags_group = {
            'skill': [],
            'location': [],
            'education': [],
            'position': []
        }

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
        tags_groups.append(tags_group)
    
    return tags_groups