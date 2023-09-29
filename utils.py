import requests, re
from time import sleep


def get_text_squares(self, squares) -> [[str]]:
    # initialize 2d array of empty strings
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
    soup = BeautifulSoup(html_code, "html.parser")
    lines = []
    # \d stand for digit, any number of them
    rect = soup.findAll(
        "rect", {"data-row": re.compile(r"\d*"), "data-col": re.compile(r"\d*")}
    )
    if rect:
        for elem in rect:
            # delete first 2 chars
            elem["aria-label"] = elem["aria-label"][2:]
            # delete newlines and replace with spaces
            elem["aria-label"] = elem["aria-label"].replace("\n", " ")
            line_data = {
                "row": int(elem["data-row"]),
                "col": int(elem["data-col"]),
                "label": elem["aria-label"],
            }
            lines.append(line_data)

    if cnt == 0:
        update_card_size(self, rect)
        get_and_set_bingo_id(html_code)
    squares = get_text_squares(self, lines)
    if cnt == 0:
        update_if_free_space_in_middle(self, squares)
    return {"url": url, "squares": squares}


def get_squares_completion(self, card: dict) -> [[bool]]:
    """
    returns the squares of the card that are checked in a 2d bool array
    adds the completion 2d matrix value to the card for it to be printed to output
    """
    squares_completion: [[bool]] = [
        [0 for _ in range(self.size)] for _ in range(self.size)
    ]
    # have to search for the free space, it won't neccesarilly be in the middle
    if self.size % 2 == 0 or not self.free_space_in_middle:
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
                if input_phrase in card["squares"][i][j].lower():
                    squares_completion[i][j] = 1
                    break

    card["completion"] = squares_completion
    return squares_completion


def check_bingo_row_collumn_diagonal(size, squares: [[bool]]) -> bool:
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


def check_blackout(size, squares: [[bool]]) -> bool:
    """
    full card
    """
    # check if all squares are filled
    for i in range(size):
        if sum(squares[i]) != size:
            return False
    return True


def check_peen(size, squares: [[bool]]) -> bool:
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
    return sum == 2 * size - 1


def check_3_in_6(size, squares: [[bool]]) -> bool:
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


def check_loser(size, squares: [[bool]]) -> bool:
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
    return cnt == 2 * size - 1


