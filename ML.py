import cv2 as cv
import numpy as np

# Mask and convert video to show only dark stuff
cap = cv.VideoCapture(0) # intialize
while True:
    check, frame = cap.read()
    hue = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    colour_lower = np.array([0,0,0])
    colour_higher = np.array([255,255,58])
    object = cv.inRange(hue, colour_lower, colour_higher)    
    countours, hierachry = cv.findContours(object, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for i in countours:
        noise = cv.contourArea(i)
        if noise > 3000:
            x, y, width, height = cv.boundingRect(i)
            cv.rectangle(frame, (x, y), (x+width, y+height), (0, 255, 0), 2)
    cv.imshow("Detection",frame)
    cv.imshow("d",object)
    if cv.waitKey(2) & 0xFF == ord('d'): # id d is pressed and 
        break
cap.release()  # destroys memroy asssociated with opening wideo
cv.destroyAllWindows

# print("hello")