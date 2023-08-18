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

    def mark_spots(self, words):
        try:
            #obtains the cards links
            cards =[]
            with open("cards.txt") as f:
                cards = f.read().splitlines()
            #for each card, find word from marking and check if, and if found check to see if that card has  a bingo, if yes report it to the logs along wit that card's link and print, continue on with the next card and go on 
            for cardURL in cards:
                self.driver.get(cardURL)
                found = self.find_words_click_and_return_num_of_found(words)
                if (found and self.check_bingo_and_write_to_output()):
                        print("CONGRATS YO YOU GOT A BINGOO!!!")
        except TimeoutError:
            print(TimeoutError)

#TODO: this whole thing lol
    def find_words_click_and_return_num_of_found(self,words):
        #this assumes the viewport is already on that specific card, so function must be used right after navigating to current page
        cnt  =0
        for word in words:
            #TODO: implement search word in page 
            #not sure if this works: n-am net bruh
            # elem =  self.driver.search_first(word)
            # if elem:
            #     elem.click()
            #     cnt+=1
            pass

        return cnt



    def check_bingo(self):
        #this assumes the viewport is already on that specific card, so function must be used right after finding new word on current page
        '''
        returns the current card's url if bingo is found, else returns None
        '''
        squares =[]
        for i in range(5):
            row = []
            for j in range(5):
                    #xapth pattern for each image that appears over a crossed out square
                    xpath = f'/html/body/div[2]/svg/g[{i*j+1}]/g/image'
                    visibility = self.waitElement(xpath).get_dom_attribute("visibility")
                    if visibility == "hidden":
                        row.append(0)
                    else:
                        row.append(1)
            squares.append(row)
            #check bingo for elements in row, collumn or diagonal
            for i in range(5):
                if sum(squares[i]) == 5:
                    return self.driver.current_url
                if sum([row[i] for row in squares]) == 5:
                    return self.driver.current_url
                if sum([squares[i][i] for i in range(5)]) == 5:
                    return self.driver.current_url
                if sum([squares[i][4-i] for i in range(5)]) == 5:
                    return self.driver.current_url
            return None
            
    def check_bingo_of_all_cards(self):
        cards =[]
        with open("cards.txt") as f:
            cards = f.read().splitlines()

        for cardURL in cards:
            self.driver.get(cardURL)
            self.check_bingo_and_write_to_output()
             
    def check_bingo_and_write_to_output(self):
        #this assumes the viewport is already on that specific card, so function must be used right after finding new word on current page
        url = self.check_bingo()
        if url:
            print(f"BRAVO MA AI BINGOO pe {url}")
            self.write_to_output(url)
        
    def write_to_output(self,cardURL):
         with open("output.txt", 'a') as f:
              f.write(cardURL)