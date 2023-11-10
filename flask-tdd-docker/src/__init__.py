from flask import Flask
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import os

# instantiate the app
app = Flask(__name__)

api = Api(app)

app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)
db = SQLAlchemy(app)

from . import routes
api.add_resource(routes.get_user, '/user/<int:user_id>')