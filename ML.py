import cv2 as cv2
import numpy as np
# from ultralytics import YOLO

# Chess Model
# model = YOLO(r"C:\Users\elilt\OneDrive\Desktop\Projects\Chess Robot\YOLO_and_Image_Database\best.pt")
# cap = cv2.VideoCapture(1)
# while True:
#     success, frame = cap.read()
#     if not success:
#         break
#     results = model(frame, conf=0.8)
#     newFrame = results[0].plot()
#     cv2.imshow("Chess Detection", newFrame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()

# Chessboard detection
cap = cv2.VideoCapture(0) # intialize
x1,y1,x2,y2 = 0,0,0,0
while True:
    check, frame = cap.read()
    if not check:
        print("NOT Wokring")
        break
    hue = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    colour_lower = np.array([0,0,0])
    colour_higher = np.array([255,255,58])
    object = cv2.inRange(hue, colour_lower, colour_higher)    
    countours, hierachry = cv2.findContours(object, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x, y, width, height = 0,0,0,0
    for i in countours:
        noise = cv2.contourArea(i)
        if noise > 3000:
            x, y, width, height = cv2.boundingRect(i)
            print(str(x))
            cv2.rectangle(frame, (x, y), (x+width, y+height), (0, 255, 0), 2)
    cv2.imshow("Detection",frame)
    cv2.imshow("d",object)
    if cv2.waitKey(2) & 0xFF == ord('d'): # id d is pressed and
        x1,y1 = x, y
        x2,y2 = width, height
        capture = frame.copy() 
        break
print("X1: " + str(x1) + " Y1: " + str(y1) + " X2: " + str(x2) + " Y2: " + str(y2))
for i in range(8):
    cv2.rectangle(capture,(int(x1*(x2*i)),int(y1)),(int(x1*(x2+1+i)),int(y2)),(255,0,0),1)
cv2.imshow("NewFrame", capture)
while True:
    if cv2.waitKey(2) & 0xFF == ord('d'):
        break
    
cap.release()  # destroys memroy asssociated with opening wideo

cv2.destroyAllWindows()


# Edge Detection
# while True:
#     check, frame = cap.read()
#     if not check:
#         print("NOT Wokring")
#         break
#     edges = cv2.Canny(frame,150,190) # MinVal and MaxVal
#     cv2.imshow("Detection",edges)
#     if cv2.waitKey(2) & 0xFF == ord('d'): # id d is pressed and 
#         break