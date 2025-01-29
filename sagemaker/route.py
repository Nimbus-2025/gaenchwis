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
    data = flask.request.get_json()
    print(data)
    try:
        logic_type = data.get("logic_type")
        payload = data.get("payload")

        if logic_type == "NewJobPostingTrain":
            return flask.jsonify(NewJobPostingTrain(payload))
        elif logic_type == "UserRecommendation":
            return flask.jsonify(UserRecommendation(payload))
        elif logic_type == "InitTrain":
            return flask.jsonify(InitTrain())
        elif logic_type == "InitJobPosting":
            return flask.jsonify(InitJobPosting())
        elif logic_type == "InitTagJson":
            return flask.jsonify(InitTagJson())
    except Exception as e:
        return {"error": f"Exception occurred: {str(e)}"}

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

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)