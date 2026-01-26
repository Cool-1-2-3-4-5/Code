
import numpy as np
from ultralytics import YOLO


# For Webcam
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2 as cv2

# Chess Model
print("H!")
model = YOLO(r"C:\Users\elilt\OneDrive\Desktop\Projects\Chess Robot\YOLO_and_Image_Database\best.pt")
print("H2")
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break
    results = model(frame, conf=0.5)
    newFrame = results[0].plot()
    enlarged_frame = cv2.resize(newFrame, None, fx=1.6, fy=1.6, interpolation=cv2.INTER_CUBIC)
    cv2.imshow("Chess Detection", enlarged_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()


# #Parametres
# def empty():
#     pass
# cv2.namedWindow("Parametres")
# cv2.createTrackbar("H_Min","Parametres",0,255,empty)
# cv2.createTrackbar("S_Min","Parametres",0,255,empty)
# cv2.createTrackbar("V_Min","Parametres",0,255,empty)
# cv2.createTrackbar("H_Max","Parametres",0,255,empty)
# cv2.createTrackbar("S_Max","Parametres",0,255,empty)
# cv2.createTrackbar("V_Max","Parametres",0,255,empty)
# # Find position of the chess
# def position(piece_x,piece_y):
#     x_pos = (piece_x - board_x)/board_width
#     x_pos = round(x_pos)
#     y_pos = (piece_y - board_y)/board_height
#     y_pos = round(y_pos)
#     return (x_pos+1),(y_pos+1)

# # Chessboard detection
# print("HI")
# cap = cv2.VideoCapture(1) # intialize
# board_x,board_y,board_width,board_height = 0,0,0,0
# while True:
#     check, frame = cap.read()
#     if not check:
#         print("NOT Wokring")
#         break
#     hue = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
#     colour_lower = np.array([cv2.getTrackbarPos("H_Min","Parametres"),cv2.getTrackbarPos("S_Min","Parametres"),cv2.getTrackbarPos("V_Min","Parametres")])
#     colour_higher = np.array([cv2.getTrackbarPos("H_Max","Parametres"),cv2.getTrackbarPos("S_Max","Parametres"),cv2.getTrackbarPos("V_Max","Parametres")])
#     object = cv2.inRange(hue, colour_lower, colour_higher)    
#     countours, hierachry = cv2.findContours(object, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     x, y, width, height = 0,0,0,0
#     for i in countours:
#         noise = cv2.contourArea(i)
#         if noise > 3000:
#             x, y, width, height = cv2.boundingRect(i)
#             # print(str(x))
#             cv2.rectangle(frame, (x, y), (x+width, y+height), (0, 255, 0), 2)
#     cv2.imshow("Detection",frame)
#     cv2.imshow("d",object)
#     if cv2.waitKey(2) & 0xFF == ord('d'): # id d is pressed and
#         board_x,board_y = x, y
#         board_width,board_height = width, height
#         capture = frame.copy() 
#         break
# print("X1: " + str(board_x) + " Y1: " + str(board_y) + " X2: " + str(board_x+board_width) + " Y2: " + str(board_y+board_height))
# board_width = board_width/8
# board_height = board_height/8

# #Draw Board
# for i in range(8):
#     for j in range(8):
#         cv2.rectangle(capture,(int(board_x+(board_width*j)),int(board_y+(board_height*i))),(int(board_x+(board_width*(j+1))),int(board_y+(board_height*(i+1)))),(255,0,0),1)

# cv2.imshow("NewFrame", capture)
# while True:
#     if cv2.waitKey(2) & 0xFF == ord('d'):
#         break
    
# cap.release()  # destroys memroy asssociated with opening wideo

# cv2.destroyAllWindows()


# # Edge Detection
# # while True:
# #     check, frame = cap.read()
# #     if not check:
# #         print("NOT Wokring")
# #         break
# #     edges = cv2.Canny(frame,150,190) # MinVal and MaxVal
# #     cv2.imshow("Detection",edges)
# #     if cv2.waitKey(2) & 0xFF == ord('d'): # id d is pressed and 
# #         break