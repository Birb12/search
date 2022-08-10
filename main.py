import torchvision
import torch
import torchvision.transforms as transforms
import os
import torch.utils.data
import torch.nn.functional as F
import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np


class ConvNetwork(nn.Module):
    def __init__(self):

        super(ConvNetwork, self).__init__()

        self.layer1 = nn.Conv2d(3, 6, 5)
        self.poollayer = nn.MaxPool2d(2, 2)
        self.layer2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16*61*61, 15000)
        self.fc2 = nn.Linear(15000, 10000)
        self.fc3 = nn.Linear(10000, 2)

    def forward(self, x):

        x = self.poollayer(F.relu(self.layer1(x)))
        x = self.poollayer(F.relu(self.layer2(x)))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

        
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = ConvNetwork().to(device)
custommean = 0.8132, 0.6343, 0.7334
customstd = 0.0807, 0.1310, 0.0968

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr = 1e-5)


transform = transforms.Compose([transforms.Resize((256, 256)), transforms.ToTensor(), transforms.Normalize(custommean, customstd)])
outputs = ("1", "0")


numepoch = 2
data_direction = os.getcwd()
trainingdata = os.path.join(data_direction, "test-train")

train_dataset = torchvision.datasets.ImageFolder(trainingdata, transform)
loader = torch.utils.data.DataLoader(train_dataset, batch_size = 100, shuffle=True)

def train():
    for epoch in range(numepoch):
        for images, labels in loader:
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            loss = criterion(outputs, labels)

            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            print(loss)
    


def show_images(train_dataset):
    batch = next(iter(loader))
    images, labels = batch

    grid = torchvision.utils.make_grid(images, nrow=3)
    plt.figure(figsize=(11,11))
    plt.imshow(np.transpose(grid, (1, 2, 0)))
    plt.show()
    print('labels: ', labels)

def save():

    torch.save({
        'modelstates' : model.state_dict(),
        "optimizerstates": optimizer.state_dict()
    }, '/checkpoint.pth')



train()
