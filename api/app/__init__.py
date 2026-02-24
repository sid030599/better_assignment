"""Recipe Manager Flask application factory."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from config import Config, ensure_instance_dir

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    ensure_instance_dir()

    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    with app.app_context():
        from app.routes import recipes_bp, ingredients_bp
        app.register_blueprint(recipes_bp, url_prefix="/api")
        app.register_blueprint(ingredients_bp, url_prefix="/api")

    return app
