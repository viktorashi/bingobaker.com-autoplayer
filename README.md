# SSSniperWolf-BBBingo-autoplay
 A script to play SSSniperWolf BBBingo by jacksfilms automatically. Esentially opens a shitton of cards to increase your chances of winning and then you can check if the input you give to it results in a bingo for any of those cards.

<h1> <span style="color:#F47174">
 Easiest
</span>: Command line usage: </h1>

First of all make sure you have pip and python 3.10+ or higher installed on your machine, if you don't have it installed, you can download it from [here](https://www.python.org/downloads/). 
Then, make sure you have git installed on your machine, if you don't have it installed, you can download it from [here](https://git-scm.com/downloads).



<h3>1. Open up  a Terminal / cmd (better PowerShell) window</h3>

Installation:
copy and paste this block into your terminal  
```bash
git clone https://github.com/viktorashi/bingobaker.com-autoplayer && cd bingobaker.com-autoplayer && pip install -r requirements.txt
```
<h3>2. Usage example</h3>

#### Don't be scared by the extensive docs, it's actually really easy to use
First you would usually want to generate the cards, so 
##### **`zsh`**
```bash
python autobingo.py generate --url https://bingobaker.com/#64c998520e68afc5 -cnt 100
```
should do the job, then you would create an **input.txt** right next to this and run

##### **`zsh`**
```bash
python autobingo.py check
```
This will copy "!bingowin #\<number\>" to your clipboard automatically for each bingo found
ez, see if it outputed anything about a congratilations, then go to output.json to check it.
#### This generates 75 bingo cards with the generator link you have provided to it, the bingo's of which will be saved to the ***wins.txt*** file.

##### **`zsh`**
```bash
python autobingo.py generate --url https://bingobaker.com/#64c998520e68afc5 --output wins.txt --count 75 
```
Given all this data has been saved to ***bingoconfig.json*** this 


<h3>3. Get usage directions</h3>


```bash
python  autobingo.py -h
```
```string
usage: autobingo [-h] [-u URL] [-cnt COUNT] [-i INPUT_PATH] [-o OUTPUT_PATH] [-c CARDS_PATH]
                 [-gm {normal,blackout,peen,3in6,loser,4corners,X,x}] [-r] [-strt START] [-fs FREE_SPACE] [-acc NUM_OF_THREADS]
                 [{editconfig,generate,check}]

Auto Bingo playing command line tool. Currently only being used for bingobaker.com

positional arguments:
  {editconfig,generate,check}
                        The mode to run the program in. [default: editconfig]

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     The link to the bingo card generator
  -cnt COUNT, --count COUNT
                        Number of bingo cards to generate from the generator link
  -i INPUT_PATH, --input INPUT_PATH
                        The file containing the keywords to search for on the bingo cards [default: input.txt]
  -o OUTPUT_PATH, --output OUTPUT_PATH
                        File to write the bingo'ed cards to [default: output.txt]
  -c CARDS_PATH, --cards CARDS_PATH
                        The path you want the cards to be saved in
  -gm {normal,blackout,peen,3in6,loser,4corners,X,x}, --gamemode {normal,blackout,peen,3in6,loser,4corners,X,x}
                        The gamemode to play in. [default: normal]
  -r, --reverse         Reverse the bingo card order when reading from [cards.txt] [default False]
  -strt START, --start START
                        The index of the card to start doing anything from
  -fs FREE_SPACE, --free-space FREE_SPACE
                        Name of the freespace to search for in the card [default: 'free space']
  -acc NUM_OF_THREADS, -accelleration NUM_OF_THREADS
                        The number of threads to use for speeding up

ion care how u use my code lol
```
for the operation and options



## Regarding  all the options : if nothing is specified, the last used value from the bingoconfig.json file will be used, if never specified before, the default values will be used

### <font size=5> Positional arguments</font> refer to the first thing you type after ```python autobingo.py```, meaning the function you want to execute, generating, checking the bingos, marking the spots (which includes checking the bingo's if any spots containing the keywords have been found), and clearing the cards in case jack got a bigo already :'( 
    
- generate : generates {--count} bingo cards from the specified {--url}, writes their links to {--cards [default cards.txt]} (middle free space is always checked)
- check :checks bingos for each card, will be less used since it automatically checks the bingo eitherway for each card as it searches (you can use the Databases supplied in the repo to check for bingos)
- editconfig : is the default behaviour if nothing specified, it does nothing but update the ***bingoconfig.json***

### <font size=5> --accelleration <sub> [default: 7 , shorthand -acc]</sub> </font>: The number of threads to use for speeding it up, careful: too many and it's won't really work that well, I suggest around 10-15 the max, it's plenty fast eitherway

### <font size=5> --url <sub>[default:"" nothing, only paramter that needs specified, shorthand -u]</sub></font>: the link to the bingobaker.com generator 

