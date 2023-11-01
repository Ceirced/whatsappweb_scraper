import json
from database import Session
from models import users_table, status_table
import os
from sqlalchemy import select

PROJECT_DIRECTORY = '/home/cederic/whatsappweb_scraper'
PROFILE_PICTURES_DIRECTORY = f'{PROJECT_DIRECTORY}/profile_pictures'
subfolders = [folder for folder in os.listdir(PROFILE_PICTURES_DIRECTORY) if os.path.isdir(os.path.join(PROFILE_PICTURES_DIRECTORY, folder))]
session = Session()
json_file = f"{PROJECT_DIRECTORY}/users.json"

def get_users_in_db():
    try:
        #get all users from the database
        users_in_db = set(session.scalars(select(users_table.contact_name)).all())
    except Exception as e:
        print(f"Error: {str(e)}")
    return users_in_db

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
        users_in_db = get_users_in_db()
    except Exception as e:
        print(f"Error: {str(e)}")

    not_in_db = users_in_js - users_in_db
    not_in_js = users_in_db - users_in_js
    if not_in_db == not_in_js == set():
        print(f'js and db users are synced\n{len(users_in_js)} users')
        return True
    else:
        print(f'users in js but not in db: {not_in_db}')
        print(f'users in db but not in js: {not_in_js}')
        return False

def json_db_status_synced():
    
    try:
        #get all users from the database
        users_in_db = get_users_in_db()
    except Exception as e:
        print(f"Error: {str(e)}")
    #join users and statuses
    stmt = select(users_table.contact_name, status_table.status, status_table.timestamp).join(status_table)
    db_status = set(session.execute(stmt).all())


    js_status = set()

    #get all users from the json files
    for folder in subfolders:
        json_file = os.path.join(PROFILE_PICTURES_DIRECTORY, folder, f'{folder}.json')
        with open(json_file) as f:
            folder_data = json.load(f)
        name = folder_data['name']
        statuses = folder_data['statuses']
        for timestamp, status in statuses.items():
            js_status.add((name, status, int(timestamp)))
    not_in_db = js_status - db_status
    not_in_js = db_status - js_status
    if not_in_db == not_in_js == set():
        print(f'js and db status are synced\n{len(js_status)} statuses')
        return True
    else:
        print(f'status in js but not in db: {not_in_db}')
        print(f'status in db but not in js: {not_in_js}')
        return False

if __name__ == '__main__':
    js_db_users_synced()
    json_db_status_synced()