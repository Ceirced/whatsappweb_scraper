#!/usr/bin/env python3
import os
import json


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

if __name__ == '__main__':
    add = True
    while add:
        name = input('name of user to add: ')
        add_user(name)
        with open('users.json', 'r') as f:
            users = json.load(f)
    
        print(f'number of users: {len(users["users"])}')
        add = input('add another user? (y/n) ') == 'y'

