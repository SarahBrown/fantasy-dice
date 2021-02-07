import cv2
import pytesseract
from pytesseract import Output

img = cv2.imread('image.jpg')

cap = cv2.VideoCapture(0)
#ret, img = cap.read()





config = ('-l eng --oem 1 --psm 3')
# pytessercat
text = pytesseract.image_to_string(img, config=config)
text.split('\n')
print(text)

cv2.imshow('img', img)
cv2.waitKey(0)
