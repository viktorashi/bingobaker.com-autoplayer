import requests, re


def get_text_squares(self, squares) -> [[str]]:
    phrases: [[str]] = [["" for _ in range(self.size)] for _ in range(self.size)]
    for square in squares:
        phrases[square["row"]][square["col"]] = square["label"]
    return phrases


def get_and_set_bingo_id(html_code) -> None:
    pattern = r'<script>\s*JS_PAGE = "\w+";\s*STATE = BigInt\("\d+"\);\s*SESSION_KEY = \'[\d\w]+\';\s*SEED = \'\d+\';\s*BINGO_ID = \'([^\"]+)\';\s*EDITED_ON = \'.*\'\s*</script>'

    matches = re.findall(pattern, html_code)
    if matches:
        print("bingo_id:", matches[0])
        update_config_one_attr("bingo_id", matches[0])


def get_card_details(self, url, cnt) -> dict:
    """
    returns a dictionary of the url of the card and a 2d array of the phrases squares of the card
    also sets the bingo_id of the game
    """
    from bs4 import BeautifulSoup

    response = requests.get(url)
    html_code = response.text
    if cnt == 0:
        get_and_set_bingo_id(html_code)
    soup = BeautifulSoup(html_code, "html.parser")

    lines = []
    for i in range(5):
        for j in range(5):
            rect = soup.find("rect", {"data-row": str(i), "data-col": str(j)})
            if rect:
                # delete first 2 chars
                rect["aria-label"] = rect["aria-label"][2:]
                # delete newlines and replace with spaces
                rect["aria-label"] = rect["aria-label"].replace("\n", " ")
                line_data = {"row": i, "col": j, "label": rect["aria-label"]}
                lines.append(line_data)

    return {"url": url, "squares": get_text_squares(self, lines)}


def get_squares_completion(self, card: dict) -> [[bool]]:
    """
    returns the squares of the card that are checked in a 2d bool array
    adds the completion 2d matrix value to the card for it to be printed to output
    """
    squares_completion: [[bool]] = [[0 for _ in range(5)] for _ in range(5)]
    # have to search for the free space, it won't neccesarilly be in the middle
    if self.size % 2 == 0 or (self.free_space_in_middle == 0):
        self.input_phrases.append(self.free_space)
    else:
        # or, in if it is odd or in the middle, just check that middle
        from math import ceil

        mid = ceil(self.size / 2) - 1
        # i forgor its indexed from 0 💀
        squares_completion[mid][mid] = 1
    for i in range(self.size):
        for j in range(self.size):
            for input_phrase in self.input_phrases:
                if input_phrase.lower() in card["squares"][i][j].lower():
                    squares_completion[i][j] = 1
                    break

    card["completion"] = squares_completion
    return squares_completion


def check_bingo_row_collumn_diagonal(size, squares) -> bool:
    """
    regular ass bingo
    """
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
    """
    full card
    """
    # check if all squares are filled
    for i in range(size):
        if sum(squares[i]) != size:
            return False
    return True


