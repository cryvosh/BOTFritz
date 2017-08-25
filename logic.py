import numpy as np
import pyautogui
import win32api
import keyboard
import time

pyautogui.FAILSAFE = False

def play(boxRay, scoreRay, classRay, scale, visionRadius):
    while True:
        time.sleep(0.1)
        i = dx = dy = 0

        # ENTER/RETURN key is pressed
        if win32api.GetAsyncKeyState(0x0D) != 0:
            # Player has been detected
            if scoreRay[0] >= 0.6:
                # Counter-strafe
                if win32api.GetAsyncKeyState(0x41) != 0:
                    keyboard.ReleaseKey(0x1E)
                    keyboard.PressKey(0x20)
                    time.sleep(0.05)
                    keyboard.ReleaseKey(0x20)
                    time.sleep(0.07)
                    continue
                elif win32api.GetAsyncKeyState(0x44) != 0:
                    keyboard.ReleaseKey(0x20)
                    keyboard.PressKey(0x1E)
                    time.sleep(0.05)
                    keyboard.ReleaseKey(0x1E)
                    time.sleep(0.07)
                    continue

                boxes = np.reshape(boxRay, (5, 4))

                dx = (((boxes[0][1] + boxes[0][3]) / 2) * visionRadius) - (visionRadius / 2)
                dy = (((boxes[0][0] + boxes[0][2]) / 2) * visionRadius) - (visionRadius / 2)

                for class_ in classRay:
                    if (class_ == 2.0 or class_ == 4.0) and scoreRay[i] >= 0.4:
                        dx = (((boxes[i][1] + boxes[i][3]) / 2) * visionRadius) - (visionRadius / 2)
                        dy = (((boxes[i][0] + boxes[i][2]) / 2) * visionRadius) - (visionRadius / 2)
                        break
                    i += 1

                dx *= scale
                dy *= scale

                pyautogui.dragRel(dx, dy, 0.0)

            else:
                keyboard.PressKey(0x1E)

        else:

            keyboard.ReleaseKey(0x1E)
            keyboard.ReleaseKey(0x20)