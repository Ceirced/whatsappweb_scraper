import json
import time
import os
import pathlib
from database import Session
from models import users_table, status_table, pictures_table
from sqlalchemy import select


session = Session()

DIRECTORY = pathlib.Path(__file__).parent.resolve()
DATA_DIRECTORY = f'{DIRECTORY}/profile_pictures'

class User:
    def __init__(self, name):
        self.name = name
        self.userdir = f'{DATA_DIRECTORY}/{self.name}'
        self.user_id = self.getUserId()
        if self.JsonFileExists():
            self.profile_pictures = self.getOldProfilePictures()
            self.statuses = self.getOldStatuses()
        else:
            print(f'No json file found for {self.name}, creating new one')
            self.profile_pictures = {}
            self.statuses = {}
            self.saveUserJson()
    def getUserId(self):
        return session.query(users_table).filter(users_table.contact_name == self.name).first().user_id
    
    def JsonFileExists(self):
        if not os.path.exists(f'{self.userdir}/{self.name}.json'):
            return False
        return True

    def getOldStatuses(self):
        stmt = select(status_table.timestamp, status_table.status).where(status_table.user_id == self.user_id)
        result = session.execute(stmt).all() 
        result = {str(i[0]): i[1] for i in result} #TODO: removve str() when picture timestamps are also ints
        return result

    def add_status(self, status):
        """adds a status to the status dictionary"""
        print(f'adding status {status} for {self.name}, statuses before: {self.statuses}')
        current_time = int(time.time())
        self.statuses[current_time] = status
        session.add(status_table(user_id=self.user_id, timestamp=current_time, status=status))
        session.commit()

    def getOldProfilePictures(self):
        stmt = select(pictures_table.timestamp, pictures_table.picture_filename).where(pictures_table.user_id == self.user_id)
        result = session.execute(stmt).all()
        result = {str(i[0]): i[1] for i in result}
        return result
        
    def addProfilePicture(self, identifier):
        self.profile_pictures[int(time.time())] = identifier
        current_time = int(time.time())
        session.add(pictures_table(user_id=self.user_id, timestamp=current_time, picture_filename=identifier))
        session.commit()
        
    def saveUserJson(self):
        dictionary = {
            'name': self.name,
            'statuses': self.statuses,
            'profile_pictures': self.profile_pictures
        }
        os.makedirs(self.userdir, exist_ok=True)
        with open(f'{self.userdir}/{self.name}.json', 'w') as f:
            json.dump(dictionary, f)
        print(f'saved json file for {self.name}')
    
    def lastProfilepictureChange(self):
        """returns the time of the last profile picture change"""
        try:
            lastChange = max(self.profile_pictures.keys())
            return lastChange 
        except:
            print(f'Could not get profile picture changes for {self.name}')
    def lastProfilePictureIdentifier(self) -> str:
        """returns the identifier of the last profile picture"""
        try:
            return self.profile_pictures[self.lastProfilepictureChange()]
        except:
            print(f'Could not find last profile picture identifier for {self.name}')
    
    def lastStatusChange(self):
        """returns the time of the last status change"""
        try:
            lastChange = max(self.statuses.keys())
            return lastChange
        except:
            print(f'Could not get last status changes for {self.name}')
    
    def lastStatus(self):
        """returns the last status"""
        try:
            return self.statuses[self.lastStatusChange()]
        except:
            print(f'Could not get last status for {self.name}')