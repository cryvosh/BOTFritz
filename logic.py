import pyautogui
import win32api
import keyboard
import time

scale = 10

AKM4 = [0x05, 0x03]
DEAGLE = [0x02, 0x06]
ARMOR = [0x06, 0x02]
ARMORHELM = [0x06, 0x03]

pyautogui.FAILSAFE = False

def play(input, aim_roi):

    team = ''
    paused = True

    while True:
        time.sleep(0.1)

        # ENTER/RETURN key is pressed
        if win32api.GetAsyncKeyState(0x0D) != 0:
            paused = not paused

        if not paused:
            game_time, callout, shape, boxes, scores, classes = input[0]

            if '1:55' in game_time:
                team = detect_team(callout)
                buy()

            if not shoot(scale, team, aim_roi, shape, boxes, scores, classes):
                # W
                keyboard.PressKey(0x11)
        else:
            keyboard.ReleaseAllKeys()

def shoot(scale, team, aim_roi, shape, boxes, scores, classes):
    if team == 'CT':
        enemy_indices = [i for i in range(len(classes)) if classes[i] == 1 or classes[i] == 2]
    elif team == 'T':
        enemy_indices = [i for i in range(len(classes)) if classes[i] == 3 or classes[i] == 4]
    else:
        enemy_indices = [i for i in range(len(classes)) if classes[i] <= 4]

    if scores[enemy_indices[0]] >= 0.6:
        dx = (((boxes[enemy_indices[0]][1] + boxes[enemy_indices[0]][3]) - 1) / 2) * aim_roi[0] * shape[1]
        dy = (((boxes[enemy_indices[0]][0] + boxes[enemy_indices[0]][2]) - 1) / 2) * aim_roi[1] * shape[0]

        for i in enemy_indices:
            if scores[i] > 0.4:
                dx = (((boxes[i][1] + boxes[i][3]) - 1) / 2) * aim_roi[0] * shape[1]
                dy = (((boxes[i][0] + boxes[i][2]) - 1) / 2) * aim_roi[1] * shape[0]
                break

        dx *= scale
        dy *= scale
        counter_strafe()

        pyautogui.dragRel(dx, dy, 0.0)
        return 1
    return 0

def detect_team(callout):
    if 'CT' in callout:
        return 'CT'
    else:
        return 'T'

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
