
import os
import sys
import logging
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    
    # Configure database
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        logger.error("DATABASE_URL environment variable not set")
        sys.exit(1)
        
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize SQLAlchemy and Migrate
    db = SQLAlchemy(app)
    from flask_migrate import Migrate
    migrate = Migrate(app, db, directory='migrations')
    
    return app

def init_db():
    try:
        # Create app context
        app = create_app()
        
        # Check and create database if needed
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        if not database_exists(engine.url):
            logger.info("Creating database...")
            create_database(engine.url)
            logger.info("Database created successfully")
        else:
            logger.info("Database already exists")

        # Run migrations
        logger.info("Running database migrations...")
        with app.app_context():
            from flask_migrate import upgrade
            upgrade(directory='.')
            
        logger.info("Database initialization completed successfully")
        return 0
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(init_db())
