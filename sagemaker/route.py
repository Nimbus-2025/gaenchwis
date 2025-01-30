import flask
import json
import NewJobPostings
import Training
import recommendation
import Tag

app = flask.Flask(__name__)

@app.route("/*", methods=["OPTIONS"])
def preflight():
    return {"status":"ok"}

@app.route("/ping", methods=["GET"])
def ping():
    response_body = "OK"
    status = 200
    return flask.Response(response=f"{response_body}\n", 
                          status=status, 
                          mimetype="application/json")

@app.route('/invocations', methods=['POST'])
def predict_fn():
    data = flask.request.get_data().decode("utf-8")
    try:
        logic_type = json.loads(data).get("logic_type")
        payload = json.loads(data).get("payload")

        if logic_type == "NewJobPostingTrain":
            return json.dumps(NewJobPostingTrain(payload))
        elif logic_type == "UserRecommendation":
            return json.dumps(UserRecommendation(payload))
        elif logic_type == "InitTrain":
            return json.dumps(InitTrain())
        elif logic_type == "InitJobPosting":
            return json.dumps(InitJobPosting())
        elif logic_type == "InitTagJson":
            return json.dumps(InitTagJson())
    except Exception as e:
        return {"error": f"Exception occurred: {str(e)}"}

def NewJobPostingTrain(job_postings_item):
    return NewJobPostings.NewJobPosting(job_postings_item)

def UserRecommendation(user_id):
    return recommendation.Recommendation(user_id)

def InitTrain():
    Training.StartTrain()
    return {"message":"Train Completed"}
    
def InitJobPosting():
    NewJobPostings.InitJobPosting()
    return {"message":"JobPosting Vector created"}

def InitTagJson():
    Tag.tags_json_init()
    print("avsdf")
    return {"message":"Tag Json created"}

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)