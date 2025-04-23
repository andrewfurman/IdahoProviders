
from flask import Flask
from networks.networks_routes import networks_bp

app = Flask(__name__)
app.register_blueprint(networks_bp)

@app.route('/')
def index():
    return networks_bp.networks()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
