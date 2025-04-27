
from flask import Flask
from providers.providers_routes import providers_bp

app = Flask(__name__)
app.register_blueprint(providers_bp)

from flask import redirect, url_for

@app.route('/')
def index():
    return redirect(url_for('providers.providers'))

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
