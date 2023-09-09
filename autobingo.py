# the command line tool version of AutoBingo
import argparse

"""
`
idei de cum sa fac comannd lineu 

e pe moduri: 
    - editconfig [defaultu daca nu e specificat]
    - generate
    - checkbingos
    - help 
    - mark
    - clear
"""
parser = argparse.ArgumentParser(
    description="Auto Bingo playing command line tool. Currently only being used for bingobaker.com",
    prog="autobingo",
    epilog="ion care how u use my code lol",
)

parser.add_argument(
    "mode",
    help="The mode to run the program in. [default: editconfig]",
    choices=["editconfig", "generate", "checkbingos", "mark", "clear", "markmid"],
    nargs="?",
)

parser.add_argument(
    "-d",
    "--driver",
    help="The web browser to use. [default: chrome] Recommended: chrome, edge",
    choices=["chrome", "edge", "firefox", "safari", "ie", "default"],
    type=str,
    dest="driver",
)
parser.add_argument(
    "-u",
    "--url",
    help="The link to the bingo card generator",
    type=str,
    dest="url",
)
parser.add_argument(
    "-cnt",
    "--count",
    help="Number of bingo cards to generate from the generator link",
    dest="count",
    type=int,
)
parser.add_argument(
    "-i",
    "--input",
    help="The file containing the keywords to search for on the bingo cards [default: input.txt] ",
    type=str,
    dest="input_path",
)
parser.add_argument(
    "-o",
    "--output",
    help="File to write the bingo'ed cards to [default: output.txt]",
    type=str,
    dest="output_path",
)
parser.add_argument(
    "-c",
    "--cards",
    help="The path you want the cards to be saved in",
    dest="cards_path",
    type=str,
)
parser.add_argument(
    "-t",
    "--timeout",
    help="Timeout in seconds for the webdriver to wait before clicking on each element to prevent malfunction [default : 0.2 ]",
    type=float,
)
parser.add_argument(
    "-gm",
    "--gamemode",
    help="The gamemode to play in. [default: normal] ",
    type=str,
    choices=["normal", "blackout", "peen", "3in6", "loser"],
    dest="type",
)
parser.add_argument(
    "-s",
    "--size",
    help="The size of the bingo card [default: 5 ] ",
    type=int,
    dest="size",
)
parser.add_argument(
    "-r",
    "--reverse",
    help="Reverse the bingo card order when reading from [cards.txt] [default False]",
    action="store_true",
    dest="reverse",
)
parser.add_argument(
    "-hdls",
    "--headless",
    help="Run the webdriver in headless mode (no interface for less VRAM consumption i think idk lol) [only possible for chrome, edge, firefox] [default False]",
    action="store_true",
    dest="headless",
)
parser.add_argument(
    "-strt",
    "--start",
    help="The index of the card to start doing anything from",
    type=int,
    dest="start",
)
parser.add_argument(
    "-fs",
    "--free-space",
    help="Name of the freespace to search for in the card [default: 'no credit']",
    type=str,
    dest="free_space",
)
parser.add_argument(
    "-fsm",
    "--free-space-middle",
    help="Whether to search for the freespace in the middle of the card [default: 1]",
    dest="free_space_in_middle",
    type=int,
)
# the rest of the defaults are in the autobingo class definition
parser.set_defaults(count=-1, mode="editconfig", driver="default", start=0)

# dict repr of the arguments, will need some cleaning up
args = vars(parser.parse_args())

options = {}


# Pentru fiecare argument, daca e default sau None o sa luam din bingoconfig.json valoarea lui, daca nu e acolo atunci lasi asa si nu adaugi nimic in options ca o sa ia optiunea default automat din clasa autobingo

from utils import update_config, read_from_config

file_config: dict

try:
    file_config = read_from_config()
except FileNotFoundError:
    file_config = {}


for arg in args:
    if (args[arg] == None) or (args[arg] == -1) or (args[arg] == "default"):
        # read from bingoconfig.json
        if arg in file_config:
            options[arg] = file_config[arg]
        else:
            match arg:
                case "driver":
                    options["driver"] = "chrome"
                case "count":
                    options["count"] = 10
                case _:
                    pass
        # if arg in bingoconfig.json: set it in options
        # else: check if:
        # arg == "mode": set it to "editconfig"
        # arg == "driver": set it to "chrome"
        # arg == "count" : set it to 10
        # else pass
    else:
        # because this is a default that we don't want to set in bingoconfig.json as it depends on the user's call of the program
        if not arg == "mode":
            options[arg] = args[arg]

if "gamemode" in options:
    if options["gamemode"] == "3in6":
        options["size"] = 6

update_config(options)

if args["mode"] == "editconfig":
    print("bingoconfig.json updated with the following options:")
    print(options)
    exit()

from selenium import webdriver

print("Options:")
for option in options:
    print(f"{option} : {options[option]}")


match options["driver"]:
    case "chrome":
        if options["headless"]:
            opts = webdriver.ChromeOptions()
            opts.add_argument("--headless=new")
            options["driver"] = webdriver.Chrome(options=opts)
        else:
            options["driver"] = webdriver.Chrome()
    case "edge":
        if options["headless"]:
            opts = webdriver.EdgeOptions()
            opts.add_argument("--headless=new")
            options["driver"] = webdriver.Edge(options=opts)
        else:
            options["driver"] = webdriver.Edge()
    case "firefox":
        if options["headless"]:
            opts = webdriver.FirefoxOptions()
            opts.add_argument("--headless=new")
            options["driver"] = webdriver.Firefox(options=opts)
        else:
            options["driver"] = webdriver.Firefox()
    case "safari":
        options["driver"] = webdriver.Safari()
    case "ie":
        options["driver"] = webdriver.Ie()
    case _:
        options["driver"] = webdriver.Chrome()
from main import autobingo

not_for_class = ["count", "headless"]
# preparing it for the autobingo class
input_options = {}


for option in options:
    if not (option in not_for_class):
        input_options[option] = options[option]

bingo = autobingo(**input_options)

match args["mode"]:
    case "generate":
        bingo.createCards(options["count"])
        print("Cards generated! Check the cards.txt file for the links")
    case "checkbingos":
        bingo.check_bingo_of_all_cards()
    case "mark":
        bingo.mark_spots()
    case "clear":
        bingo.clear_all_cards()
    case "markmid":
        bingo.mark_all_middle_spots()
