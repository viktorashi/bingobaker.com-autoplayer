from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from main import autobingo
from typing import Callable
from time import sleep


def waitElement(self, xpath: str) -> WebElement:
    return WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
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
    waitElement(self, "/html/body/div[3]/a")
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


def check_bingo_row_collumn_diagonal(self) -> bool:
    # must be used at the viewport already on that specific card, so function must be used right after finding new word on current page
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
        if cnt == 5:
            squares.append(row)
            cnt = 0
            row = []

    # check bingo for elements in row, collumn or diagonal
    for i in range(5):
        if sum(squares[i]) == 5:
            return True
        if sum([row[i] for row in squares]) == 5:
            return True
        if sum([squares[i][i] for i in range(5)]) == 5:
            return True
        if sum([squares[i][4 - i] for i in range(5)]) == 5:
            return True
    return False


def check_full_bingo(self) -> bool:
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
        if cnt == 5:
            squares.append(row)
            cnt = 0
            row = []

    # check if all squares are filled
    for i in range(5):
        if sum(squares[i]) != 5:
            return False
    return True


def check_bingo_and_write_to_output(self) -> bool:
    # this assumes the viewport is already on that specific card, so function must be used right after finding new word on current page

    check_bigo: Callable[[autobingo], bool]
    match self.type:
        case "normal":
            check_bingo = check_bingo_row_collumn_diagonal

    if check_bingo(self):
        curr_url = str(self.driver.current_url)
        write_to_output(self, curr_url)
        return True
    return False


def write_to_output(self, cardURL: str) -> None:
    with open(self.output_path, "a") as f:
        f.write(cardURL + "\n")


def update_config():
    pass
