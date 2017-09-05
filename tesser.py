import pytesseract
import PIL
import cv2

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'

def image_to_text(input, output):
    while True:
        for i in range(len(input)):

            frame, threshold = input[i]

            if frame is not None:
                gray = cv2.cvtColor(frame, cv2.COLOR_RGBA2GRAY)
                resized = cv2.resize(gray, None, fx=7, fy=7, interpolation=cv2.INTER_CUBIC)
                blurred = cv2.blur(resized, (3, 3))

                if threshold != -1:
                    thresh = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY_INV)[1]
                else:
                    thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

                output[i] = (pytesseract.image_to_string(PIL.Image.fromarray(thresh)), thresh)