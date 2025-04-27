
from flask import Flask, redirect, url_for
from providers.providers_routes import providers_bp, db
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(providers_bp)

@app.route('/')
def index():
    return redirect(url_for('providers.providers'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
