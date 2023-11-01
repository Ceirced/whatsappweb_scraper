import json
from database import Session
from models import users_table

PROJECT_DIRECTORY = '/home/cederic/whatsappweb_scraper'
session = Session()
json_file = f"{PROJECT_DIRECTORY}/users.json"

def js_db_users_synced():
    try: 
        with open(json_file, "r") as file:
            data = json.load(file)
            users_in_js = set([i['name'] for i in data.get("users", [])])
    except Exception as e:
        print('Could not open json file')
        print(f"Error: {str(e)}")

    try:
        #get all users from the database
        users_objects = session.query(users_table).all()
        users_in_db = set([user_object.contact_name for user_object in users_objects])
    except Exception as e:
        print(f"Error: {str(e)}")

    not_in_db = users_in_js - users_in_db
    not_in_js = users_in_db - users_in_js
    if not_in_db == not_in_js == set():
        print(f'js and db are synced\n{len(users_in_js)} users')
        return True
    else:
        print(f'in js but not in db: {not_in_db}')
        print(f'in db but not in js: {not_in_js}')
        return False

if __name__ == '__main__':
    js_db_users_synced()