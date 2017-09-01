import pyautogui
import win32api
import keyboard
import time

scale = 3.5

AKM4 = [0x05, 0x03]
DEAGLE = [0x02, 0x06]
ARMOR = [0x06, 0x02]
ARMORHELM = [0x06, 0x03]

pyautogui.FAILSAFE = False

def play(queue, visionRadius):
    while True:
        time.sleep(0.1)
        i = 0

        # ENTER/RETURN key is pressed
        if win32api.GetAsyncKeyState(0x0D) != 0:

            game_time, boxes, scores, classes = queue.get()

            if '1:55' in game_time:
                buy()

            if scores[0] >= 0.6:

                counter_strafe()

                dx = (((boxes[0][1] + boxes[0][3]) / 2) * visionRadius) - (visionRadius / 2)
                dy = (((boxes[0][0] + boxes[0][2]) / 2) * visionRadius) - (visionRadius / 2)

                for class_ in classes:
                    if (class_ == 2.0 or class_ == 4.0) and scores[i] >= 0.4:
                        dx = (((boxes[i][1] + boxes[i][3]) / 2) * visionRadius) - (visionRadius / 2)
                        dy = (((boxes[i][0] + boxes[i][2]) / 2) * visionRadius) - (visionRadius / 2)
                        break
                    i += 1

                dx *= scale
                dy *= scale

                pyautogui.dragRel(dx, dy, 0.0)

            else:
                # W
                keyboard.PressKey(0x11)

            # Ugly, yes
            while not queue.empty():
                queue.get()
        else:
            keyboard.ReleaseAllKeys()

# Buggy, yes
def buy():
    keyboard.ReleaseAllKeys()

    # B
    keyboard.PressKey(0x30)
    time.sleep(0.1)
    keyboard.ReleaseKey(0x30)

    buy_list = [AKM4, DEAGLE]

    for scancode in ARMOR:
        keyboard.PressKey(scancode)
        time.sleep(0.1)
        keyboard.ReleaseKey(scancode)

    keyboard.PressKey(0x30)
    time.sleep(0.1)
    keyboard.ReleaseKey(0x30)

    for item in buy_list:
        for scancode in item:
            keyboard.PressKey(scancode)
            time.sleep(0.1)
            keyboard.ReleaseKey(scancode)

    for _ in range(3):
        keyboard.PressKey(0x30)
        time.sleep(0.1)
        keyboard.ReleaseKey(0x30)

def counter_strafe():
    hold_time = 0.05
    relax_time = 0.05

    counter = []
    wasd = [0x11, 0x1E, 0x1F, 0x20]

    for i in range(4):
        if wasd[i] in keyboard.PRESSED:
            keyboard.ReleaseKey(wasd[i])
            counter.append(wasd[(i + 2) % 4])

    if counter:
        for key in counter:
            keyboard.PressKey(key)

        time.sleep(hold_time)

        for key in counter:
            keyboard.ReleaseKey(key)

        time.sleep(relax_time)
