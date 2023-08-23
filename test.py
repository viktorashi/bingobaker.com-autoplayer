from main import autobingo
from selenium import webdriver

url = "https://bingobaker.com/#64c998520e68afc5"

driver = webdriver.Edge()

bingo = autobingo(driver, url=url, timeout=0.47)

bingo.createCards(100)
# bingo.mark_spots()
