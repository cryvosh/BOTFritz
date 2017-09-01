import pytesseract
import PIL
import cv2

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'

def image_to_text(frame_queue, data_queue):
    while True:
        gray = cv2.cvtColor(frame_queue.get(), cv2.COLOR_RGBA2GRAY)
        resized = cv2.resize(gray, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
        ret, thresh = cv2.threshold(resized, 230, 255, cv2.THRESH_BINARY_INV)

        data_queue.put(pytesseract.image_to_string(PIL.Image.fromarray(thresh)))