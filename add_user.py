#!/usr/bin/env python3
import os
import json
import argparse 

def add_user(name: str):
    """adds a user to the users.json file"""
    with open('users.json', 'r') as f:
        users = json.load(f)
    
    if name in [entry["name"] for entry in users["users"]] or name == "":
        print(f'User {name} already exists, or name is empty')
        return
    users["users"].append({"name": name})
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)
    print(f'added user {name} to users.json')

def userCount():
    """returns the number of users in users.json"""
    with open('users.json', 'r') as f:
        users = json.load(f)
    return len(users["users"])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='add a user to the users.json file')
    parser.add_argument('-n' , '--name', type=str,help='name of user to add')
    args = parser.parse_args()

    if args.name:
        add_user(args.name)
        print(f'number of users: {userCount()}')
        quit()

    add = True
    while add:
        name = input('name of user to add: ')
        add_user(name)
        print(f'number of users: {userCount()}')
        add = input('add another user? (y/n) ') == 'y'

