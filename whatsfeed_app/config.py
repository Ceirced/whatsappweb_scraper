import os
from dotenv import load_dotenv

load_dotenv()

class BaseConfig:
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    FLASK_ENV = 'development'


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = False
    FLASK_ENV = 'testing'


class ProductionConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI = os.getenv('PRODUCTION_DATABASE_URI')