import os
import random
import sys
from threading import Thread
from time import sleep
import vlc
from termcolor import colored
from config import *
import importlib
artFile = "art"  # Example, ensure this matches the actual file name (without .py)
art = importlib.import_module(f'arts.{artFile}')


# Importing module specified in the config file
art = __import__(f'arts.{artFile}', globals(), locals(), ['*'])

def replaceMultiple(mainString, toBeReplace, newString):
    """Replace a set of multiple substrings with a new string."""
    for elem in toBeReplace:
        if elem in mainString:
            mainString = mainString.replace(elem, newString)
    return mainString

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    try:
        base_path = sys._MEIPASS  # For PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def custom_print(art_lines, delay):
    """Custom print with colors and delays."""
    for line in art_lines:
        color_used = [random.choice(color)]  # Choose random colors
        color_attr = []

        for char in line:
            if char in colorCodes:
                if char == '⑨':  # Blink
                    color_attr = [colorCodes[char]]
                elif char == '⑩':  # Reset attributes
                    color_attr = []
                elif char == '®':  # Random color
                    color_used = color
                else:
                    color_used = [colorCodes[char]]

        # Print the line
        print(
            colored(
                replaceMultiple(line, colorCodes, ''),
                random.choice(color_used),
                attrs=color_attr,
            ),
            sep='',
            end='',
            flush=True,
        )
        sleep(delay)

def play_audio():
    """Play audio if enabled."""
    if playAudio:
        player = vlc.MediaPlayer(r"F:\Git python program\PyBirthdayWish-main\PyBirthdayWish-main\HappyBirthday.mp3")
        player.play()

def display_code():
    """Print the code if enabled."""
    if codePrint:
        for char in code:
            print(colored(char, codeColor), sep='', end='', flush=True)
            sleep(codingSpeed)
        input('\n\n' + colored('python3', 'blue') + colored(' PyBirthdayWish.py', 'yellow'))
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        input(colored('press F11 and hit {Enter}...', 'blue'))
        os.system('cls' if os.name == 'nt' else 'clear')

# Read the script's source code
with open(resource_path(__file__), 'r') as f_in:
    code = f_in.read()

# Clear the terminal
os.system('cls' if os.name == 'nt' else 'clear')

try:
    display_code()  # Display the source code
    Thread(target=play_audio).start()  # Start audio in a separate thread
    Thread(target=custom_print, args=(art.mainArt, speed)).start()  # Start printing art
    input()
except KeyboardInterrupt:
    print(colored('\n[-] Thanks!!', 'red'))
    os._exit(0)