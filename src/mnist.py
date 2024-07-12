import torch


class CNN(torch.nn.Module):
  def __init__(self):
    super(CNN, self).__init__()
    self.conv1 = torch.nn.Conv2d(1, 32, kernel_size=3, padding=1)
    self.conv2 = torch.nn.Conv2d(32, 64, kernel_size=3, padding=1)
    self.pool = torch.nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
    self.fc1 = torch.nn.Linear(64 * 7 * 7, 128)
    self.fc2 = torch.nn.Linear(128, 10)
    self.relu = torch.nn.ReLU()
    self.drop = torch.nn.Dropout(0.25)

  def forward(self, x):
    x = self.pool(self.relu(self.conv1(x)))
    x = self.pool(self.relu(self.conv2(x)))
    x = x.view(-1, 64 * 7 * 7) # flatten the tensor
    x = self.relu(self.fc1(x))
    x = self.fc2(self.drop(x))
    return x


if __name__ == '__main__':
  torch.manual_seed(42)
  x = torch.randn(1, 1, 28, 28)
  model = CNN()
  model.eval()
  torch.set_grad_enabled(False)
  print(model(x))