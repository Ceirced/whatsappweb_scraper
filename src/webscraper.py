from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

driver.get('https://www.google.com/')
print('title: %s' % driver.title)
driver.save_screenshot('/app/data/screenie3.png')
driver.quit()
print('done')
