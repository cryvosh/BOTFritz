import screenshot
import threading
import detector
import win32api
import tesser
import logic
import time
import cv2

import numpy as np

# y1, y2, x1, x2 in percentages
aim_roi = (0.3, 0.7, 0.3, 0.7)
time_roi = (0.076, 0.099, 0.475, 0.525)
callout_roi = (0.08, 0.115, 0.08, 0.2)

def main():
    last_time = time.time()

    logic_input = [None]
    logic_thread = threading.Thread(target=logic.play, args=(logic_input, aim_roi))
    logic_thread.daemon = True
    logic_thread.start()

    detector_dict = {'input': [None], 'output': [None]}
    detection_thread = threading.Thread(target=detector.worker, kwargs=detector_dict)
    detection_thread.daemon = True
    detection_thread.start()

    tesser_dict = {'input': [[None, None], [None, None]], 'output': [None, None]}
    tesser_thread = threading.Thread(target=tesser.image_to_text, kwargs=tesser_dict)
    tesser_thread.daemon = True
    tesser_thread.start()

    while True:
        print('Main thread FPS: {}'.format(1 / (time.time() - last_time)))
        last_time = time.time()

        frame = np.asarray(screenshot.grab(window_name='Counter-Strike: Global Offensive'))

        aim_frame = crop(frame, aim_roi)
        time_frame = crop(frame, time_roi)
        callout_frame = crop(frame, callout_roi)

        detector_dict['input'][0] = aim_frame
        tesser_dict['input'][0] = (time_frame, 245)
        tesser_dict['input'][1] = (callout_frame, -1)

        if detector_dict['output'][0] and tesser_dict['output'][0]:
            game_time, time_frame_debug = tesser_dict['output'][0]
            callout, callout_frame_debug = tesser_dict['output'][1]
            image, boxes, scores, classes = detector_dict['output'][0]

            logic_input[0] = (game_time, callout, image.shape, boxes[0], scores[0], classes[0])

            cv2.imshow('BOT Fritz', image)

        # DELETE key to quit
        if cv2.waitKey(1) & win32api.GetAsyncKeyState(0x2E):
            cv2.destroyAllWindows()
            break

def crop(frame, roi):
    height, width = frame.shape[:2]

    cropped = frame[int(height * roi[0]):
                    int(height * roi[1]),
                    int(width  * roi[2]):
                    int(width  * roi[3])]
    return cropped

if __name__ == '__main__':
    main()