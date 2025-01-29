import json
import NewJobPostings
import Training
import recommendation
import Tag

def model_fn(model_dir):
    # SageMaker 엔드포인트에서 모델 로드를 처리할 경우 사용
    # 여기서는 단순히 호출만 가능하도록 로직 정의
    return None

def predict_fn(input_data, model):
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
        return request_body
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