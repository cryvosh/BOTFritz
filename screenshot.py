import pyautogui
import win32gui
import mss

sct = mss.mss()

def grab(region=None, window_name=None):

    if not region:
        region = {'top': 0,
                  'left': 0,
                  'width': pyautogui.size()[0],
                  'height': pyautogui.size()[1]}

    if window_name:
        hwnd = win32gui.FindWindow(None, window_name)

        if hwnd != 0:
            right, bot = win32gui.GetClientRect(hwnd)[2:]
            width, height = win32gui.GetWindowRect(hwnd)[2:]

            region = {'top': height - bot - 3,
                      'left': width - right,
                      'width': right,
                      'height': bot}

    return sct.grab(region)