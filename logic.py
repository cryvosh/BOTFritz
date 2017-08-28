import pyautogui
import win32api
import keyboard
import time

scale = 3.5

pyautogui.FAILSAFE = False

def play(queue, visionRadius):
    while True:
        time.sleep(0.1)
        i = 0

        boxes, scores, classes = queue.get()

        # ENTER/RETURN key is pressed
        if win32api.GetAsyncKeyState(0x0D) != 0:
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
        else:
            keyboard.ReleaseAllKeys()

def counter_strafe():
    hold_time = 0.1
    wasd = [0x11, 0x1E, 0x1F, 0x20]

    for i in range(4):
        if wasd[i] in keyboard.PRESSED:
            keyboard.ReleaseKey(wasd[i])
            keyboard.PressKey(wasd[(i + 2) % 4])

    time.sleep(hold_time)

    for key in wasd:
        keyboard.ReleaseKey(key)
