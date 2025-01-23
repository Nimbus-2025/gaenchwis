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
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, position, location, education, skill):
        combined = torch.cat([position, location, education, skill], dim=-1)
        output = self.fc(combined)
        return output