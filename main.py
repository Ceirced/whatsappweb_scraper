#!/usr/bin/env python3
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
import argparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import urllib.request
import os
from user import User
import pathlib
import matplotlib.pyplot as plt
from matplotlib.image import imread
from check_sync import (
    js_db_users_synced,
    json_db_status_synced,
    get_users_in_db,
    json_db_picture_synced,
)

DIRECTORY = pathlib.Path(__file__).parent.resolve()
PROFILE_PICTURES = f"{DIRECTORY}/profile_pictures"

# check if json file is synced with db
if not js_db_users_synced():
    print(
        "json user file is not synced with db,something is wrong, please run insert_users.py"
    )
    exit()

if not json_db_status_synced():
    print(
        "json status files are not synced with db, something is wrong, please run insert_status.py"
    )
    exit()

if not json_db_picture_synced():
    print(
        "json picture files are not synced with db, something is wrong, please run insert_pictures.py"
    )
    exit()


def parse_arguments():
    parser = argparse.ArgumentParser(description="Whatsapp Profile picture scraper")
    parser.add_argument(
        "-t",
        "--time",
        help="Time to wait for login in seconds",
        required=False,
        default=30,
    )
    parser.add_argument(
        "--head", help="Run with open browser window", action="store_true"
    )
    parser.add_argument(
        "-u", "--user", help="scrape specific user", nargs=1, required=False
    )
    parser.add_argument("-s", "--status", help="scrape statuses", action="store_true")
    return parser.parse_args()


def wait_for_login(driver, time: int):
    print(f"waiting for login for {time} seconds")
    try:
        WebDriverWait(driver, time).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]')
            )
        )
    except:
        print("Timeout while waiting for search box")
        print("trying to get the qr code")
        qr_code = getQRcode(driver)
        if qr_code:
            qr_code.screenshot(f"{DIRECTORY}/qr_code.png")
            print("saved qr code as qr_code.png")
            img = imread(f"{DIRECTORY}/qr_code.png")
            plt.imshow(img)
            plt.axis("off")
            print("showing qr code")
            plt.show()

        else:
            quit()
    print("login successful")


def getQRcode(driver):
    try:
        qr_code = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[1]/div/div/div[3]/div[1]/div/div/div[2]/div/canvas",
                )
            )
        )
    except:
        print("could not get qr code")
        return False
    return qr_code


def search_user(driver, name):
    clear_search(driver)
    searchBox = driver.find_element(
        "xpath", '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]'
    )
    searchBox.send_keys(name)
    searchBox.send_keys(Keys.ENTER)
    print(f"entered {name} in search box")


def clear_search(driver):
    searchBox = driver.find_element(
        "xpath", '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]'
    )
    searchBox.send_keys(Keys.CONTROL + "a")
    searchBox.send_keys(Keys.DELETE)


def NewPicture(driver, user):
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"//img[contains(@src, '{user.lastProfilePictureIdentifier()}')]",
                )
            )
        )
        return False
    except Exception as e:
        return True


def getStatus(driver, user, profile_section):
    """function to get status of user
    should only be called when profile was already klicked"""

    try:
        WebDriverWait(driver, 3).until(
            lambda x: profile_section.find_element(
                By.XPATH, "./div[2]/span/span"
            ).get_attribute("title")
            != ""
        )
    except Exception as e:
        print("could not get status text")
        return False

    try:
        # have to find a better way to wait for the status to load
        status = WebDriverWait(profile_section, 2).until(
            EC.presence_of_element_located((By.XPATH, "./div[2]/span/span"))
        )
    except Exception as e:
        print("could not get status")
        return False
    print(f"got status for {user.name}")

    # wait for text to appear in status

    try:
        return status.get_attribute("title")
    except Exception as e:
        print(e)
        print("could not get status text")
        return False


