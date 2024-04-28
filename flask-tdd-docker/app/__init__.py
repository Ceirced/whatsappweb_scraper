from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os


#to set the app Settings in the docker compose
db = SQLAlchemy()
migrate = Migrate()

def create_app() -> Flask:
    app = Flask(__name__)
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)
    db.init_app(app)
    migrate.init_app(app, db)
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    return app

from app import models