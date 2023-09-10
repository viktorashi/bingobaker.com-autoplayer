from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from utils import (
    waitElement,
    note_card,
    check_bingos_and_write_to_output,
    get_card_details,
    update_config_one_attr,
)

# do enums idk


class autobingo:
    def __init__(
        self,
        driver: webdriver = "",
        url: str = "",
        cards_path="cards.txt",
        input_path="input.txt",
        output_path="output.json",
        gamemode: str = "normal",
        size: int = 5,
        reverse: bool = False,
        start: int = 0,
        free_space: str = "no credit",
        free_space_in_middle: int = 1,
    ) -> None:
        """
        driver : selenium.webdriver
        url : string of the bingomaker.com generator url
        cards_location : where the cards links will be stored
        input_phrases : where the input phrases to search for will be stored
        output_path : where the bingo'ed cards' links will be stores [will be automatically created if not provided]
        size must be odd
        """
        # turn input phrases file path into list of strings

        input_phrases: [str]
        with open(input_path) as f:
            input_phrases = f.read().splitlines()

        self.input_phrases = input_phrases
        self.free_space_in_middle = free_space_in_middle
        self.free_space = free_space
        self.reverse = reverse
        self.gamemode = gamemode
        self.driver = driver
        self.url = url
        self.input_path = input_path
        self.output_path = output_path
        self.cards_path = cards_path

        if self.reverse:
            cards.reverse()
        if start > 0:
            cards = cards[start:]

        if gamemode == "3in6":
            self.size = 6
        else:
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
                # check the free space in the middle
                elems = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_all_elements_located(
                        (By.CLASS_NAME, "bingo-card-svg g g")
                    )
                )
                from math import sqrt

                # automatically set the size of the card
                self.size = int(sqrt(len(elems)))
                update_config_one_attr("size", self.size)

                # this will be done in the mark function, and also the mark middle function doesn't really have a purpose anymore
                # click_middle(elems, self.size, self)
                card_details = get_card_details(self, elems)
                note_card(self, card_details)
            except TimeoutError:
                print(TimeoutError)

    def check_bingo_of_all_cards(self) -> None:
        """
        checks bingo for all cards in the cards.txt file
        """
        check_bingos_and_write_to_output(self)