### <font size=5> --count <sub>[default: 100, shorthand -cnt]</sub></font> : number of cards to be generated by the {generate} function 


### <font size=5> --gamemode <sub>[default : normal , shorthand -gm] </sub> </font>: The bingo shape for the code to check
options:
 - norrmal : full row, collumn or diagonal
 - blackout : all spots
 - peen : form of a peepee ╭ᑎ╮ middle collumn bottom row
 - 3in6 : 3x3 square inside 6x6 grid
 - loser : shape of an L on her forehead (first collumn, last row)
 - 4corners : 4 corners of the card
- X (or x): X shape
- plus : + shape

### <font size=5> --reverse <sub>[Bool, default: False, shorthand -r] </sub> </font>: Wether  to do all operations on cards in reverse or normal order, usage (kinda deprecated, was used when the app was slow asl): 
```bash
python autobingo.py mark -r
```
or 
```bash
python autobingo.py mark --reverse
```


### <font size=5> --start <sub>[int, default: 0, shorthard -strt] </sub> </font>:  The index of the card to start doing anything from (kinda deprecated, was used when the app was slow asl)

### <font size=5> --free-space <sub>[string, default: "free space", shorthand -fs] </sub> </font>: The name of the freespace spot to check for if the card has an even size (meaning there is no clear midde spot)

### <font size=5> --input <sub> [default: input.txt , shorthand -i]</sub> </font>  is the file in which you have the keywords you want to search for on the bingo cards, each keyword on a new line. They DON'T have to match perfectly with the ones in the cards: It's case insesitive and looks if the phrases in each line are a substring of what's written on the cards, for example:
#### **`inpux.txt`**
``` 
freebooting a freebooted 
fake laugh
bro
```
would all match
``` 
Freebooting a freebooted video
Fake Laugh
"bro"
```
respectively
### <font size=5> --output <sub>[default: output.json, shorthand -o]</sub></font> : file that outputs the bingos 
#### **`output.json`**
``` 
[{
    "url": "https://bingobaker.com/play/650263ec6865dd96",
    "completion": [
        [1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 1],
        [0, 0, 0, 0, 1, 0]
    ],
    "key": "!bingowin #65dd96"
}, {
    "url": "https://bingobaker.com/play/6502520d86a0fbb5",
    "completion": [
        [1, 1, 1, 0, 1, 0],
        [1, 1, 1, 1, 0, 0],
        [1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0]
    ],
    "key": "!bingowin #a0fbb5"
}]
```

### <font size=5> --cards <sub>[default: cards.txt, shorthand -c]</font> </sub>: path you want the generated cards to be saved in 
#### **`cards.txt`**
``` 
..............
{"url": "https://bingobaker.com/play/65024d5ed200c69e", "squares": [["Freebooting a freebooted video", "Jack predicts what she says/does", "References a famous TikTok audio", "\"What did you expect?\"", "Actual insight", "\"Girrrllllll\""], ["Nothing burger", "Forgets to react!", "Desaturated colors", "\"Ohhhh noooooo\"", "\"This guy be...\"", "Editing mistake"], ["Stock or Vine sound effect", "Random tangent", "Random graphic that adds nothing", "\"If that happened to me...\"", "\"Camcorder\" effect", "Mr. Beast subtitles"], ["Unnecessary yelling", "\"What is that?\"", "Says something that makes absolutely no sense", "Weird zoom", "Using same creator's vids multiple times", "Calling someone \"bro\""], ["Video is cropped far too much", "Explains the video before it starts", "Weird flex", "Victim Blaming", "Rain effect", "Steals someone's joke"], ["Contrast filter", "Baby talk", "Repeating what someone said but louder", "Any rhyming words (\"crusty musty\" etc.)", "Black and white filter", "Shaky camera effect"]]}
.................
```




<h3><span style="color:#F47174"> 3. It will all be saved  </span></h3>


### Every parameter value you provide to the command will be saved in a file called ***bingoconfig.json*** right next to the program. Plus it will automatically check set the size to the card's size, if the free space is in the middle or not and update that in the config file. Found bingo's are automatically clicked as well<h3><span style="color:red"> DO NOT CHANGE THE CONFIG FILE DIRECTLY</span></h3>



<img src="image.png" alt="drawing" width="70">   <font size=40> Warning: </font> 

idk how well i've tested this but i believe it starts messing up if you do. But delete it all-togather if you have and it doesn't work anymore, it will just generate another one.

Also, if you've checked the same card twice, even if you changed the gamemode, it won't auto-mark the spots again, even if the checked spots are different.


<h2>For the coders</h2>
There's also a class you can use in your projects by doing

```python
from main import autobingo
```

at the top of your adjecent python file


<h1>Credits</h1>

[Itamar1337](https://github.com/Itamar1337) - thanks for making it actually usable and and not have this script impose the same effect a TNT minecraft nuke bomb has on your pc

bye bruh