import psycopg2
import torch
import mnist
import shutil
import datetime
import minio
import os

#
#
url_minio = 'minio-service.workshop:9000' if os.getenv('APP_ENV') == 'production' else 'localhost:9000'
c = minio.Minio(url_minio, access_key='ln12nka1a7te', secret_key='a1jkcxj2xaopa', secure=False)
objects = c.list_objects('mnist', recursive=True)
objects = sorted(objects, key=lambda x: x.last_modified, reverse=True)
c.fget_object('mnist', objects[0].object_name, './weights.pth')

#
#
hostpath_pg = 'pg-service.workshop' if os.getenv('APP_ENV') == 'production' else 'localhost'
conn = psycopg2.connect(f'postgresql://ab93lka1z1a:bxlao9koslq51@{hostpath_pg}:5432')
cur = conn.cursor()
query = "SELECT id, img_json, prediction, label FROM fct_prediction WHERE label IS NOT NULL AND prediction IS NOT NULL AND label <> '' AND prediction <> '';"
cur.execute(query)
rows = cur.fetchall()
cur.close(); conn.close()

#
#
store = []
for r in rows: 
  if r[1] == None or r[3] == None: continue #  skip if missing
  img_tensor = torch.tensor(r[1], dtype=torch.float32).view(1, 28, 28)
  img_tensor = (img_tensor / 255.0 - 0.1307) / 0.3081
  lbl_tensor = torch.tensor(int(r[3]), dtype=torch.long)
  store.append((img_tensor, lbl_tensor))

#
#
imgs, lbls = zip(*store)
imgs = torch.stack(imgs)
lbls = torch.tensor(lbls)
print(imgs.shape, lbls)

#
#
torch.manual_seed(42)
model = mnist.CNN()
model.load_state_dict(torch.load('./weights.pth'))
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

#
#
model.eval()
torch.set_grad_enabled(False)
y_ = model(imgs)
loss = criterion(y_, lbls)
print(f'Before Loss: {loss.item():.5f}')

#
#
model.train()
torch.set_grad_enabled(True)
y_ = model(imgs)
loss = criterion(y_, lbls)
loss.backward()
optimizer.step()

#
#
model.eval()
torch.set_grad_enabled(False)
y_ = model(imgs)
loss = criterion(y_, lbls)
print(f'After Loss: {loss.item():.5f}')
ts = int(datetime.datetime.now().timestamp())
name = f'./weights_{ts}.pth'
torch.save(model.state_dict(), name)

#
#
DOCKERFILE = f"""
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime
WORKDIR /usr/src/app
COPY weights.pth .
COPY mnist.py .
COPY predictor.py .
RUN pip install Flask
CMD ["python", "predictor.py"]
"""

#
#
os.makedirs('/share', exist_ok=True)
shutil.copy(name, '/share/weights.pth')
shutil.copy('./predictor.py', '/share/predictor.py')
shutil.copy('./mnist.py', '/share/mnist.py')
with open('/share/Dockerfile', 'w') as f: f.write(DOCKERFILE)
