from mss import mss
import pyautogui

sct = mss()

def grab(region=None):
    if not region:
        region = {'top': 0,
                  'left': 0,
                  'width': pyautogui.size()[0],
                  'height': pyautogui.size()[1]}
    return sct.grab(region)