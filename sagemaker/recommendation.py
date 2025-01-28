import Tag
import torch
import torch.nn.functional as F
import Layer
import boto3

def Recommendation(user_id):
    tags_json = Tag.get_tags_json()
    tags_group = Tag.MakeUserTagGroup(user_id)


    for i in range(len(tags_group["position"])):
        tags_group["position"][i]=tags_json["position"].index(tags_group["position"][i])
    for i in range(len(tags_group["location"])):
        tags_group["location"][i]=tags_json["location"].index(tags_group["location"][i])
    for i in range(len(tags_group["education"])):
        tags_group["education"][i]=tags_json["education"].index(tags_group["education"][i])
    for i in range(len(tags_group["skill"])):
        tags_group["skill"][i]=tags_json["skill"].index(tags_group["skill"][i])

    position_model = torch.load("position_model.pth")
    location_model = torch.load("location_model.pth")
    education_model = torch.load("education_model.pth")
    skill_model = torch.load("skill_model.pth")

    position_model.eval()
    location_model.eval()
    education_model.eval()
    skill_model.eval()

    user_vector = Layer.Vector(tags_group, position_model, location_model, education_model, skill_model)
    
    return BestRecommendation(user_vector)

def BestRecommendation(user_vector):
    dynamodb = boto3.resource('dynamodb')
    job_postings_table = dynamodb.Table("job_postings")


    job_postings = job_postings_table.query(
        IndexName="StatusIndex",
        KeyConditionExpression="GSI1PK = :gsi1pk",
        ExpressionAttributeValues={
            ":gsi1pk": "STATUS#active"
        }
    )
    result=[]
    for job_postings_item in job_postings["Items"]:
        if job_postings_item.get("recommend_vector_a"):
            a=job_postings_item.get("recommend_vector_a")
            b=job_postings_item.get("recommend_vector_b")
            c=job_postings_item.get("recommend_vector_c")
            d=job_postings_item.get("recommend_vector_d")
            similarity = F.cosine_similarity(user_vector, [a,b,c,d], dim=0)
            result.append([similarity, job_postings_item])
    
    return sorted(result, key=lambda x: x[0], reverse=True)