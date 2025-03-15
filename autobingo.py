# the command line tool version of AutoBingo
import argparse

parser = argparse.ArgumentParser(
    description="Auto Bingo playing command line tool. Currently only being used for bingobaker.com",
    prog="autobingo",
    epilog="ion care how u use my code lol",
)

parser.add_argument(
    "mode",
    help="The mode to run the program in. [default: editconfig]",
    choices=["editconfig", "generate", "gen", "check"],
    nargs="?",
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
    "-gm",
    "--gamemode",
    help="The gamemode to play in. [default: normal] ",
    type=str,
    choices=[
        "normal",
        "blackout",
        "peen",
        "3in6",
        "loser",
        "4corners",
        "X",
        "x",
        "plus",
        "j",
    ],
    dest="gamemode",
)

parser.add_argument(
    "-r",
    "--reverse",
    help="(deprecated) Reverse the bingo card order when reading from [cards.txt] [default False]",
    action="store_true",
    dest="reverse",
)

parser.add_argument(
    "-strt",
    "--start",
    help="(deprecated) The index of the card to start doing anything from",
    type=int,
    dest="start",
)
parser.add_argument(
    "-fs",
    "--free-space",
    help="Name of the freespace to search for in the card [default: 'free space']",
    type=str,
    dest="free_space",
)
parser.add_argument(
    "-acc",
    "-accelleration",
    help="The number of threads to use for speeding up",
    type=int,
    dest="num_of_threads",
)

# the rest of the defaults are in the autobingo class definition
parser.set_defaults(count=-1, mode="editconfig")

# dict repr of the arguments, will need some cleaning up
args = vars(parser.parse_args())

# Pentru fiecare argument, daca e default sau None o sa luam din bingoconfig.json valoarea lui, daca nu e acolo
# atunci lasi asa si nu adaugi nimic in options ca o sa ia optiunea default automat din clasa autobingo.

# For each argument, if it's default or None we're going to take the value from bingoconfig.json,
# if it's not there then we leave it as is and don't add it to options because it's going to take the
# default value from the autobingo class

from utils import update_config, read_from_config, format_link

options = {}
file_config: dict = read_from_config()

# if not mentioned in the command line arguments, read from bingoconfig.json and it if it isn't there set the defaults
for arg in args:
    if (args[arg] == None) or (args[arg] == -1) or (args[arg] == "default"):
        # read from bingoconfig.json
        if arg in file_config:
            options[arg] = file_config[arg]
        else:
            match arg:
                case "count":
                    options["count"] = 100
                case _:
                    pass
    elif not (arg == "mode"):
        options[arg] = args[arg]

options_for_class_not_user = ["free_space_in_middle", "size", "bingo_id"]
for option in options_for_class_not_user:
    if option in file_config:
        options[option] = file_config[option]
    else:
        match option:
            case "free_space_in_middle":
                options["free_space_in_middle"] = False
            case "size":
                options["size"] = 5
if "url" in options:
    options["url"] = format_link(options["url"])

update_config(options)

print("Options:")
for option in options:
    print(f"{option} : {options[option]}")

if args["mode"] == "editconfig":
    print("bingoconfig.json updated with the previous options↑↑↑")
    exit()

from main import autobingo

not_for_class = ["count"]
# it's "options" without the "count" key
input_options = {}
for option in options:
    if not (option in not_for_class):
        input_options[option] = options[option]

# kinda like object destructuring in js
bingo = autobingo(**input_options)

match args["mode"]:
    case "generate" | "gen":
        print(f"Generating {options['count']} cards from {options['url']}")
        bingo.create_cards(options["count"])
        print("Cards generated! Check the cards.txt file for the links")
    case "check":
        print("Checking to see if my mans (or gals) got a bingo....")
        bingo.check_bingo_of_all_cards()
