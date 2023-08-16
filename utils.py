from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class App:
    url = "https://bingobaker.com/#64c998520e68afc5"

    def __init__(self,driver) -> None:
        self.driver = driver            

    def waitElement(self,xpath):
        return WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, xpath)))

    def writeTheCards(self, link):
        with open("cards.txt", "a") as f:
            f.write(link + '\n')

    def create10Cards(self):
        for i in range(10):
            try:
                #go to the website
                self.driver.get(self.url)
                #create card
                self.waitElement("/html/body/div[1]/div/form/button").click()
                #"OK" the rules
                self.waitElement("/html/body/div[1]/p[2]/button").click()
                self.writeTheCards(str(self.driver.current_url))
            except TimeoutError:
                print(TimeoutError)


