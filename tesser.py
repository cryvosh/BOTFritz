import pytesseract
import PIL
import cv2

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'

def image_to_text(input, output):
    while True:
        for key in input.keys():
            if input[key] is not None:

                frame, threshold = input[key]

                gray = cv2.cvtColor(frame, cv2.COLOR_RGBA2GRAY)
                resized = cv2.resize(gray, None, fx=7, fy=7, interpolation=cv2.INTER_CUBIC)

                if threshold == -1:
                    thresh = cv2.threshold(resized, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                else:
                    thresh = cv2.threshold(resized, threshold, 255, cv2.THRESH_BINARY_INV)[1]

                blurred = cv2.blur(thresh, (7, 7))

                output[key] = (pytesseract.image_to_string(PIL.Image.fromarray(blurred)), blurred)