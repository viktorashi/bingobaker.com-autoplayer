from selenium import webdriver
from utils import App


driver = webdriver.Edge()
a=  App(driver)


try:
    #obtains the cards links
    cards =[]
    with open("cards.txt") as f:
        cards = f.read().splitlines()

    driver.get(cards[0])

    a.waitElement("/html/body/div[2]/svg/g[1]/g/image").click()
    
    # for i in range(25):
    #     #look to see if every square is checked or not
    #     xpath = f'/html/body/div[2]/svg/g[{i+1}]/g/image'
    #     # print(value)
    #     print(xpath)
except TimeoutError:
    print(TimeoutError)