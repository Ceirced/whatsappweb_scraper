#!/usr/bin/env python3
import json
import argparse 
from database import Session
from models import users_table
from check_sync import js_db_users_synced, get_users_in_db
from vobject import readOne
import os
import difflib

session = Session()

VCF_DIRECTORY = '/home/cederic/contacts/contacts'
PROJECT_DIRECTORY = '/home/cederic/whatsappweb_scraper'



if not js_db_users_synced():
    print('ERROR: users.json and database are not synced, something went wrong')
    quit()

def parse_vcf_files(vcfs_directory: str):
    fullnames = []
    for filename in os.listdir(vcfs_directory):
        absoulte_filename = f'{vcfs_directory}/{filename}'
        with open(absoulte_filename, 'r') as f:
            vcf = readOne(f)
        fullname = vcf.fn.value  
        fullnames.append(fullname)
    return fullnames

def find_exact_match(fullnames: list[str], input_fullname: str):
    return input_fullname in fullnames

def suggest_closest_matches(fullnames: list[str], input_fullname: str):
    closest_matches = difflib.get_close_matches(input_fullname, fullnames)
    return closest_matches

def add_user(name: str):
    """adds a user to the users.json file"""
    with open(f'{PROJECT_DIRECTORY}/users.json', 'r') as f:
        users = json.load(f)
    
    if name in get_users_in_db() or name == "":
        print(f'User {name} already exists, or name is empty')
        return
        
    users["users"].append({"name": name})
    session.add(users_table(contact_name=name))
    session.commit()
    with open(f'{PROJECT_DIRECTORY}/users.json', 'w') as f:
        json.dump(users, f, indent=4)
    print(f'added user {name} to users.json')

def userCount():
    """returns the number of users in users.json"""
    return session.query(users_table).count()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='add a user to the users.json file')
    parser.add_argument('-n' , '--name', type=str,help='name of user to add')
    args = parser.parse_args()
    
    print(f'parsing vcf files in {VCF_DIRECTORY}')
    fullnames = parse_vcf_files(VCF_DIRECTORY)

    if args.name:
        add_user(args.name)
        print(f'number of users: {userCount()}')
        quit()

    add = True
    users_to_add = []
    while add:
        input_fullname = input('name of user to add: ')
        if find_exact_match(fullnames, input_fullname):
            print(f"Exact match found: {input_fullname}")
        else:
            # Step 4: Suggest closest matches
            closest_matches = suggest_closest_matches(fullnames, input_fullname)
            if closest_matches:
                print(f"No exact match found. Closest matches: {closest_matches}")
                continue
            else:
                print("No match found.")
                continue
        users_to_add.append(input_fullname)
        add = input('add another user? (y/n) ') == 'y'

    for user in users_to_add:
        print(user)
    
    input('do you want to add the these users? (press enter to continue)')
    for user in users_to_add:
        add_user(user)    
    
    print(f'number of users: {userCount()}')
