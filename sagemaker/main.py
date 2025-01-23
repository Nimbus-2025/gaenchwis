import Layer
import Tag
import Training

def Train():
    position_train=[]
    location_train=[]
    education_train=[]
    skill_train=[]

    tags_groups = Tag.train_tags_group()
    for tags_group in tags_groups:
        position_train.append(tags_group["position"])
        location_train.append(tags_group["location"])
        education_train.append(tags_group["education"])
        skill_train.append(tags_group["skill"])

    tags_json = Tag.get_tags_json()
    position_tags=len(tags_json["position"])
    location_tags=len(tags_json["location"])
    education_tags=len(tags_json["education"])
    skill_tags=len(tags_json["skill"])

    position_model = Layer.TagsTrainModel(position_tags, 128)
    location_model = Layer.TagsTrainModel(location_tags, 128)
    education_model = Layer.TagsTrainModel(education_tags, 128)
    skill_model = Layer.TagsTrainModel(skill_tags, 128)
    
    Training.Train("position", position_train, position_model, lr=0.01)
    Training.Train("location", location_train, location_model, lr=0.01)
    Training.Train("education", education_train, education_model, lr=0.01)
    Training.Train("skill", skill_train, skill_model, lr=0.01)