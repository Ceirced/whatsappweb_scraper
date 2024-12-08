import argparse 
from database import Session
from models import users_table
from check_sync import get_users_in_db
import difflib

session = Session()

VCF_DIRECTORY = '/home/cederic/contacts/contacts'
PROJECT_DIRECTORY = '/home/cederic/whatsappweb_scraper'



def find_exact_match(fullnames: list[str], input_fullname: str):
    return input_fullname in fullnames

def suggest_closest_matches(fullnames: list[str], input_fullname: str):
    closest_matches = difflib.get_close_matches(input_fullname, fullnames)
    return closest_matches

def add_user(name: str):
    if name in get_users_in_db() or name == "":
        print(f'User {name} already exists, or name is empty')
        return
        
    session.add(users_table(contact_name=name))
    session.commit()

    print(f'added user {name} to database')

def userCount():
    """returns the number of users in users.json"""
    return session.query(users_table).count()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='add a user to the users.json file')
    parser.add_argument('-n' , '--name', type=str,help='name of user to add')
    args = parser.parse_args()
    
    if args.name:
        add_user(args.name)
        print(f'number of users: {userCount()}')
        quit()

    add = True
    users_to_add = []
    while add:
        input_fullname = input('name of user to add: ')
        users_to_add.append(input_fullname)
        add = input('add another user? (y/n) ') == 'y'

    for user in users_to_add:
        print(user)
    
    input('do you want to add the these users? (press enter to continue)')
    for user in users_to_add:
        add_user(user)    
    
    print(f'number of users: {userCount()}')
