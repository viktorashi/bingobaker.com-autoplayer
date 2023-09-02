from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
from utils import (
    waitElement,
    writeTheCards,
    clear_card,
    find_words_click_and_return_num_of_found,
    check_bingo_and_write_to_output,
    click_middle,
)

# do enums


class autobingo:
    def __init__(
        self,
        driver: webdriver,
        url: str = "",
        cards_path="cards.txt",
        input_path="input.txt",
        output_path="output.txt",
        timeout: int = 0.6,
        type: str = "normal",
        size: int = 5,
        reverse: bool = False,
    ) -> None:
        if size % 2 == 0:
            raise Exception("size must be odd")
        """
        driver : selenium.webdriver
        url : string of the bingomaker.com generator url
        cards_location : where the cards links will be stored
        input_phrases : where the input phrases to search for will be stored
        output_path : where the bingo'ed cards' links will be stores [will be automatically created if not provided]
        size must be odd
        """
        # turn input phrases file path into list of strings

        phrases: [str]
        with open(input_path) as f:
            phrases = f.read().splitlines()

        cards: [str]
        with open(cards_path, "r+") as f:
            cards = f.read().splitlines()

        input_phrases: list[str]
        with open(input_path) as f:
            input_phrases = f.read().splitlines()

        self.reverse = reverse
        self.type = type
        self.input_phrases = input_phrases
        if self.reverse:
            cards.reverse()
        self.cards: [str] = cards
        self.input_path: [str] = phrases
        self.driver = driver
        self.url = url
        self.output_path = output_path
        self.cards_path = cards_path
        self.timeout = timeout
        self.size = size

    def createCards(self, num: int) -> None:
        """
        creates num cards and writes their links to the cards.txt file
        """
        for i in range(num):
            try:
                # go to the website
                self.driver.get(self.url)
                # create card
                waitElement(self, "/html/body/div[1]/div/form/button").click()
                # "OK" the rules
                waitElement(self, "/html/body/div[1]/p[2]/button").click()
                # check the free space in the middle (13th element)
                elems = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_all_elements_located(
                        (By.CLASS_NAME, "bingo-card-svg g g")
                    )
                )
                cnt = 0
                click_middle(elems, self.size, self)
                writeTheCards(self, str(self.driver.current_url))
            except TimeoutError:
                print(TimeoutError)

    def mark_spots_list(self, input_phrases: list[str]) -> None:
        """'
        input_phrases : list of strings that will be searched for in the bingo card
        """
        try:
            # obtains the cards links

            # for each card, find word from marking and check if, and if found check to see if that card has  a bingo, if yes report it to the logs along wit that card's link and print, continue on with the next card and go on
            for cardURL in self.cards:
                self.driver.get(cardURL)
                found = find_words_click_and_return_num_of_found(self, input_phrases)
                if found and check_bingo_and_write_to_output(self):
                    print(
                        "CONGRATS YO YOU GOT A BINGOO!!!, check the output file for the link"
                    )
        except TimeoutError:
            print(TimeoutError)

    def mark_spots_str(self, input_phrases: str) -> None:
        """'
        input_phrases : file containing the list of strings that will be searched for in the bingo card
        """
        try:
            # obtains the cards links

            # for each card, find word from marking and check if, and if found check to see if that card has  a bingo, if yes report it to the logs along wit that card's link and print, continue on with the next card and go on
            # get the input phrases as list from the file

            with open(input_phrases) as f:
                input_phrases = f.read().splitlines()

            print(input_phrases)

            for cardURL in self.cards:
                self.driver.get(cardURL)
                found = find_words_click_and_return_num_of_found(self, input_phrases)
                if found and check_bingo_and_write_to_output(self):
                    print(
                        "CONGRATS YO YOU GOT A BINGOO!!!, check the output file for the link"
                    )
        except TimeoutError:
            print(TimeoutError)

    def mark_spots(self) -> None:
        """'
        default for no file or list of words, uses the default input.txt file specified in the constructor
        """
        try:
            # for each card, find word from marking and check if, and if found check to see if that card has  a bingo, if yes report it to the logs along wit that card's link and print, continue on with the next card and go on
            # get the input phrases as list from the file
            for cardURL in self.cards:
                self.driver.get(cardURL)
                found = find_words_click_and_return_num_of_found(
                    self, self.input_phrases
                )
                if found and check_bingo_and_write_to_output(self):
                    print(
                        "CONGRATS YO YOU GOT A BINGOO!!!, check the output file for the link"
                    )
        except TimeoutError:
            print(TimeoutError)

    def clear_all_cards(self) -> None:
        """
        clears all the cards from the cards.txt file
        """
        for cardURL in self.cards:
            self.driver.get(cardURL)
            clear_card(self)

    def check_bingo_of_all_cards(self) -> None:
        """
        checks bingo for all cards in the cards.txt file
        """
        for cardURL in self.cards:
            self.driver.get(cardURL)
            check_bingo_and_write_to_output(self)

    def mark_all_middle_spots(self) -> None:
        for cardURL in self.cards:
            try:
                # go to the website
                self.driver.get(cardURL)
                # check the free space in the middle (13th element)
                elems = WebDriverWait(self.driver, 50).until(
                    EC.visibility_of_all_elements_located(
                        (By.CLASS_NAME, "bingo-card-svg g g")
                    )
                )
                click_middle(elems, self.size, self)
                writeTheCards(self, str(self.driver.current_url))
            except TimeoutError:
                print(TimeoutError)
