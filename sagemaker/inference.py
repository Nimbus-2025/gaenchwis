import Layer
import torch
import json
import NewJobPostings
import Training
import recommendation
import Tag
import boto3

def model_fn(model_dir):
    tags_json = Tag.get_tags_json()
    
    position_tags=len(tags_json["position"])
    location_tags=len(tags_json["location"])
    education_tags=len(tags_json["education"])
    skill_tags=len(tags_json["skill"])

    s3 = boto3.client('s3',
        aws_access_key_id="AKIAWX2IF5YDAMM7FH4V",
        aws_secret_access_key="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",
        region_name="ap-northeast-2"
    )
    bucket_name = "gaenchwis-sagemaker"

    position_model = Layer.TagsTrainModel(position_tags, 128)
    location_model = Layer.TagsTrainModel(location_tags, 128)
    education_model = Layer.TagsTrainModel(education_tags, 128)
    skill_model = Layer.TagsTrainModel(skill_tags, 128)
    
    s3.download_file(bucket_name, "position_model.pth", "position_model.pth")
    s3.download_file(bucket_name, "location_model.pth", "location_model.pth")
    s3.download_file(bucket_name, "education_model.pth", "education_model.pth")
    s3.download_file(bucket_name, "skill_model.pth", "skill_model.pth")

    position_model.load_state_dict(torch.load("position_model.pth"), strict=False)
    location_model.load_state_dict(torch.load("location_model.pth"), strict=False)
    education_model.load_state_dict(torch.load("education_model.pth"), strict=False)
    skill_model.load_state_dict(torch.load("skill_model.pth"), strict=False)

    position_model.eval()
    location_model.eval()
    education_model.eval()
    skill_model.eval()

    return {
        "position_model": position_model,
        "location_model": location_model,
        "education_model": education_model,
        "skill_model": skill_model
    }

def predict_fn(input_data, models):
    try:
        data = json.loads(input_data)
        logic_type = data.get("logic_type")
        payload = data.get("payload")

        if logic_type == "NewJobPostingTrain":
            return NewJobPostingTrain(payload)
        elif logic_type == "UserRecommendation":
            return UserRecommendation(payload)
        elif logic_type == "InitTrain":
            return InitTrain()
        elif logic_type == "InitJobPosting":
            return InitJobPosting()
        elif logic_type == "InitTagJson":
            return InitTagJson()
    except Exception as e:
        return {"error": f"Exception occurred: {str(e)}"}

def input_fn(request_body, content_type):
    if content_type == "application/json":
        return json.loads(request_body)
    else:
        raise ValueError("Unsupported content type: {content_type}")

def output_fn(prediction, accept):
    if accept == "application/json":
        return json.dumps(prediction), "application/json"
    else:
        raise ValueError("Unsupported accept type: {accept}")

def NewJobPostingTrain(job_postings_item):
    return NewJobPostings.NewJobPosting(job_postings_item)

def UserRecommendation(user_id):
    return recommendation.Recommendation(user_id)

def InitTrain():
    Training.StartTrain()
    return "Train Completed"
    
def InitJobPosting():
    NewJobPostings.InitJobPosting()
    return "JobPosting Vector created"

def InitTagJson():
    Tag.tags_json_init()
    return "Tag Json created"