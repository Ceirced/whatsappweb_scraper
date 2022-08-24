from selenium import webdriver
import math


driver = webdriver.Firefox()

driver.get('https://web.whatsapp.com')

print(f'{driver.title}')