import torch
import torch.nn as nn
import torch.optim as optim

def Train(type, train_tags, model, lr=0.001):
    optimizer = optim.Adam(model.parameters(), lr=lr)

    total_loss = 0
    model.train()
    for train_tag in train_tags:
        tags = torch.tensor(train_tag, dtype=torch.long)

        output = model(tags)
        output_center = output.mean(dim=0)

        loss = sum(LossFunction(out, output_center) for out in output)
        total_loss += loss.item()

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f"{type} Training, Loss: {total_loss}")
    
    return model

def LossFunction(output, target):
    criterion = nn.MSELose()
    return criterion(output, target)