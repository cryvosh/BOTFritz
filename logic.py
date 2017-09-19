import win32api
import keyboard
import time

scale = 7
turn_amount = 2000
paused = True

AKM4 = [0x05, 0x03]
DEAGLE = [0x02, 0x06]
ARMOR = [0x06, 0x02]
ARMORHELM = [0x06, 0x03]

def play(dict, _):
    global paused
    team = ''

    last_time = {'turn_amount_change':  time.time(),
                 'velocity_read':       time.time(),
                 'shot':                time.time(),
                 'jump':                time.time(),
                 'turn':                time.time()}

    while True:
        time.sleep(0.15)

        # ENTER/RETURN key is pressed
        if win32api.GetAsyncKeyState(0x0D) != 0:
            paused = not paused

        if not paused and 'shape' in dict:
            if dict['game_mode'] == 'defuse':
                if 'game_time' in dict and '1:55' in dict['game_time']:
                    team = detect_team(dict['callout'])
                    buy()

            if shoot(scale, dict['aim_roi'], dict['shape'], dict['boxes'], dict['scores'], dict['classes'], team):
                last_time['shot'] = time.time()
            elif dict['roam']:
                move(last_time, dict['velocity'])

            dict['boxes'] = None
        else:
            keyboard.ReleaseAllKeys()

def shoot(scale, aim_roi, shape, boxes, scores, classes, team=None):
    if boxes is None:
        return 0

    if team == 'CT':
        enemy_indices = [i for i in range(len(classes)) if classes[i] == 1 or classes[i] == 2]
    elif team == 'T':
        enemy_indices = [i for i in range(len(classes)) if classes[i] == 3 or classes[i] == 4]
    else:
        enemy_indices = [i for i in range(len(classes)) if classes[i] <= 4]

    if scores[enemy_indices[0]] >= 0.5:
        dx = (((boxes[enemy_indices[0]][1] + boxes[enemy_indices[0]][3]) / 2) - 0.5) * (aim_roi[1]-aim_roi[0]) * shape[1]
        dy = (((boxes[enemy_indices[0]][0] + boxes[enemy_indices[0]][2]) / 2) - 0.5) * (aim_roi[3]-aim_roi[2]) * shape[0]

        for i in enemy_indices:
            if (classes[i] == 2.0 or classes[i] == 4.0) and scores[i] > 0.5:
                dx = (((boxes[i][1] + boxes[i][3]) / 2) - 0.5) * (aim_roi[1]-aim_roi[0]) * shape[1]
                dy = (((boxes[i][0] + boxes[i][2]) / 2) - 0.5) * (aim_roi[3]-aim_roi[2]) * shape[0]
                break

        dx *= scale
        dy *= scale
        counter_strafe()

        keyboard.MoveMouse(dx, dy)
        time.sleep(0.02)
        keyboard.Click()
        return 1
    return 0

def move(last_time, velocity_str):
    # W
    keyboard.PressKey(0x11)

    if dt(last_time['shot']) > 1:
        global turn_amount

        if dt(last_time['turn']) < 2:
            return

        try:
            velocity = float(velocity_str)
            last_time['velocity_read'] = time.time()
            if velocity < 100:
                last_time['turn'] = time.time()
                keyboard.MoveMouse(turn_amount, 0)
        except ValueError:
            if dt(last_time['velocity_read']) > 3:
                last_time['turn'] = time.time()
                keyboard.MoveMouse(turn_amount, 0)

        if dt(last_time['jump']) > 7:
            keyboard.TapKey(0x39)
            keyboard.TapKey(0x1D)
            last_time['jump'] = time.time()

        if dt(last_time['turn_amount_change']) > 15:
            turn_amount *= -1
            last_time['turn_amount_change'] = time.time()

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

def set_pause(pause):
    global paused
    paused = pause

def dt(last_time):
    return (time.time() - last_time)

def detect_team(callout):
    if 'CT' in callout:
        return 'CT'
    else:
        return 'T'

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
