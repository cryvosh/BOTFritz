import screenshot
import threading
import detector
import win32api
import win32gui
import tesser
import logic
import time
import cv2

import numpy as np

# x1, x2, y1, y2 in percentages
aim_roi = (0.2, 0.8, 0.2, 0.8)

# Last value is threshold
tesser_rois = {'game_time':  ((0.475, 0.525, 0.076, 0.099), 245),
               'callout':    ((0.08, 0.2, 0.08, 0.115),      -1),
               'self_money': ((0.105, 0.185, 0.41, 0.44),    -1),
               'team_money': ((0.585, 0.64, 0.325, 0.72),   110),
               'velocity':   ((0.03, 0.08, 0.084, 0.0985),  230)}

def main():
    last_time = time.time()

    # 'movement' = 'roam', 'sound', or 'none'
    # 'game_mode' = 'defuse' or 'deathmatch'
    logic_dict = {'aim_roi': aim_roi, 'movement': 'roam', 'game_mode': 'defuse'}
    logic_thread = threading.Thread(target=logic.play, args=(logic_dict, None))
    logic_thread.daemon = True
    logic_thread.start()

    tesser_dict = {'input': {}, 'output': {}}
    tesser_thread = threading.Thread(target=tesser.image_to_text, kwargs=tesser_dict)
    tesser_thread.daemon = True
    tesser_thread.start()

    detector.setup()

    while True:
        print('Main thread FPS: {}'.format(1 / (time.time() - last_time)))
        last_time = time.time()

        window = win32gui.GetForegroundWindow()
        if win32gui.GetWindowText(window) != 'Counter-Strike: Global Offensive':
            logic.set_pause(True)

        frame = np.asarray(screenshot.grab(window_name='Counter-Strike: Global Offensive'))

        for key in tesser_rois.keys():
            tesser_dict['input'][key] = (crop(frame, tesser_rois[key][0]), tesser_rois[key][1])

        for key in tesser_dict['output'].keys():
            logic_dict[key] = tesser_dict['output'][key][0]

        image, detection_data = detector.detect(crop(frame, aim_roi))

        logic_dict['shape'] = image.shape
        logic_dict.update(detection_data)

        cv2.imshow('BOT Fritz', image)

        # END key to quit
        if cv2.waitKey(1) & win32api.GetAsyncKeyState(0x23):
            cv2.destroyAllWindows()
            break

def crop(frame, roi):
    height, width = frame.shape[:2]

    cropped = frame[int(height * roi[2]):
                    int(height * roi[3]),
                    int(width  * roi[0]):
                    int(width  * roi[1])]
    return cropped

if __name__ == '__main__':
    main()