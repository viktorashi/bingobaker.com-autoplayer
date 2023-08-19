from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from typing import overload
from time import sleep
class BingoAutomator:
    def __init__(self, driver :webdriver , url : str , cards_location = "cards.txt", input_phrases = "input.txt", output_path = "output.txt", timeout :int = 0.44) -> None:
        '''
        driver : selenium.webdriver
        url : string of the bingomaker.com generator url
        cards_location : where the cards links will be stored
        input_phrases : where the input phrases to search for will be stored
        output_path : where the bingo'ed cards' links will be stores [will be automatically created if not provided]
        '''
        #turn input phrases file path into list of strings
        
        with open(input_phrases) as f:
            input_phrases = f.read().splitlines()
                
        self.input_phrases : [str] = input_phrases

        self.driver = driver            
        self.url = url
        self.output_path = output_path
        self.cards_location = cards_location
        self.timeout = timeout

    def waitElement(self,xpath : str) -> WebElement :
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))

    def writeTheCards(self, link :str) ->None:
        '''
        writes the link to the cards.txt file
        '''
        with open(self.cards_location, "a") as f:
            f.write(link + '\n')

    def createCards(self, num : int) -> None:
        '''
        creates num cards and writes their links to the cards.txt file
        '''
        for i in range(num):
            try:
                #go to the website
                self.driver.get(self.url)
                #create card
                self.waitElement("/html/body/div[1]/div/form/button").click()
                #"OK" the rules
                self.waitElement("/html/body/div[1]/p[2]/button").click()
                #check the free space in the middle (13th element)
                elems = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "bingo-card-svg g g")))
                cnt  =0 
                for elem in elems:
                    cnt +=1
                    if cnt == 13:
                        sleep(self.timeout)
                        elem.click()
                self.writeTheCards(str(self.driver.current_url))
            except TimeoutError:
                print(TimeoutError)

    
    def mark_spots_list(self, input_phrases : list[str]) -> None:
        ''''
        input_phrases : list of strings that will be searched for in the bingo card
        '''
        try:
            #obtains the cards links
            cards =[]
            with open(self.cards_location) as f:
                cards = f.read().splitlines()
            #for each card, find word from marking and check if, and if found check to see if that card has  a bingo, if yes report it to the logs along wit that card's link and print, continue on with the next card and go on 
            for cardURL in cards:
                self.driver.get(cardURL)
                found = self.find_words_click_and_return_num_of_found(input_phrases)
                if (found and self.check_bingo_and_write_to_output()):
                        print("CONGRATS YO YOU GOT A BINGOO!!!")
        except TimeoutError:
            print(TimeoutError)    
    
    
    def mark_spots_str(self, input_phrases : str) -> None:
        ''''
        input_phrases : file containing the list of strings that will be searched for in the bingo card
        '''
        try:
            #obtains the cards links
            cards =[]
            with open(self.cards_location) as f:
                cards = f.read().splitlines()
            #for each card, find word from marking and check if, and if found check to see if that card has  a bingo, if yes report it to the logs along wit that card's link and print, continue on with the next card and go on 
            #get the input phrases as list from the file

            with open(input_phrases) as f:
                input_phrases = f.read().splitlines()

            print(input_phrases)

            for cardURL in cards:
                self.driver.get(cardURL)
                found = self.find_words_click_and_return_num_of_found(input_phrases)
                if (found and self.check_bingo_and_write_to_output()):
                        print("CONGRATS YO YOU GOT A BINGOO!!!")
        except TimeoutError:
            print(TimeoutError)
    
    def mark_spots(self) -> None:
        ''''
        default for no file or list of words, uses the default input.txt file specified in the constructor
        '''
        try:
            #obtains the cards links
            cards =[]
            with open(self.cards_location) as f:
                cards = f.read().splitlines()
            #for each card, find word from marking and check if, and if found check to see if that card has  a bingo, if yes report it to the logs along wit that card's link and print, continue on with the next card and go on 
            #get the input phrases as list from the file
            
            for cardURL in cards:
                self.driver.get(cardURL)
                found = self.find_words_click_and_return_num_of_found(self.input_phrases)
                if (found and self.check_bingo_and_write_to_output()):
                        print("CONGRATS YO YOU GOT A BINGOO!!!")
        except TimeoutError:
            print(TimeoutError)


    def clear_card(self) -> None:
        '''
        clears the current card
        must be used at the viewport already on that specific card, so function must be used right after navigating to current page
        '''
        #this checks for free space
        cnt = 0
        elems = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "bingo-card-svg g g")))
        for elem in elems:
            cnt +=1
            #check if elem already clicked
            img = elem.find_element(By.TAG_NAME, "image")
            if cnt != 13 and img.get_dom_attribute("visibility") == "visible" or img.get_dom_attribute("visibility") == '':
                #idk just for safety
                sleep(self.timeout)
                elem.click()
        print(f"cleared {str( self.driver.current_url)}")
            
    def clear_all_cards(self) -> None:
        '''
        clears all the cards from the cards.txt file
        '''
        cards =[]
        with open(self.cards_location) as f:
            cards = f.read().splitlines()

        for cardURL in cards:
            self.driver.get(cardURL)
            self.clear_card()
        
    def find_words_click_and_return_num_of_found(self,input_phrases : list[str] ) -> int:
        '''
        this must be run on the viewport that is already on that specific card, so function must be used right after navigating to current page

        input_phrases : list[str] 
        '''
        cnt = 0
        elems = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "bingo-card-svg g g")))
        for elem in elems:
            #check if elem already clicked
            img = elem.find_element(By.TAG_NAME, "image")
            if img.get_dom_attribute("visibility") == "hidden":
                texts = elem.find_elements(By.TAG_NAME, "tspan")
            #transform list of strings by replacing \n with space and joining them
                texts = " ".join([text.text.replace("\n", " ") for text in texts])
                for phrase in input_phrases:
                    if phrase.lower() in texts.lower():
                        sleep(self.timeout)
                        elem.click()
                        cnt +=1
        return cnt

    def check_bingo(self) -> bool :
        #must be used at the viewport already on that specific card, so function must be used right after finding new word on current page
        squares : [[bool]] =[]
        elems = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "image")))
        cnt  =0 
        row : [bool] = []
        for elem in elems:
            cnt +=1
            #XAPTHU SFANTTT
            # xpath = f"/html/body/div[2]/*[local-name() = 'svg']/*[local-name()='g'][{i*5 + j + 1}]/*[local-name()='g']/*[local-name()='image']"
            visibilty = elem.get_dom_attribute("visibility")

            #daca e gol gen '' sau daca apare visibilty visib;e atunci e shown si doar daca apare hidden e hidden bruh

            if visibilty == "visible" or visibilty == '':
                row.append(1)
            else:
                row.append(0)
            if cnt==5:
                squares.append(row)
                cnt =0
                row =[]

        

        # check bingo for elements in row, collumn or diagonal
        for i in range(5):
            if sum(squares[i]) == 5:
                return True
            if sum([row[i] for row in squares]) == 5:
                return True
            if sum([squares[i][i] for i in range(5)]) == 5:
                return True
            if sum([squares[i][4-i] for i in range(5)]) == 5:
                return True
        return False
            
    def check_bingo_of_all_cards(self) -> None :
        '''
        checks bingo for all cards in the cards.txt file
        '''
        cards =[]
        with open(self.cards_location) as f:
            cards = f.read().splitlines()

        for cardURL in cards:
            self.driver.get(cardURL)
            self.check_bingo_and_write_to_output()
             
    def check_bingo_and_write_to_output(self) -> bool :
        #this assumes the viewport is already on that specific card, so function must be used right after finding new word on current page
        if self.check_bingo():
            curr_url = str( self.driver.current_url)
            self.write_to_output(curr_url)
            return True
        return False
        
    def write_to_output(self,cardURL : str ) -> None :
         with open(self.output_path, 'a') as f:
              f.write(cardURL + '\n')

#TODO  sa vezi sa fie bifat pe mijloc tot timpu ala, cand creezi cardu adica