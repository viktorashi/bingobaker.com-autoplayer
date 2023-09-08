from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
from typing import Callable
from time import sleep


def waitElement(self, xpath: str) -> WebElement:
    return WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )


def waitElementSelector(self, selector: str) -> WebElement:
    return WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )


def writeTheCards(self, link: str) -> None:
    """
    writes the link to the cards.txt file
    """
    self.cards.append(link)
    with open(self.cards_path, "a") as f:
        f.write(link + "\n")


def clear_card(self) -> None:
    """
    clears the current card
    must be used at the viewport already on that specific card, so function must be used right after navigating to current page
    """
    # this checks for free space
    cnt = 0
    waitElement(self, "/html/body/div[3]/a").click()

    waitElement(self, "/html/body/div[3]/div/div[6]/a").click()

    # switch to alert and accept
    self.driver.switch_to.alert.accept()
    # switch back to default content

    self.driver.switch_to.default_content()

    # wait for the page to load
    # click on the free space
    waitElementSelector(
        self, "#svg > svg > g:nth-child(20) > g > text > tspan:nth-child(1)"
    ).click()

    """
    mai sunt cateva clickuri
    """
    print(f"cleared {str( self.driver.current_url)}")


def find_words_click_and_return_num_of_found(self, input_phrases: list[str]) -> int:
    """
    this must be run on the viewport that is already on that specific card, so function must be used right after navigating to current page

    input_phrases : list[str]
    """
    cnt = 0
    elems = WebDriverWait(self.driver, 10).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "bingo-card-svg g g"))
    )
    for elem in elems:
        # check if elem already clicked
        img = elem.find_element(By.TAG_NAME, "image")
        if img.get_dom_attribute("visibility") == "hidden":
            texts = elem.find_elements(By.TAG_NAME, "tspan")
            # transform list of strings by replacing \n with space and joining them
            texts = " ".join([text.text.replace("\n", " ") for text in texts])
            for phrase in input_phrases:
                if phrase.lower() in texts.lower():
                    sleep(self.timeout)
                    elem.click()
                    cnt += 1
    return cnt


def get_squares(self) -> [[bool]]:
    # must be used at the viewport already on that specific card, so function must be used right after finding new word on current page
    """
    returns the squares of the card that are checked in a 2d bool array
    """
    squares: [[bool]] = []
    elems = WebDriverWait(self.driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "image"))
    )
    cnt = 0
    row: [bool] = []
    for elem in elems:
        cnt += 1
        # XAPTHU SFANTTT
        # xpath = f"/html/body/div[2]/*[local-name() = 'svg']/*[local-name()='g'][{i*5 + j + 1}]/*[local-name()='g']/*[local-name()='image']"
        visibilty = elem.get_dom_attribute("visibility")

        # daca e gol gen '' sau daca apare visibilty visib;e atunci e shown si doar daca apare hidden e hidden bruh

        if visibilty == "visible" or visibilty == "":
            row.append(1)
        else:
            row.append(0)
        if cnt == self.size:
            squares.append(row)
            cnt = 0
            row = []
    return squares


def check_bingo_row_collumn_diagonal(size, squares) -> bool:
    # check bingo for elements in row, collumn or diagonal
    for i in range(size):
        if sum(squares[i]) == size:
            return True
        if sum([row[i] for row in squares]) == size:
            return True
        if sum([squares[i][i] for i in range(size)]) == size:
            return True
        if sum([squares[i][size - 1 - i] for i in range(size)]) == size:
            return True
    return False


def check_blackout(size, squares) -> bool:
    # check if all squares are filled
    for i in range(size):
        if sum(squares[i]) != size:
            return False
    return True


def check_peen(size, squares) -> bool:
    # check middle collumn and bottom row
    for i in range(size):
        sum = 0
        if squares[i][size // 2] == 1:
            sum += 1
        if squares[size - 1][i] == 1:
            sum += 1
    if sum == 2 * size - 2:
        return True


def check_3_in_6(size, squares) -> bool:
    import numpy as np

    arr = np.array(squares)
    # check for any 3x3 squares of only true
    for i in range(size - 2):
        for j in range(size - 2):
            if np.all(arr[i : i + 3, j : j + 3]):
                return True
    return False


def check_bingo_and_write_to_output(self) -> bool:
    # this assumes the viewport is already on that specific card, so function must be used right after finding new word on current page

    check_bigo: Callable[[any], bool]

    match self.type:
        case "normal":
            check_bingo = check_bingo_row_collumn_diagonal
        case "blackout":
            check_bingo = check_blackout
        case "peen":
            check_bingo = check_peen
        case "3in6":
            check_bingo = check_3_in_6

    if check_bingo(self.size, get_squares(self)):
        curr_url = str(self.driver.current_url)
        write_to_output(self, curr_url)
        # currently only works for macos but imma try to change it si maybe i also contribute to playsound library on github with python 10+ support
        # import os

        # os.system("afplay bruh.mp3")
        return True
    return False


def write_to_output(self, cardURL: str) -> None:
    with open(self.output_path, "a+") as f:
        f.write(cardURL + "\n")


def update_config(options: dict):
    with open("bingoconfig.json", "w+") as f:
        f.write(json.dumps(options))


def read_from_config() -> dict:
    with open("bingoconfig.json", "r") as f:
        return json.loads(f.read())


def click_middle(elems, size, self) -> None:
    # size must be odd for freespace to be in the center, else check where it is
    if size % 2 == 0:
        find_words_click_and_return_num_of_found(self, [self.free_space])
        return
    from math import floor, ceil

    # check if elem already clicked
    mid = (floor(size / 2) * size) + ceil(size / 2)
    # i forgor its indexed from 0 💀
    elem = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable(elems[mid - 1])
    )
    # elem = elems[mid - 1]
    img = elem.find_element(By.TAG_NAME, "image")
    # if it hasn't been clicked yet
    if img.get_dom_attribute("visibility") == "hidden":
        elem.click()
        # check_bingo_and_write_to_output(self)
