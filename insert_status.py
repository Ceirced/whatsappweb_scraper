import json
import os
from user import User
from check_sync import js_db_users_synced, json_db_status_synced
from database import Session
from models import users_table, status_table


session = Session()
#check if json file is synced with db
if not js_db_users_synced():
    print('json file is not synced with db, please run insert_users.py')
    exit()
    
if json_db_status_synced():
    exit()

# Database connection parameters
with open("app/config.json", "r") as file:
    db_config = json.load(file)


PROJECT_DIRECCTORY = '/home/cederic/whatsappweb_scraper'
root_directory = f'{PROJECT_DIRECCTORY}/profile_pictures'
subfolders = [folder for folder in os.listdir(root_directory) if os.path.isdir(os.path.join(root_directory, folder))]
users = session.query(users_table).all()

try:
    for user in users:
        user = User(user.contact_name)
        status = user.statuses
        for timestamp, status in status.items():
            session.add(status_table(user_id=user.user_id, timestamp=timestamp, status=status))
    session.commit()
except Exception as e:
    print(f"Error: {str(e)}")
finally:
    session.close()
        


