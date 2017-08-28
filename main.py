import screenshot
import threading
import pyautogui
import detector
import win32api
import logic
import queue
import time
import cv2

visionRadius = 500

region = {'top': pyautogui.size()[1] // 2 - visionRadius // 2,
               'left': pyautogui.size()[0] // 2 - visionRadius // 2,
               'width': visionRadius, 'height': visionRadius}

def main():
    last_time = time.time()

    logic_queue = queue.LifoQueue()

    logic_thread = threading.Thread(target=logic.play, args=(logic_queue, visionRadius))
    logic_thread.daemon = True
    logic_thread.start()

    frame_queue = queue.LifoQueue()
    data_queue = queue.LifoQueue()

    detection_thread = threading.Thread(target=detector.worker, args=(frame_queue, data_queue))
    detection_thread.daemon = True
    detection_thread.start()

    while True:
        print('FPS: {}'.format(1 / (time.time() - last_time)))
        last_time = time.time()

        frame = screenshot.grab(region)

        frame_queue.put(frame)
        image, boxes, scores, classes = data_queue.get()

        logic_queue.put((boxes[0], scores[0], classes[0]))

        cv2.imshow('BOT Fritz', image)

        # DELETE key to quit
        if cv2.waitKey(1) & win32api.GetAsyncKeyState(0x2E):
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()