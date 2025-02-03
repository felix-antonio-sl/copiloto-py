# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
import os

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    app = Flask(__name__, template_folder=os.path.join(base_dir, 'templates'))
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        from app import models
        db.create_all()

    # Import and register blueprint
    from app import routes
    app.register_blueprint(routes.bp)

    return app 