from main import autobingo
from selenium import webdriver

url = 'https://bingobaker.com/#64c998520e68afc5'

driver = webdriver.Chrome()

bingo = autobingo(driver, url=url )

bingo.mark_spots()