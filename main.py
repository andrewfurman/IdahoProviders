
from flask import Flask, redirect, url_for
from providers.providers_routes import providers_bp, db
from flask_mail import Mail
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer
import os

app = Flask(__name__)

# Configure app
app.config.from_prefixed_env()  # Loads FLASK_ and other prefixed env vars
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set secret key
if 'FLASK_SECRET_KEY' not in os.environ:
    raise ValueError("FLASK_SECRET_KEY environment variable is not set")
if 'SECURITY_TOKEN_SALT' not in os.environ:
    raise ValueError("SECURITY_TOKEN_SALT environment variable is not set")

app.secret_key = os.environ['FLASK_SECRET_KEY']

# Initialize extensions
db.init_app(app)
mail = Mail(app)
login_manager = LoginManager(app)

ts = URLSafeTimedSerializer(
    secret_key=app.config["FLASK_SECRET_KEY"],
    salt=app.config["SECURITY_TOKEN_SALT"]
)

# Register blueprints
from auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(providers_bp)

@app.route('/')
def index():
    return redirect(url_for('providers.providers'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
