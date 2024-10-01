import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

with open("config.json", "r") as config_file:
    config_data = json.load(config_file)

user = config_data["user"]
password = config_data["password"]
host = config_data["host"]
database = config_data["database"]
port = config_data["port"]

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
