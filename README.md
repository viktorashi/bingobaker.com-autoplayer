# SSSniperWolf-BBBingo-autoplay
 A script to play SSSniperWolf BBBingo by jacksfilms automatically
ToDO: will add more documentation

<h1> <span style="color:#F47174">
 Easiest
</span>: Command line usage: </h1>

First of all make sure you have pip and python 3.10+ or higher installed on your machine, if you don't have it installed, you can download it from [here](https://www.python.org/downloads/). 
Then, make sure you have git installed on your machine, if you don't have it installed, you can download it from [here](https://git-scm.com/downloads).



<h3>1. Open up  a Terminal / cmd window</h3>

Installation:
copy and paste this block into your terminal  
```bash
git clone https://github.com/viktorashi/bingobaker.com-autoplayer && cd bingobaker.com-autoplayer && pip install -r requirements.txt
```
<h3>2. Get usage directions</h3>



```bash
python  autobingo.py -h
```
```string
usage: autobingo [-h] [-d {chrome,edge,firefox,safari,ie,default}] [-u URL] [-cnt COUNT]
                 [-i INPUT_PATH] [-o OUTPUT_PATH] [-c CARDS_PATH] [-t TIMEOUT]
                 [{editconfig,generate,checkbingos,mark,clear}]

Auto Bingo playing command line tool. Currently only being used for bingobaker.com

positional arguments:
  {editconfig,generate,checkbingos,mark,clear}
                        The mode to run the program in. [default: editconfig]

options:
  -h, --help            show this help message and exit
  -d {chrome,edge,firefox,safari,ie,default}, --driver {chrome,edge,firefox,safari,ie,default}
                        The web browser to use. [default: chrome] Recommended: chrome, edge
  -u URL, --url URL     The link to the bingo card generator
  -cnt COUNT, --count COUNT
                        Number of bingo cards to generate from the generator link
  -i INPUT_PATH, --input INPUT_PATH
                        The file containing the keywords to search for on the bingo cards
                        [default: input.txt]
  -o OUTPUT_PATH, --output OUTPUT_PATH
                        File to write the bingo'ed cards to [default: output.txt]
  -c CARDS_PATH, --cards CARDS_PATH
                        The path you want the cards to be saved in
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout in seconds for the webdriver to wait before clicking on
                        each element to prevent malfunction [default : 0.6 ]

ion care how u use my code lol
```
for the operation and options

## Regarding  all the options : if nothing is specified, the last used value from the bingoconfig.json file will be used, if never specified before, the default values will be used

### <font size=5> Positional arguments</font> reffer to the first thing you type after ```python autobingo.py```, meaning the function you want to execute, generating, checking the bingos, marking the spots (which includes checking the bingo's if any spots containing the keywords have been found), and clearing the cards in case jack got a bigo already :'( 
    
- generate : generates {--count} bingo cards from the specified {--url}, writes their links to {--cards [default cards.txt]} (middle free space is always checked)
- mark : starts checking each card from {--cards} to see if they contain any keywords from {--input}, if they do, they check for a bingo, which, if found will output the link of those cards tp {--output}
- clear : clears the cards in {--cards} 
- checkbingos :checks bingos for each card, will be less used since it automatically checks the bingo eitherway for each card as it searches
- editconfig : is the default behaviour if nothing specified, it does nothing but update the ***bingoconfig.json***

### <font size=5> --input <sub> [default: input.txt , shorthand -i]</sub> </font>  is the file in which you have the keywords you want to search for on the bingo cards, each keyword on a new line. They DON'T have to be specified exactly as in the cards, lowercase values will be compared and they can just contain  those strings 
#### **`inpux.txt`**
``` 
freebooting a freebooted 
fake laugh
bro
```
### <font size=5> --output <sub>[default: output.txt, shorthand -o]</sub></font> : file that outputs the bingos 
#### **`output.txt`**
``` 
https://bingobaker.com/#64e7dce5f63bda5a
https://bingobaker.com/#64e7dce69d2d0c80
```

### <font size=5> --cards <sub>[default: cards.txt, shorthand -c]</font> </sub>: path you want the generated cards to be saved in 
#### **`cards.txt`**
``` 
..............
https://bingobaker.com/#64e7dce5f63bda5a
https://bingobaker.com/#64e7dce69d2d0c80
https://bingobaker.com/#64e7dce8ea9ba59b
https://bingobaker.com/#64e7ef15848b63aa
https://bingobaker.com/#64e7ef16a2ac9aa0
https://bingobaker.com/#64e7f64cb4cf4a44
https://bingobaker.com/#64e7f64e07911364
https://bingobaker.com/#64e7f650b9c63320
https://bingobaker.com/#64e7f65121c3c750
https://bingobaker.com/#64e7f6535e698b25
.................
```

### <font size=5> --url <sub>[default:"" nothing, only paramter that needs specified, shorthand -u]</sub></font>: the link to the bingobaker.com generator 

### <font size=5> --count <sub>[default: 10, shorthand -cnt]</sub></font> : number of cards to be generated by the {generate} function 

### <font size=5> --driver  <sub>[default: chrome, shorthand -d]</font></sub>: the webdriver to use (not all of them might work) 
options: 
 - chrome
 - edge
 - safari
 - firefox 
 - ie ("internet explorer" lol whytf idk can u even install it anymore? damn that nostalgia)

### <font size=5> --timeout <sub>[default : 0.6 , shorthand -t] </sub> </font>: the time the program waits before clicking an element if it has to, due to the webdriver messin up if it moves to fast sometimes, consider chaging it at will 

<h3><span style="color:#F47174"> 3. It will all be saved  </span></h3>

### Every parameter value you provide to the command will be saved in a file called ***bingoconfig.json*** right next to the program. <h3><span style="color:red"> DO NOT CHANGE THE CONFIG FILE DIRECTLY</span></h3>
idk how well i've tested this but i believe it starts messing up if you do. But delete it all-togather if you have and it doesn't work anymore, it will just generate another one.



<img src="image.png" alt="drawing" width="70">   <font size=40> Warning: </font> 
<h3>Some functionality might sometimes glitch due to excessive speed, in which case increasing the {--timeout} can be a good idea</h3>



<h1>Usage example</h1>

#### Don't be scared by the extensive docs, it's actually really easy to use
First you would usually want to generate the cards, so 
##### **`zsh`**
```bash
python autobingo.py generate --url https://bingobaker.com/#64c998520e68afc5 -cnt 100
```
should do the job, then you would create an **input.txt** right next to this and run

##### **`zsh`**
```bash
python autobingo.py mark
```
ez, peek into the console once in a while and see if it outputed anything about a congratilations, then go to output.txt to check it.
#### This opens up Microsoft Edge browser and and generates 75 bingo cards with the generator link you have provided to it, the bingo's of which will be saved to the ***wins.txt*** file, also increases the timeout.

##### **`zsh`**
```bash
python autobingo.py generate --url https://bingobaker.com/#64c998520e68afc5 --output wins.txt --count 75 --driver edge --timeout 0.8
```
Given all this data has been saved to ***bingoconfig.json*** this 


<h2>For the coders</h2>
There's also a class you can use in your projects by doing

```python
from main import autobingo
```

at the top of your adjecent python file





