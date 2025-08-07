import pyautogui
import keyboard
from pynput import mouse
# import mouse
import urllib.parse
import pyperclip
import time
import threading

isrunning = False
lock = threading.Lock()

def on_click(x, y, button, pressed):
    if pressed:
        if button == mouse.Button.left:
            with lock:
                global isrunning
                if not isrunning:
                    isrunning = True
                    threading.Thread(target=addsong, daemon=True).start()
        elif button == mouse.Button.middle:
            pass
        elif button == mouse.Button.right:
            return True # keep listening
        
        return False # stop listening

def addsong():
    try:
        isFound = False
        while not isFound:
            try:
                pos = pyautogui.locateCenterOnScreen('assets/fav.png', confidence=0.9)
                if pos:
                    isFound = True
            except pyautogui.ImageNotFoundException:
                print("image not found")
            
            time.sleep(0.5)

        pyautogui.click(pos)
    
    finally:
        with lock:
            global isrunning
            isrunning = False


def openlink(line):

    # find position of last space (' ')
    last_space_index = line.rstrip().rfind(' ')

    # remove last word and space
    if last_space_index != -1:
        trimmed_line = line[:last_space_index]
    else:
        print(f"Line without last word")

    # rewrite line in url format
    encoded_line = urllib.parse.quote(trimmed_line)
    final_line = f'https://music.apple.com/in/search?term={encoded_line}'

    pyautogui.hotkey('ctrl', 't')
    pyperclip.copy(final_line)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')

    pyperclip.copy(line)

def lineparser():

    with open('formatted_tracks.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in reversed(lines):
        line = line.rstrip() # remove trailing whitespaces

        # split into words
        words = line.split()

        last_word = words[-1]

        if last_word == "Explicit":
            openlink(line)

            # for explicit music, jump to url bar and type explicit
            pyautogui.hotkey('ctrl', 'l')
            pyautogui.typewrite('explicit')
            pyautogui.press('esc')
        
        else:
            openlink(line)

        # keyboard.wait('ctrl+space')
        # mouse.wait(button='left')
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()
        # addsong()
        time.sleep(1.5)
        pyautogui.hotkey('ctrl', 'w')


# initiate
time.sleep(4)
lineparser()