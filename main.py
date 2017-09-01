import screenshot
import threading
import pyautogui
import detector
import win32api
import tesser
import logic
import queue
import time
import cv2

import numpy as np

visionRadius = 500

def main():
    last_time = time.time()

    logic_queue = queue.LifoQueue()
    logic_thread = threading.Thread(target=logic.play, args=(logic_queue, visionRadius))
    logic_thread.daemon = True
    logic_thread.start()

    detector_frame_queue = queue.LifoQueue()
    detector_data_queue = queue.LifoQueue()
    detection_thread = threading.Thread(target=detector.worker, args=(detector_frame_queue, detector_data_queue))
    detection_thread.daemon = True
    detection_thread.start()

    tesser_frame_queue = queue.LifoQueue()
    tesser_data_queue = queue.LifoQueue()
    tesser_thread = threading.Thread(target=tesser.image_to_text, args=(tesser_frame_queue, tesser_data_queue))
    tesser_thread.daemon = True
    tesser_thread.start()

    while True:
        print('FPS: {}'.format(1 / (time.time() - last_time)))
        last_time = time.time()

        frame = np.asarray(screenshot.grab())

        aim_roi = frame[pyautogui.size()[1] // 2 - visionRadius // 2:
                        pyautogui.size()[1] // 2 + visionRadius // 2,
                        pyautogui.size()[0] // 2 - visionRadius // 2:
                        pyautogui.size()[0] // 2 + visionRadius // 2]

        time_roi = frame[0:
                        30,
                        pyautogui.size()[0] // 2 - 50:
                        pyautogui.size()[0] // 2 + 50]

        detector_frame_queue.put(aim_roi)
        tesser_frame_queue.put(time_roi)

        if not tesser_data_queue.empty():
            game_time = tesser_data_queue.get()

        if not detector_data_queue.empty():
            image, boxes, scores, classes = detector_data_queue.get()
            logic_queue.put((game_time, boxes[0], scores[0], classes[0]))

            cv2.imshow('BOT Fritz', image)

        # DELETE key to quit
        if cv2.waitKey(1) & win32api.GetAsyncKeyState(0x2E):
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()