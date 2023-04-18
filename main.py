#!/usr/bin/env python3
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
import argparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from selenium.webdriver.common.keys import Keys
import urllib.request
import os
import time



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
    searchBox = driver.find_element('xpath', '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]')
    searchBox.send_keys(name)
    print(f'entered {name} in search box')

def clear_search(driver):
    searchBox = driver.find_element('xpath', '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]')
    searchBox.send_keys(Keys.CONTROL + "a")
    searchBox.send_keys(Keys.DELETE)

def NewPicture(driver, user):
    name = user['name']
    try:
        image_name = os.listdir(f'./profile_pictures/{name}')[0]
    except FileNotFoundError:
        return True
    identifier = image_name.split('_',1)[1].split('.jpg')[0]
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, f'//img[contains(@src, \'{identifier}\')]'))
        )
        return False
    except Exception as e:
        print(e)
        return True



def main(args):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--user-data-dir=./User_Data')
    if args.head:
        options.arguments.remove("--headless")  

    driver = webdriver.Chrome(options=options)  # 2nd change
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
        name = user['name']
        print(f'Getting profile picture for {name}')
        search_user(driver, name)
        try:
            chat = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, f'//span[contains(@title,\'{name}\')]'))
            )
            print(f'found chat with {name}')
        except Exception as e:
            print(e)
            print(f'No user found for {name}')
            clear_search(driver)
            continue

        if NewPicture(driver,user):
            print(f'New Picture for {name}')
        else:
            print(f'No new Picture for {name}')
            clear_search(driver)
            continue

        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(chat)
            )
            print(f'chat clickable for {name}')
        except:
            print(f'chat not clickable for {name}')
        counter = 0
        while counter < 5: 
            try:
                chat.click()
                break
            except:
                print(f'could not open chat with {name}\ntrying again')
                counter += 1

                sleep(1)

        if counter == 5:
            print(f'could not open chat with {name} after 5 tries')
            continue

        print(f'opened chat with {name}')
        try:
            profile = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[5]/div/header/div[2]/div/div/span')))
        except Exception as e:
            print(e)
            print(f'Profile not Clickable {name}')
            clear_search(driver)
            continue
        profile.click()

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/div/div/div[6]/span/div/span/div/div/section/div[1]/div[2]/h2/span[contains(text(), "{name}")]'))
        )
        try:
            profile_picture = driver.find_element('xpath', '/html/body/div[1]/div/div/div[6]/span/div/span/div/div/section/div[1]/div[1]/div/img')
        except:
            print(f'No profile picture for {name}')
            clear_search(driver)
            continue
        image_url = profile_picture.get_attribute('src')
        identifier = image_url.split('.jpg')[0].split('/')[-1]

        if not os.path.exists(f'./profile_pictures/{name}'):
            os.makedirs(f'./profile_pictures/{name}')
        
        if os.path.exists(f'./profile_pictures/{name}/{name}_{identifier}.jpg'):
            print(f'profile picture for {name} already exists')
            clear_search(driver)
            continue
        image_name = f'./profile_pictures/{name}/{name}_{identifier}.jpg'
        urllib.request.urlretrieve(image_url, image_name)
        print(f'saved profile picture as {image_name}')


        clear_search(driver)
    # input('Press enter to exit')


args = parse_arguments()
main(args)