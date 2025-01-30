import torch
import torch.nn as nn

class TagsTrainModel(nn.Module):
    def __init__(self, num_tags, embedding_dim):
        super(TagsTrainModel, self).__init__()
        
        self.embedding = nn.Embedding(num_tags, embedding_dim)
        self.fc = nn.Sequential(
            nn.Linear(embedding_dim, embedding_dim),
            nn.ReLU(),
            nn.Linear(embedding_dim, embedding_dim),
            nn.ReLU(),
            nn.Linear(embedding_dim, embedding_dim)
        )

    def forward(self, tag_ids):
        output = self.embedding(tag_ids)
        output = torch.mean(output, dim=0)
        output = self.fc(output)
        return output
  
class CombineVectors(nn.Module):
    def __init__(self, input_dim, hidden_dim=128, output_dim=4):
        super(CombineVectors, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, position, location, education, skill):
        combined = torch.cat([position, location, education, skill], dim=-1)
        output = self.fc(combined)
        return output
    
def Vector(tags_group, position_model, location_model, education_model, skill_model):
    position_tensor = torch.tensor(tags_group["position"], dtype=torch.long)
    location_tensor = torch.tensor(tags_group["location"], dtype=torch.long)
    education_tensor = torch.tensor(tags_group["education"], dtype=torch.long)
    skill_tensor = torch.tensor(tags_group["skill"], dtype=torch.long)

    position_vector = position_model(position_tensor)
    location_vector = location_model(location_tensor)
    education_vector = education_model(education_tensor)
    skill_vector = skill_model(skill_tensor)

    combined_model = CombineVectors(input_dim=512)

    combined_vector = combined_model(position_vector, location_vector, education_vector, skill_vector)

    return combined_vector

def ModifyLayer(checkpoint, model_state):
    old_emb, new_emb = checkpoint["embedding.weight"], model_state["embedding.weight"]
    num_old, num_new, emb_dim = old_emb.shape[0], new_emb.shape[0], new_emb.shape[1]

    checkpoint["embedding.weight"] = (
        torch.cat([old_emb, torch.randn(num_new - num_old, emb_dim) * 0.01], dim=0) if num_new > num_old else old_emb[:num_new, :]
    )
    return checkpoint