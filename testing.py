from selenium import webdriver
from utils import BingoAutomator

url  = "https://bingobaker.com/#64c998520e68afc5"

driver = webdriver.Safari()

a=  BingoAutomator(driver, url)
a.check_bingo_of_all_cards()

