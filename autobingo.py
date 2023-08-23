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
    description="AutoBingo command line tool. Currently only being used for bingobaker.com",
    prog="autobingo",
    epilog="ion care how u use my code lol",
)

parser.add_argument(
    "mode",
    help="The mode to run the program in. [default: editconfig]",
    choices=["editconfig", "generate", "checkbingos", "help", "mark", "clear"],
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
    "-g",
    "--generator",
    help="The link to the bingo card generator",
    type=str,
    dest="url",
)
parser.add_argument(
    "-cnt",
    "--count",
    help="Number of bingo cards to generate from the generator link",
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
    help="Timeout in seconds for the webdriver to wait before clicking on each element to prevent malfunction [default : 0.6 ]",
    type=float,
)

# the rest of the defaults are in the autobingo class definition
parser.set_defaults(c=-1, mode="default", driver="default")

# dict repr of the arguments, will need some cleaning up
args = vars(parser.parse_args())

options = {}

# Pentru fiecare argument, daca e default sau None o sa luam din bingoconfig.json valoarea lui, daca nu e acolo atunci lasi asa si nu adaugi nimic in options ca o sa ia optiunea default automat din clasa autobingo

for arg in args:
    if args[arg] == None or args[arg] == -1 or args[arg] == "default":
        # read from bingoconfig.json
        pass
    elif args[arg] == "default":
        options[arg] = None
    else:
        options[arg] = args[arg]


from main import autobingo
