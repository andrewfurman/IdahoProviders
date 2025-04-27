
from flask import Flask
from networks.networks_routes import networks_bp
from providers.providers_routes import providers_bp

app = Flask(__name__)
app.register_blueprint(networks_bp)
app.register_blueprint(providers_bp)

from flask import redirect, url_for

@app.route('/')
def index():
    return redirect(url_for('networks.networks'))

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
