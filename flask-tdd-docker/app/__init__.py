from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

#to set the app Settings in the docker compose
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models