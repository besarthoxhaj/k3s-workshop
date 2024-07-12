import os
import sys
import torch
import torchvision
import datetime
import minio
import mnist


torch.manual_seed(42)
transform = torchvision.transforms.Compose([torchvision.transforms.ToTensor(), torchvision.transforms.Normalize((0.1307,), (0.3081,))])
trn_ds = torchvision.datasets.MNIST(root='./mnist_data', train=True, transform=transform, download=True)
trn_dl = torch.utils.data.DataLoader(trn_ds, batch_size=128, shuffle=True)
tst_ds = torchvision.datasets.MNIST(root='./mnist_data', train=False, transform=transform)
tst_dl = torch.utils.data.DataLoader(tst_ds, batch_size=128, shuffle=False)


model = mnist.CNN()
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters())


model.train()
for idx, (x, y) in enumerate(trn_dl, 1):
  optimizer.zero_grad()
  y_ = model(x)
  loss = criterion(y_, y)
  loss.backward()
  optimizer.step()
  print(f'[{idx:04}/{len(trn_dl):04}] Loss: {loss.item():.5f}')
  if (idx != len(trn_dl)): sys.stdout.write("\033[F\033[K")
  # [0469/0469] Loss: 0.01513


torch.save(model.state_dict(), './weights.pth')
hostpath = 'minio-service.workshop' if os.getenv('APP_ENV') == 'production' else 'localhost'
c = minio.Minio(f'{hostpath}:9000', access_key='ln12nka1a7te', secret_key='a1jkcxj2xaopa', secure=False)
does_bucket_exists = c.bucket_exists('mnist')
if not does_bucket_exists: c.make_bucket('mnist')
ts = int(datetime.datetime.now().timestamp())
c.fput_object('mnist', f'weights_{ts}.pth', './weights.pth')
