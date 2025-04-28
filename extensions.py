
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer

# Initialize extensions without app context
db = SQLAlchemy()
mail = Mail()
login_mgr = LoginManager()
ts = None  # Will be initialized in app context

def init_extensions(app):
    global ts
    
    # Initialize extensions with app
    db.init_app(app)
    mail.init_app(app)
    login_mgr.init_app(app)
    
    # Create URL safe serializer
    ts = URLSafeTimedSerializer(
        secret_key=app.config["FLASK_SECRET_KEY"],
        salt=app.config["SECURITY_TOKEN_SALT"]
    )