def main(args):
    changes = {}
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument(f"--user-data-dir={DIRECTORY}/User_Data")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3641.0 Safari/537.36"
    )
    if args.head:
        options.arguments.remove("--headless")

    driver = webdriver.Chrome(options=options)
    driver.get("https://web.whatsapp.com/")

    users = get_users_in_db()
    if args.user:
        users = [user for user in users if user == args.user[0]]
        if len(users) == 0:
            print(f"No user found with name {args.user[0]}")
            quit()

    wait_for_login(driver, int(args.time))
    image_url = ""
    for user in users:
        print(f'\n{"":~^50}\n')

        user = User(user)
        print(f"Getting profile picture for {user.name}")
        changes[user.name] = {}
        search_user(driver, user.name)
        # newChatSearch(driver, user)
        try:
            chat = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//span[contains(@title,'{user.name}')]")
                )
            )
            print(f"found chat with {user.name}")
        except Exception as e:
            print(e)
            print(f"No user found for {user.name}")
            continue

        if not args.status:
            if NewPicture(driver, user):
                print(f"New Picture for {user.name}")
            else:
                print(f"No new Picture for {user.name}")
                continue

        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable(chat))
            print(f"chat clickable for {user.name}")
        except:
            print(f"chat not clickable for {user.name}")
        counter = 0
        while counter < 5:
            try:
                chat.click()
                break
            except:
                print(f"could not open chat with {user.name}\ntrying again")
                counter += 1

                sleep(1)

        if counter == 5:
            print(f"could not open chat with {user.name} after 5 tries")
            continue

        try:
            main_section = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[@id="main"]'))
            )
        except Exception as e:
            print(e)
            print(f"could not find main section for {user.name}")
            continue

        try:
            header_name_element = WebDriverWait(main_section, 5).until(
                EC.element_to_be_clickable((By.XPATH, f".//header"))
            )
        except Exception as e:
            print(e)
            print(f"Profile not Clickable {user.name}")
            continue
        open_chat = header_name_element.text.split("\n")[0]
        if user.name != open_chat:
            print(f"Error: opened chat with {open_chat}")
            print(f"Header says: {header_name_element.text}")
            continue
        header_name_element.click()
        print(f"clicked profile for {user.name}")

        try:
            profile_section = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "section"))
            )
            print(f"profile section found")
        except Exception as e:
            print(e)
            print(f"could not find profile section for {user.name}")
            continue

        try:
            name_present = WebDriverWait(profile_section, 5).until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, "div"), user.name)
            )
            print(f"Name present in profile section for {user.name}")
            if not name_present:
                print(f"Name not present in profile section for {user.name}")
                continue

        except Exception as e:
            print(e)
            print(f"could not find first div in section for {user.name}")
            continue

        status = getStatus(driver, user, profile_section)
        if status:
            lastStatus = user.lastStatus()
            if lastStatus != status:
                print(f"old status: {lastStatus} new status: {status}")
                user.add_status(status)
                user.saveUserJson()
                changes[user.name]["status"] = status
            else:
                print(f"No new Status for {user.name}")
        try:
            profile_picture = profile_section.find_element(
                By.XPATH, "./div[1]/div[1]/div/img"
            )
        except:
            print(f"No profile picture for {user.name}")
            continue
        image_url = profile_picture.get_attribute("src")
        identifier = image_url.split("_n.jpg")[0].split("/")[-1]

        os.makedirs(user.userdir, exist_ok=True)

        image_name = f"{user.userdir}/{user.name}_{identifier}.jpg"
        if os.path.exists(image_name):
            print(f"profile picture for {user.name} already exists")
            continue
        urllib.request.urlretrieve(image_url, image_name)
        print(f"saved profile picture as {image_name}")
        user.addProfilePicture(identifier)
        user.saveUserJson()
        changes[user.name]["profile_picture"] = identifier
    return changes

    # input('Press enter to exit')


if __name__ == "__main__":
    args = parse_arguments()
    changes = main(args)

    print(f'\n{"":~^50}\n')

    if any(change != {} for change in changes.values()):
        print("Changes:")
        for user, change in changes.items():
            if change != {}:
                print(f"{user}: {change}")
    else:
        print("No Changes")
