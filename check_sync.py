import json
from database import Session
from models import users_table, status_table, pictures_table
import os
from sqlalchemy import select
from user import User

PROJECT_DIRECTORY = '/home/cederic/whatsappweb_scraper'
PROFILE_PICTURES_DIRECTORY = f'{PROJECT_DIRECTORY}/profile_pictures'
subfolders = [folder for folder in os.listdir(PROFILE_PICTURES_DIRECTORY) if os.path.isdir(os.path.join(PROFILE_PICTURES_DIRECTORY, folder))]
session = Session()
json_file = f"{PROJECT_DIRECTORY}/users.json"

def get_users_in_db() -> set[str]:
    """returns a set of all users in the database

    Returns:
        set[str]: set of all contact names in the database
    """
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

def json_db_picture_synced() -> bool:
    """Compares the pictures in the json files with the pictures in the database
    and checks if all images in the database are also saved on disk

    Returns:
        bool: True if the pictures are synced, False otherwise
    """
    
    contact_names = get_users_in_db()

    #join users and profile_pictures
    stmt = select(users_table.contact_name, pictures_table.picture_filename, pictures_table.timestamp).join(pictures_table)
    db_pictures = set(session.execute(stmt).all())

    js_pictures = set()
    saved_pictures = set()
    for contact_name in contact_names:
        user = User(contact_name)
        jpg_files = ['_'.join(name.split('_')[1:]).split('.')[0] for name in os.listdir(user.userdir) if name.endswith('.jpg')]
        
        #add tuples of (name, picture, timestamp) to saved_pictures
        for picture in jpg_files:
            saved_pictures.add((user.name, picture))
        
        json_file = os.path.join(user.userdir, f'{user.name}.json')
        with open(json_file) as f:
            folder_data = json.load(f)
        name = folder_data['name']
        profile_pictures = folder_data['profile_pictures']
        for timestamp, picture in profile_pictures.items():
            js_pictures.add((name, picture, int(timestamp)))
    not_in_db = js_pictures - db_pictures
    not_in_js = db_pictures - js_pictures
    # saved images do not have a timestamp
    not_saved = {(name, picture_filename) for (name, picture_filename, timestamp) in db_pictures} - saved_pictures
    if not not_in_db == not_in_js == set():
        print(f'ERROR: js and db pictures are not synced')
        print(f'pictures in js but not in db: {not_in_db}')
        print(f'pictures in db but not in js: {not_in_js}')
        return False 
    
    print(f'js and db pictures are synced\n{len(js_pictures)} pictures')
    if not_saved != set():
        print(f'ERROR: saved images and db pictures are not synced')
        print(f'pictures in db but not saved: {not_saved}')
        return False
    print(f'all images in db and json are saved')
    return True

if __name__ == '__main__':
    # just to debug
    js_db_users_synced()
    json_db_status_synced()
    json_db_picture_synced()