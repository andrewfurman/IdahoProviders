
from flask import Flask, redirect, url_for
from providers.providers_routes import providers_bp, db
from flask_mail import Mail
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer
import os

app = Flask(__name__)

# Configure app
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_prefixed_env()  # Loads FLASK_ and other prefixed env vars

# Initialize extensions
db.init_app(app)
mail = Mail(app)
login_manager = LoginManager(app)

# Ensure secret key is set
if not app.config.get("FLASK_SECRET_KEY"):
    raise ValueError("FLASK_SECRET_KEY environment variable is not set")
if not app.config.get("SECURITY_TOKEN_SALT"):
    raise ValueError("SECURITY_TOKEN_SALT environment variable is not set")

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
