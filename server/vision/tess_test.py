import cv2
import numpy as np

import pytesseract
from pytesseract import Output

#img = cv2.imread('image.jpg')

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image,3)
 
#thresholding
def thresholding(image):
    image = cv2.GaussianBlur(image, (5,5),0)
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    #return cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,13,2)

#dilation
def dilate(image):
    kernel = np.ones((3,3),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
#erosion
def erode(image):
    kernel = np.ones((3,3),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

#opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((3,3),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

#template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED) 

#resize my a certain scale. scale is an int larger than 0. 100 = 1x scale
def resize_frame(src, scale):
    width = int(src.shape[1] * scale / 100)
    height = int(src.shape[0] * scale / 100)
    dsize = (width, height)
    return cv2.resize(src, dsize)

#applies the filters and cannies it.
def filter_frame(src):
    gray = resize_frame(src, 90)
    gray = remove_noise(gray)
    
    #gray = remove_noise(gray)
    
    
    gray = get_grayscale(gray)
    gray = thresholding(gray)
    
    
    #gray = opening(gray)
    #gray = opening(gray)
    #gray = erode(gray)
    
    gray = (255 - gray)
    
    return gray
    
def detect_motion(frame, old_frame):
    gray = get_grayscale(frame)
    gray = cv2.GaussianBlur(gray, (25,25), 0)
    
    gray_2 = get_grayscale(old_frame)
    gray_2 = cv2.GaussianBlur(gray_2, (25,25), 0)
    
    delta = cv2.absdiff(gray, gray_2)
    threshold=cv2.threshold(delta,35,255, cv2.THRESH_BINARY)[1]
    
    
    contours, x =cv2.findContours(threshold,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        return True
    
    return False

def d6(total):
    cap = cv2.VideoCapture(0)
    ret, old_frame = cap.read()
    frame = old_frame
    count_bool = False
    count = 0
    

    while(True):
        # Capture frame-by-frame


        old_frame = frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        m_f = frame
        m_of = old_frame
        motion_bool = detect_motion(m_f, m_of)
        canned = filter_frame(frame)
        
        #canned = canned[20:400, 100:480]
        canned = canned[20:400, 100:480]
        
        config = r'--oem 3 --psm 6 outputbase digits'
        # pytessercat
        text = pytesseract.image_to_string(canned, config=config)
        if text:
            text.split('\n')
            text.replace(" ", "")
            print(text)
            print("new set")
        
        
        # Display the resulting frame
        cv2.imshow('ocr',canned)
        
        if motion_bool:
            count_bool = True
        
        if count_bool:
            count = count + 1
            if count > 30:
                
                text.replace('-', '1')
                text.replace('-', '1')
                text.replace('9', '6')
                die_count = 0
                num_list = []
                for x in text:
                    if (x != '\n') and (x !='\x0c'):
                        try:
                            if x == '-':
                                x = 1
                            x = int(x)
                            if x > 0 and x < 7:
                                num_list.append(x)
                                die_count = die_count + 1
                        except ValueError:
                            print("bad char" + x)
                if die_count == total:
                    cap.release()
                    return num_list
                
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break

def get_dice(roll_purpose:str):
    dice_selection = {
        6: d6
    }
    total_dice = 1
    func = dice_selection.get(6, "no")
    final_num = func(total_dice)
    print("final number(s) ")
    print(final_num)
    return sum(final_num)

# When everything done, release the capture
cv2.destroyAllWindows()
