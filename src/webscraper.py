from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import os

USERAGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
print("test")

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument(f'--user-agent={USERAGENT}')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

driver.get('https://open.spotify.com/artist/1LDYdZ0TAovDFvPtQLm6e9')
print('title: %s' % driver.title)

if driver.save_screenshot('/home/user/app/data/screenie3.png'):
    print('screenshot saved')
else:
    print('screenshot failed')
driver.quit()
print('done')