def check_plus(size, squares: [[bool]]) -> bool:
    """
    shape of a +
    """
    # from math import ceil
    cnt: int = 0
    for i in range(size):
        if squares[i][size // 2]:
            cnt += 1
        if squares[size // 2][i]:
            cnt += 1
    return cnt == (2 * size)


def check_4_corners(size, squares: [[bool]]) -> bool:
    """
    4 corners
    """
    return (
        squares[0][0]
        and squares[0][size - 1]
        and squares[size - 1][0]
        and squares[size - 1][size - 1]
    )


def check_x(size, squares: [[bool]]) -> bool:
    """
    shape of an X
    """
    # check first collumn and last row
    cnt: int = 0
    for i in range(size):
        if squares[i][i]:
            cnt += 1
        if squares[size - 1 - i][i]:
            cnt += 1
    return cnt == 2 * size - 1


def check_bingos_and_write_to_output(self) -> None:
    from typing import Callable

    check_bingo: Callable[[any], bool]
    # always exclude the freespot
    min_required: int
    match self.gamemode.lower():
        case "normal":
            check_bingo = check_bingo_row_collumn_diagonal
            min_required = self.size - 1
        case "blackout":
            check_bingo = check_blackout
            min_required = self.size**2 - 1
        case "peen":
            check_bingo = check_peen
            min_required = self.size * 2 - 2
        case "3in6":
            check_bingo = check_3_in_6
            min_required = 9
        case "loser":
            check_bingo = check_loser
            min_required = self.size * 2 - 2
        case "4corners":
            check_bingo = check_4_corners
            min_required = 4
        case "x":
            check_bingo = check_x
            min_required = self.size * 2 - 2
        case "plus":
            check_bingo = check_plus
            min_required = self.size * 2 - 2
    # if the first one doesn't have it in the middle, change the settings to not look for it in the middle

    if len(self.input_phrases) < min_required:
        raise Exception(
            f"Minnimum number of {min_required} words for {self.gamemode} bingo gamemode of size {self.size} by {self.size} not reached!!!!, only got {len(self.input_phrases)}"
        )

    cards: [str] = read_cards_file(self)

    if self.reverse:
        cards.reverse()
    if self.start > 0:
        cards = cards[self.start :]

    self.cards = cards
    print(f"Checking through {len(cards)} cards....")

    # split the cards into chunnks of self.num_of_threads and check them in parallel, joining them later, run the check_part_of_cards function on each chunk

    leng = len(self.cards)
    cards_chunks = [
        self.cards[i : i + leng // self.num_of_threads]
        for i in range(0, leng, leng // self.num_of_threads)
    ]
    import threading

    winning_cards: [dict] = []
    threads = []
    global lock
    lock = threading.Lock()
    for chunk in cards_chunks:
        t = threading.Thread(
            target=check_part_of_cards, args=(self, chunk, check_bingo, winning_cards)
        )
        # t.daemon = True
        threads.append(t)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    if len(winning_cards) > 0:
        previous_wins = read_from_output(self)
        mark_winning_cards(self, winning_cards)
        new_wins = []
        if not previous_wins == []:
            previous_urls = [card["url"] for card in previous_wins]
            new_wins = [
                card for card in winning_cards if card["url"] not in previous_urls
            ]
            new_wins.extend(previous_wins)
            write_to_output(self, new_wins)
        else:
            write_to_output(self, winning_cards)
    else:
        print("Ain't found none sowyy 😭")


def check_part_of_cards(
    self, cards: [dict], check_bingo_function, winning_cards
) -> [dict]:
    for card in cards:
        # the following will add new attribute to card dict
        if check_bingo_function(self.size, get_squares_completion(self, card)):
            # for better performance when multithreading
            with lock:
                print(
                    "CONGRATS YOOO YOU GOT A BINGOO, check the output file for details"
                )
                # last 6 charracters of the link
                card["key"] = f'!bingowin #{ card["url"][-6:]}'

                print(card["url"])
                print(card["key"])
                for row in card["completion"]:
                    print(row)
            # try to make this work when multithreading
            # mark_bingo(self, card)
            del card["squares"]

            winning_cards.append(card)
            # currently only plays sound and works for macos but imma try to change it si maybe i also contribute to playsound library on github with python 10+ support
            # playsound()


def mark_winning_cards(self, winning_cards: [dict]) -> None:
    for card in winning_cards:
        mark_bingo(self, card)


def mark_bingo(self, card: dict) -> None:
    """
    make self.size no. of threads and mark each square, use the bingo_id from self.bingo_id
    edit: no need for multithreading inside this function, but the one wrapping this
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


def mark(session: str, bingo_id: str, indexes: [int]):
    """
    session is the code for the current card
    bingoid is the code for the generator link
    both of these reffer to the charracters after the /play/ or # in the url
    """

    import asyncio, websockets
    from string import Template

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
    return url.replace("#", "/play/")


def update_config(options: dict):
    with open("bingoconfig.json", "w+") as f:
        f.write(json.dumps(options))


def read_cards_file(self) -> [dict]:
    try:
        with open(self.cards_path, "r") as f:
            lines = f.readlines()
            json_lines = []
            for line in lines:
                try:
                    line = json.loads(line)
                except:
                    continue
                json_lines.append(line)
            return json_lines
    except:
        raise Exception("nah, you aint got no cards/ the file")


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
    with open(self.input_path) as f_in:
        lines = (line.rstrip() for line in f_in)  # All lines including the blank ones
        lines = list(line for line in lines if line)  # Non-blank lines
        if lines == []:
            raise ValueError(f"input file {self.input_path} is empty")
        return lines


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


def update_card_size(self, regexMatch) -> None:
    from math import sqrt

    if not self.gamemode == "3in6":
        # automatically set the size of the card
        self.size = int(sqrt(len(regexMatch)))
        update_config_one_attr("size", self.size)
        print("size of card updated to", self.size)


def update_if_free_space_in_middle(self, squares):
    if self.size % 2 == 1:
        from math import ceil

        # if the first one doesn't have it in the middle, change the settings to not look for it in the middle
        mid = ceil(self.size / 2) - 1
        free_space_in_mid = self.free_space.lower() in squares[mid][mid].lower()
        update_config_one_attr("free_space_in_middle", free_space_in_mid)
        print("free space in middle updated to", free_space_in_mid)
    else:
        update_config_one_attr("free_space_in_middle", False)
        print("free space in middle updated to", False)


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
    try:
        response = requests.post(url)
        response.raise_for_status()  # Check if the request was successful
        pattern = r'<meta property="og:url" content="([^"]+)"'
        matches = re.findall(pattern, response.text)
        if matches:
            return matches[0]
        else:
            print("Error getting Session key, retring....")
            generate_card(url)
            return
    except:
        print(f"Temporary Unavailability for {url}  Retrying...")

        sleep(1)
        generate_card(url)
        return


def generate_and_return_details(self, cnt=1) -> dict:
    """
    generates card, and looks into it to see details
    """
    url = generate_card(self.url)
    # less cpu intensive to not log it
    # print(url)
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
