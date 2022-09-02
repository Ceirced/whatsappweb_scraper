from selenium import webdriver
from selenium.webdriver.chrome.options import Options





options = webdriver.ChromeOptions() 
options.add_argument("user-data-dir=/home/cederic/.mozilla/firefox/e5vg9le0.default")

driver = webdriver.Firefox()
driver.get('https://web.whatsapp.com')

print(f'{driver.title}')