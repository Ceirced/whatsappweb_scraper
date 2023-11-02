import mysql.connector
import json
import os
from user import User
from check_sync import js_db_users_synced, json_db_picture_synced
from database import Session
from models import users_table, pictures_table

session = Session()
#check if json file is synced with db
if not js_db_users_synced():
    print('json file is not synced with db, please run insert_users.py')
    exit()

if json_db_picture_synced():
    print('pictures synced, nothing to do')
    exit()

PROJECT_DIRECTORY = '/home/cederic/whatsappweb_scraper'

root_directory = f'{PROJECT_DIRECTORY}/profile_pictures'
subfolders = [folder for folder in os.listdir(root_directory) if os.path.isdir(os.path.join(root_directory, folder))]
users = session.query(users_table).all()

try:
    for user in users:
        user = User(user.contact_name)
        profile_pictures = user.profile_pictures
        for timestamp, profile_picture in profile_pictures.items():
            print(timestamp, profile_picture)
            session.add(pictures_table(user_id=user.user_id, timestamp=timestamp, picture_filename=profile_picture))
    session.commit()
except Exception as e:
    print(f"Error: {str(e)}")
finally:
    session.close()
        


