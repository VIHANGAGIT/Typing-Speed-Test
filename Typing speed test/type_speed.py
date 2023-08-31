import time
import random
import curses
from curses import wrapper

def start_scr(stdout):
    stdout.clear()
    stdout.addstr("""
        _____            _               ____                      _   _____         _   
       |_   _|   _ _ __ (_)_ __   __ _  / ___| _ __   ___  ___  __| | |_   _|__  ___| |_ 
         | || | | | '_ \| | '_ \ / _` | \___ \| '_ \ / _ \/ _ \/ _` |   | |/ _ \/ __| __|
         | || |_| | |_) | | | | | (_| |  ___) | |_) |  __/  __/ (_| |   | |  __/\__ \ |_ 
         |_| \__, | .__/|_|_| |_|\__, | |____/| .__/ \___|\___|\__,_|   |_|\___||___/\__|
             |___/|_|            |___/        |_|                     \n\n
""")
    stdout.addstr("Welcome to the Typing Speed Test by DEAMON_X")
    stdout.addstr("\nPress any key to begin!")
    stdout.refresh()
    stdout.getkey()
    
def disp_text(stdout, ref, usr, wpm = 0):
    stdout.addstr(ref)
    # Fstring is for embedding python variable in the string
    stdout.addstr(1, 0, f"WPM: {wpm}")
    
    # Get index to i and character to char    
    for i, char in enumerate(usr):
        # Manipulates where the string will be added in terminal
        text_color = curses.color_pair(1)
        if (char != ref[i]):
            text_color = curses.color_pair(2)
        stdout.addstr(0, i, char, text_color)
    
# Load the lines in lines.txt
def choose_line():
    with open("test_lines.txt", "r") as file:
        lines = file.readlines()
        return random.choice(lines).strip()
        
def test(stdout):
    ref_text = choose_line()
    usr_text = []
    wpm = 0
    st_time = time.time()
    # Used to avoid waiting for user input for the time calculation
    stdout.nodelay(True)

    while True:
        # Calculate elapsed time from started time, minimum value will be 1
        elapsed_time = max(time.time() - st_time, 1)
        # Initial calculation gives characters/m divided by 5 to get words/m assuming a word in general has 5 characters
        wpm = round((len(usr_text) / (elapsed_time / 60)) / 5)
        
        # Clear should be there because otherwise everything is going to repeat when refreshing.
        stdout.clear()
        disp_text(stdout, ref_text, usr_text, wpm)
        stdout.refresh()
        
        # Handles when user completed the test
        if "".join(usr_text) == ref_text:
            stdout.nodelay(False)
            break
        
        # Making sure nodelay does not get exceptions
        try:
            key = stdout.getkey()
        except:
            continue
        
        # If user press Esc he's gonna exit.
        if ord(key) == 27:
            break
        
        # Delete character when backspace is pressed
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(usr_text) > 0:
                usr_text.pop()
        elif len(usr_text) < len(ref_text):
            usr_text.append(key)
        
        
    

def main(stdout):
    # Colour pallets for the different states of the program
    # First is for text second is for background
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    
    start_scr(stdout)
    while(True):
        test(stdout)
        
        stdout.addstr(2, 0, "You completed the Speed Test! \n\n Press any key to play again.. \n\n Press Rsc to exit..")
        key = stdout.getkey()
        if ord(key) == 27:
            break
        
    

wrapper(main)

