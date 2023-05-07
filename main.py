#!/usr/bin/env python3
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
import argparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import json
from selenium.webdriver.common.keys import Keys
import urllib.request
import os
import time

DATA_DIRECTORY = './profile_pictures/'

class User:
    def __init__(self, name):
        self.name = name
        self.status = {}
        self.userdir = f'{DATA_DIRECTORY}{self.name}'
        if self.JsonFileExists():
            self.profile_pictures = self.getOldProfilePictures()
        else:
            print(f'No json file found for {self.name}, creatiung new one')
            self.profile_pictures = {}
            self.saveUserJson()

    def JsonFileExists(self):
        if not os.path.exists(f'{self.userdir}/{self.name}.json'):
            print(f'No json file found for {self.name}')
            return False
        return True

    def getOldStatuses(self):
        with open(f'{DATA_DIRECTORY}{self.name}.json') as f:
            self.status = json.load(f)['status']
    
    
    def add_status(self, status):
        """adds a status to the status dictionary"""
        self.status[int(time.time())] = status
        self.saveUserJson()

    def getOldProfilePictures(self):
        with open(f'{self.userdir}/{self.name}.json') as f:
            return json.load(f)['profile_pictures']
        
    def addProfilePicture(self, identifier):
        self.profile_pictures[int(time.time())] = identifier
        self.saveUserJson()

    def saveUserJson(self):
        dictionary = {
            'name': self.name,
            'statuses': self.status,
            'profile_pictures': self.profile_pictures
        }
        with open(f'{self.userdir}/{self.name}.json', 'w') as f:
            json.dump(dictionary, f)
        print(f'saved json file for {self.name}')
    
    def lastProfilepictureChange(self):
        #returns the time of the last profile picture change
        return int(max(self.profile_pictures.keys()))
    
    def lastProfilePictureIdentifier(self):
        #returns the identifier of the last profile picture
        return self.profile_pictures[self.lastProfilepictureChange()]
    

        
        

def parse_arguments():
    parser = argparse.ArgumentParser(description='Whatsapp Profile picture scraper')
    parser.add_argument('-t', '--time', help='Time to wait for login in seconds', required=False, default=30)
    parser.add_argument('--head', help='Run with open browser window', action='store_true')
    parser.add_argument('-u', '--user', help='scrape specific user', nargs=1, required=False)
    return parser.parse_args()

def read_users():
    with open('users.json') as f:
        users = json.load(f)['users']
    return users

def wait_for_login(driver, time: int):
    print(f'waiting for login for {time} seconds')
    try:
        WebDriverWait(driver, time).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]'))
        )
    except:
        print('Timeout while waiting for search box')
        quit()
    print('login successful')

def search_user(driver, name):
    clear_search(driver)
    searchBox = driver.find_element('xpath', '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]')
    searchBox.send_keys(name)
    print(f'entered {name} in search box')

def clear_search(driver):
    searchBox = driver.find_element('xpath', '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]')
    searchBox.send_keys(Keys.CONTROL + "a")
    searchBox.send_keys(Keys.DELETE)

def NewPicture(driver, user):
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, f'//img[contains(@src, \'{user.lastProfilePictureIdentifier()}\')]'))
        )
        return False
    except Exception as e:
        return True

def getStatus(driver, user):
    #function to get status of user
    #should only be called when profile was already klicked

    try:
        status = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[6]/span/div/span/div/div/section/div[2]/span/span'))
        )
    except Exception as e:
        print(e)
        return 'Could not get status'
    print(f'got status for {user["name"]}')
    print(status.text)
    return status.text




def main(args):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--user-data-dir=./User_Data')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3641.0 Safari/537.36')
    if args.head:
        options.arguments.remove("--headless")  

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options, )  # 2nd change
    driver.get('https://web.whatsapp.com/')

    users = read_users()
    if args.user:
        users = [user for user in users if user['name'] == args.user[0]]
        if len(users) == 0:
            print(f'No user found with name {args.user[0]}')
            quit()

    wait_for_login(driver, int(args.time))
    image_url = ''
    for user in users:
        print(f'\n{"":~^50}\n')
        print(f'Getting profile picture for {user["name"]}')
        user = User(user['name'])
        search_user(driver, user.name)
        try:
            chat = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, f'//span[contains(@title,\'{user.name}\')]'))
            )
            print(f'found chat with {user.name}')
        except Exception as e:
            print(e)
            print(f'No user found for {user.name}')
            continue

        if NewPicture(driver,user):
            print(f'New Picture for {user.name}')
        else:
            print(f'No new Picture for {user.name}')
            continue

        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(chat)
            )
            print(f'chat clickable for {user.name}')
        except:
            print(f'chat not clickable for {user.name}')
        counter = 0
        while counter < 5: 
            try:
                chat.click()
                break
            except:
                print(f'could not open chat with {user.name}\ntrying again')
                counter += 1

                sleep(1)

        if counter == 5:
            print(f'could not open chat with {user.name} after 5 tries')
            continue
        
        try:
            profile = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[5]/div/header/div[2]/div/div/span')))
        except Exception as e:
            print(e)
            print(f'Profile not Clickable {user.name}')
            continue
        if profile.text != user.name:
            print('opened wrong chat')
            print(f'opened chat with {profile.text} instead of {user.name}. Skipping...')
            continue
        profile.click()
        print(f'clicked profile for {user.name}')

        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/div/div/div[6]/span/div/span/div/div/section/div[1]/div/div[2]/h2/span[contains(text(), "{user.name}")]'))
            )
            print(f'{user.name} profile opened')
        except Exception as e:
            print(f'could not open profile for {user.name}')
            input('press enter to continue')

        # status = getStatus(driver, user)
        # print(f'Status: {status}')
        try:
            profile_picture = driver.find_element('xpath', '/html/body/div[1]/div/div/div[6]/span/div/span/div/div/section/div[1]/div/div[1]/div/img')
        except:
            print(f'No profile picture for {user.name}')
            continue
        image_url = profile_picture.get_attribute('src')
        identifier = image_url.split('_n.jpg')[0].split('/')[-1]

        if not os.path.exists(f'./profile_pictures/{user.name}'):
            os.makedirs(f'./profile_pictures/{user.name}')
        
        if os.path.exists(f'./profile_pictures/{user.name}/{user.name}_{identifier}.jpg'):
            print(f'profile picture for {user.name} already exists')
            continue
        image_name = f'./profile_pictures/{user.name}/{user.name}_{identifier}.jpg'
        urllib.request.urlretrieve(image_url, image_name)
        print(f'saved profile picture as {image_name}')
        user.addProfilePicture(identifier)


    # input('Press enter to exit')


args = parse_arguments()
main(args)
