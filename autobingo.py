#the command line tool version of AutoBingo
import argparse
'''
`
idei de cum sa fac comannd lineu 

e pe moduri: 
    - editconfig [defaultu daca nu e specificat]
    - generate
    - checkbingos
    - help 
    - mark
    - clear
'''
parser = argparse.ArgumentParser(description='AutoBingo command line tool. Currently only being used for bingobaker.com', prog='autobingo', epilog='ion care how u use my code lol')
parser.add_argument('-d', '--driver' , help='The web browser to use. Recommended: chrome, edge', choices=['chrome', 'edge', 'firefox' , 'safari', 'ie' ] , type=str, dest="driver")
parser.add_argument('-g', '--generator', help='The link to the bingo card generator' , type=str, dest="url")
parser.add_argument('-i', '--input', help='The file containing the keywords to search for on the bingo cards [default: input.txt] ', type=str, dest="input_path")
parser.add_argument('-o', '--output', help="File to write the bingo'ed cards to [default: output.txt]", type=str , dest ="output_path")
parser.add_argument('-t', '--timeout', help='Timeout in seconds for the webdriver to wait before clicking on each element to prevent malfunction [default : 0.6 ]',   type=float)
parser.add_argument('-c', '--cards', help='The path you want the cards to be saved in', dest="cards_path", type=str)
parser.add_argument('-cnt', '--count', help='Number of bingo cards to generate from the generator link',type=int)
parser.add_argument("mode" , help="The mode to run the program in. [default: editconfig]", choices=['editconfig', 'generate', 'checkbingos', 'help', 'mark', 'clear'], nargs='?')


parser.set_defaults(c = 10, mode = "editconfig", driver = "chrome")

args = parser.parse_args()

# bingo = AutoBingo(args.file, int(args.count))


    



