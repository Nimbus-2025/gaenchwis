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

    s3 = boto3.client('s3',
    aws_access_key_id="AKIAWX2IF5YDAMM7FH4V",
    aws_secret_access_key="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",
    region_name="ap-northeast-2"
    )
    bucket_name = "gaenchwis-sagemaker"

    position_tags=len(tags_json["position"])
    location_tags=len(tags_json["location"])
    education_tags=len(tags_json["education"])
    skill_tags=len(tags_json["skill"])

    position_model = Layer.TagsTrainModel(position_tags, 128)
    location_model = Layer.TagsTrainModel(location_tags, 128)
    education_model = Layer.TagsTrainModel(education_tags, 128)
    skill_model = Layer.TagsTrainModel(skill_tags, 128)
    
    s3.download_file(bucket_name, "position_model.pth", "position_model.pth")
    s3.download_file(bucket_name, "location_model.pth", "location_model.pth")
    s3.download_file(bucket_name, "education_model.pth", "education_model.pth")
    s3.download_file(bucket_name, "skill_model.pth", "skill_model.pth")

    #position_model.load_state_dict(torch.load("position_model.pth"), strict=False)
    #location_model.load_state_dict(torch.load("location_model.pth"), strict=False)
    #education_model.load_state_dict(torch.load("education_model.pth"), strict=False)
    #skill_model.load_state_dict(torch.load("skill_model.pth"), strict=False)

    position_model.eval()
    location_model.eval()
    education_model.eval()
    skill_model.eval()

    user_vector = Layer.Vector(tags_group, position_model, location_model, education_model, skill_model).tolist()
    print("recom_f")
    return BestRecommendation(user_vector)[:5]

def BestRecommendation(user_vector):
    dynamodb = boto3.resource('dynamodb',
    aws_access_key_id="AKIAWX2IF5YDAMM7FH4V",
    aws_secret_access_key="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",
    region_name="ap-northeast-2"
    )
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

            x1_tensor = torch.tensor(user_vector, dtype=torch.float32)
            x2_tensor = torch.tensor([float(a),float(b),float(c),float(d)], dtype=torch.float32)
            similarity = F.cosine_similarity(x1_tensor.unsqueeze(0), x2_tensor.unsqueeze(0), dim=1)
            print(similarity.item())
            result.append([similarity.item(), job_postings_item])

    return sorted(result, key=lambda x: x[0], reverse=True)