import torch
import flask as f
import mnist


app = f.Flask(__name__)
torch.set_grad_enabled(False)
model = mnist.CNN()
model.load_state_dict(torch.load('./weights.pth'))
model.eval()


@app.route('/', methods=['GET'])
def index():
  return 'Predictor is up and running!'


@app.route('/prediction', methods=['POST'])
def predict():
  data = f.request.get_json()
  x = torch.tensor(data['pix']).view(1, 1, 28, 28)
  x = (x / 255.0 - 0.1307) / 0.3081
  output = model(x) # <-- magic happens here
  output = output.argmax(dim=1, keepdim=True).item()
  return f.jsonify({'prediction': output})


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5015)