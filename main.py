from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from utils import (
    check_bingos_and_write_to_output,
    read_cards_file,
    update_if_free_space_in_middle,
    create_card_return_card_details,
    init_driver,
)

# do enums idk


class autobingo:
    def __init__(
        self,
        driver: str = "chrome",
        cards_path="cards.txt",
        input_path="input.txt",
        url: str = "",
        output_path="output.json",
        gamemode: str = "normal",
        reverse: bool = False,
        start: int = 0,
        free_space: str = "no credit",
        headless: bool = True,
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
        # dont mention input_path or cards_path if you're using the generate function

        self.input_path = input_path
        self.cards_path = cards_path
        self.start = start
        self.free_space = free_space
        self.reverse = reverse
        self.gamemode = gamemode
        self.driver = driver
        self.url = url
        self.output_path = output_path
        self.headless = headless

        if gamemode == "3in6":
            self.size = 6

    def createCards(self, num: int) -> None:
        """
        creates num cards and writes their links to the cards.txt file
        """
        # check for the first card to update the details
        if self.url == "":
            raise ValueError("url not provided")
        init_driver(self)
        update_if_free_space_in_middle(self, create_card_return_card_details(self))
        for _ in range(1, num):
            try:
                create_card_return_card_details(self)
            except TimeoutError:
                print(TimeoutError)

    def check_bingo_of_all_cards(self) -> None:
        """
        checks bingo for all cards in the cards.txt file
        """
        # innit the reading and changing of the files
        input_phrases: [str]
        with open(self.input_path) as f:
            input_phrases = f.read().splitlines()

        if input_phrases == []:
            raise ValueError("input file is empty/ inexistent")

        self.input_phrases = input_phrases

        cards: [str] = read_cards_file(self)
        if self.reverse:
            cards.reverse()
        if self.start > 0:
            cards = cards[self.start :]
        self.cards = cards

        check_bingos_and_write_to_output(self)
