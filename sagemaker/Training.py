import torch
import torch.nn as nn
import torch.optim as optim
import Layer
import Tag
import os

def Train(type, train_tags, model, lr=0.001):
    optimizer = optim.Adam(model.parameters(), lr=lr)

    total_loss = 0
    model.train()
    for e in range(1):
        for train_tag in train_tags:
            tags = torch.tensor(train_tag, dtype=torch.long)

            output = model(tags)
            output_center = output.mean(dim=0)

            loss = sum(LossFunction(out, output_center) for out in output)
            total_loss += loss.item()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        print(f"{e+1}, {type} Training, Loss: {total_loss}")
    
    return model

def LossFunction(output, target):
    criterion = nn.MSELose()
    return criterion(output, target)

def StartTrain(tags_groups=None, tags_json = Tag.get_tags_json()):
    position_train=[]
    location_train=[]
    education_train=[]
    skill_train=[]

    if not tags_groups:
        tags_groups = Tag.train_tags_group()
    
    for tags_group in tags_groups:
        if tags_groups:
            tags_json = Tag.tags_json_update(tags_group, tags_json)
        for i in range(len(tags_group["position"])):
            tags_group["position"][i]=tags_json["position"].index(tags_group["position"][i])
        for i in range(len(tags_group["location"])):
            tags_group["location"][i]=tags_json["location"].index(tags_group["location"][i])
        for i in range(len(tags_group["education"])):
            tags_group["education"][i]=tags_json["education"].index(tags_group["education"][i])
        for i in range(len(tags_group["skill"])):
            tags_group["skill"][i]=tags_json["skill"].index(tags_group["skill"][i])

        position_train.append(tags_group["position"])
        location_train.append(tags_group["location"])
        education_train.append(tags_group["education"])
        skill_train.append(tags_group["skill"])

    position_tags=len(tags_json["position"])
    location_tags=len(tags_json["location"])
    education_tags=len(tags_json["education"])
    skill_tags=len(tags_json["skill"])
    
    position_model = Layer.TagsTrainModel(position_tags, 128)
    location_model = Layer.TagsTrainModel(location_tags, 128)
    education_model = Layer.TagsTrainModel(education_tags, 128)
    skill_model = Layer.TagsTrainModel(skill_tags, 128)

    position_model_exists = os.path.exists("position_model.pth")
    location_model_exists = os.path.exists("location_model.pth")
    education_model_exists = os.path.exists("education_model.pth")
    skill_model_exists = os.path.exists("skill_model.pth")

    if position_model_exists:
        position_model = position_model.load_state_dict(torch.load(position_model_exists), strict=False)
    if location_model_exists:
        location_model = location_model.load_state_dict(torch.load(location_model_exists), strict=False)
    if education_model_exists:
        education_model = education_model.load_state_dict(torch.load(education_model_exists), strict=False)
    if skill_model_exists:
        skill_model = skill_model.load_state_dict(torch.load(skill_model_exists), strict=False)
    
    position_model=Train("position", position_train, position_model, lr=0.01)
    location_model=Train("location", location_train, location_model, lr=0.01)
    education_model=Train("education", education_train, education_model, lr=0.01)
    skill_model=Train("skill", skill_train, skill_model, lr=0.01)

    torch.save(position_model, "position_model.pth")
    torch.save(location_model, "location_model.pth")
    torch.save(education_model, "education_model.pth")
    torch.save(skill_model, "skill_model.pth")

    return position_model, location_model, education_model, skill_model