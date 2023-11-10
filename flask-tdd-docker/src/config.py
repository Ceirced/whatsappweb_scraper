import os
from dotenv import load_dotenv

load_dotenv()

class BaseConfig:
    TESTING = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = False
    FLASK_ENV = 'testing'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(BaseConfig):
    DEBUG = True
    FLASK_ENV = 'development'
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI = os.getenv('PRODUCTION_DATABASE_URI')