def check_peen(size, squares) -> bool:
    """
    shape of peen:
    """
    # check middle collumn and bottom row
    for i in range(size):
        sum = 0
        if squares[i][size // 2] == 1:
            sum += 1
        if squares[size - 1][i] == 1:
            sum += 1
    if sum == 2 * size - 1:
        return True


def check_3_in_6(size, squares) -> bool:
    """
    3x3 squares insode 6x6 grid
    """
    import numpy as np

    arr = np.array(squares)
    # check for any 3x3 squares of only true
    for i in range(size - 2):
        for j in range(size - 2):
            if np.all(arr[i : i + 3, j : j + 3]):
                return True
    return False


def check_loser(size, squares) -> bool:
    """
    shape of an L on her forehead
    """
    # check first collumn and last row
    cnt: int = 0
    for i in range(size):
        if squares[i][0]:
            cnt += 1
        if squares[size - 1][i]:
            cnt += 1
    if cnt == 2 * size - 1:
        return True
    return False


def check_bingos_and_write_to_output(self) -> None:
    from typing import Callable

    check_bingo: Callable[[any], bool]

    match self.gamemode:
        case "normal":
            check_bingo = check_bingo_row_collumn_diagonal
        case "blackout":
            check_bingo = check_blackout
        case "peen":
            check_bingo = check_peen
        case "3in6":
            check_bingo = check_3_in_6
        case "loser":
            check_bingo = check_loser

    cards: [dict] = read_cards_file(self)

    # if the first one doesn't have it in the middle, change the settings to not look for it in the middle
    from math import ceil

    winning_cards: [dict] = []

    for card in cards:
        # the following will add new attribute to card dict
        if check_bingo(self.size, get_squares_completion(self, card)):
            # for better conciseness and readability
            print("CONGRATS YOOO YOU GOT A BINGOO, check the output file for details")
            # last 6 charracters of the link
            card["key"] = f'!bingowin #{ card["url"][-6:]}'

            print(card["url"])
            print(card["key"])
            for row in card["completion"]:
                print(row)
            del card["squares"]
            winning_cards.append(card)
            # currently only plays sound and works for macos but imma try to change it si maybe i also contribute to playsound library on github with python 10+ support
            # playsound()
    if len(winning_cards) > 0:
        mark_winning_cards(self, winning_cards)
        final_wins = winning_cards
        previous_wins = read_from_output(self)
        if len(previous_wins) > 0:
            previous_urls = [card["url"] for card in previous_wins]
            new_wins = [
                card for card in winning_cards if card["url"] not in previous_urls
            ]
            new_wins.extend(previous_wins)
            final_wins = new_wins
        write_to_output(self, final_wins)


def mark_winning_cards(self, winning_cards: [dict]) -> None:
    for card in winning_cards:
        mark_bingo(self, card)


def mark_bingo(self, card: dict) -> None:
    """
    make self.size no. of threads and mark each square, use the bingo_id from self.bingo_id
    """
    pass
    session = card["url"].split("/")[-1]
    bingo_id = self.bingo_id
    indexes: [int] = []
    for i in range(self.size):
        for j in range(self.size):
            if card["completion"][i][j]:
                indexes.append(i * self.size + j)
    mark(session, bingo_id, indexes)


import asyncio, websockets
from string import Template


def mark(session: str, bingo_id: str, indexes: [int]):
    """
    session is the code for the current card
    bingoid is the code for the generator link
    both of these reffer to the charracters after the /play/ or # in the url
    """

    async def send_message():
        async with websockets.connect(
            f"wss://bingobaker.com/ws?type=handshake&bingo_id={bingo_id}&session_key={session}"
        ) as websocket:
            for index in indexes:
                message = Template(
                    '{"index": $index, "is_checked": 1, "type": "set_check", "bingo_id": "$bingo_id", "session_key": "$session_key"}'
                )
                message = message.substitute(
                    index=index, bingo_id=bingo_id, session_key=session
                )
                await websocket.send(message)

    asyncio.get_event_loop().run_until_complete(send_message())


import json


def format_link(url):
    return url.replace("#", "play/")


def update_config(options: dict):
    with open("bingoconfig.json", "w+") as f:
        f.write(json.dumps(options))


def read_cards_file(self) -> [dict]:
    with open(self.cards_path, "r") as f:
        return [json.loads(line) for line in f.readlines()]


def note_card(self, card: dict) -> None:
    """
    writes the link to the cards.txt file
    """
    card["url"] = format_link(card["url"])
    with open(self.cards_path, "a+") as f:
        f.write(json.dumps(card))
        f.write("\n")


def read_from_config() -> dict:
    try:
        with open("bingoconfig.json", "r") as f:
            return json.loads(f.read())
    except:
        return {}


def read_from_input(self) -> [str]:
    with open(self.input_path) as f:
        input_phrases = f.read().splitlines()
        if input_phrases == []:
            raise ValueError("input file is empty")
        return input_phrases


def write_to_output(self, cards: [dict]) -> None:
    with open(self.output_path, "w+") as f:
        f.write(json.dumps(cards))


def read_from_output(self) -> [dict]:
    try:
        with open(self.output_path, "r") as f:
            return json.loads(f.read())
    except:
        return []


def update_config_one_attr(attr: str, value: any) -> None:
    options = read_from_config()
    options[attr] = value
    update_config(options)


def update_card_size(self, card) -> None:
    if not self.gamemode == "3in6":
        # automatically set the size of the card
        self.size = len(card["squares"][0])
        update_config_one_attr("size", self.size)
        print("size of card updated to", self.size)


def update_if_free_space_in_middle(self, card):
    if self.size % 2 == 1:
        from math import ceil

        # if the first one doesn't have it in the middle, change the settings to not look for it in the middle
        mid = ceil(self.size / 2) - 1
        if self.free_space.lower() in card["squares"][mid][mid].lower():
            print("free space found in middle of card, updating config")
            update_config_one_attr("free_space_in_middle", 1)
        else:
            print("WARNING: free space not found in middle of card, updating config")
            update_config_one_attr("free_space_in_middle", 0)


def generate_multiple_cards(self, num) -> None:
    for i in range(num):
        try:
            generate_and_return_details(self)
        except TimeoutError:
            print(TimeoutError)


def generate_card(url) -> str:
    """
    generates a card and returns its url in the good /play/ format
    """

    response = requests.post(url)
    pattern = r'<meta property="og:url" content="([^"]+)"'
    matches = re.findall(pattern, response.text)
    if matches:
        return matches[0]
    else:
        print("Error getting Session key")


def generate_and_return_details(self, cnt=1) -> dict:
    """
    generates card, and looks into it to see details
    """
    url = generate_card(self.url)
    print(url)
    card_details = get_card_details(self, url, cnt)
    note_card(self, card_details)
    return card_details


# def playsound():
#     import sounddevice
#     import soundfile

#     filename = "bruh.wav"
#     data, fs = soundfile.read(filename, dtype="float32")
#     sounddevice.play(data, fs)
#     status = sounddevice.wait()
