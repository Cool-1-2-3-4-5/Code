import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2 as cv2
import numpy as np
import time
import math

# Calibration Data
cameraMatrix = np.array([
    [727.84220328, 0., 354.16226615],
    [0., 730.03025553, 221.97923977],
    [0., 0., 1.]
])

distCoeffs = np.array([
    [0.11655149, -0.0385357, 0.00033531, 0.00156088, 0.31343139]
])


def undistort_frame(frame):
    h,  w = frame.shape[:2]
    newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, (w,h), 1, (w,h))
    
    # Undistort
    dst = cv2.undistort(frame, cameraMatrix, distCoeffs, None, newCameraMatrix)
    
    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    return dst

click_point = None
board_dict = {}
board_length = []

def mouse_callback(event, x, y, flags, param):
    global click_point
    if event == cv2.EVENT_LBUTTONDOWN:
        click_point = (x, y)
        print(f"Clicked at: {click_point}")

def piece_in_square(middle_of_piece):
    letters_array = ['a','b','c','d','e','f','g','h']
    x_pos = middle_of_piece[0]
    y_pos = middle_of_piece[1]
    top_corner_of_board = board_dict['a1'][0]
    relative_x_pos = x_pos - top_corner_of_board[0]
    relative_y_pos = y_pos - top_corner_of_board[1]
    raw_x = relative_x_pos/board_length[0]
    raw_y = relative_y_pos/board_length[1]
    true_pos_x = math.floor(raw_x)
    true_pos_y = math.floor(raw_y)
    piece = letters_array[true_pos_x] + str(true_pos_y+1)
    return piece


# LOOKL OVER THIS FUNCTION
def eval_board(current_setup_black,current_setup_white,previous_setup_black,previous_setup_white,black_prev,white_prev,black_cur,white_cur):
    string = ''
    for update in previous_setup_white:
        if update in current_setup_white:
            previous_setup_white.remove(update)
            current_setup_white.remove(update)
        else: #updated move
            string += update
    string += current_setup_white[0]
    return string

# Chess Model
print("H2")
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
print("H2")
file_name = 'test.jpg'

def board_analyser(cap):
    cv2.namedWindow("Frame")
    # Tell OpenCV to run 'mouse_callback' when events happen in the "Frame" window
    cv2.setMouseCallback("Frame", mouse_callback)
    main_set = set()
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        frame = undistort_frame(frame) # Assuming this function exists from your code

        # If we have clicked somewhere, draw a circle there
        if click_point is not None:
            main_set.add(click_point)
        
        for i in main_set:
            cv2.circle(frame, i, 5, (0, 0, 255), -1)

        if len(main_set) == 4:
            pts = list(main_set)
            pts.sort(key=lambda p: p[1])
            top_pts = sorted(pts[:2], key=lambda p: p[0])
            bot_pts = sorted(pts[2:], key=lambda p: p[0])
            TL, TR = top_pts[0], top_pts[1]
            BL, BR = bot_pts[0], bot_pts[1]
            
            delta_x = TR[0]-TL[0]
            delta_y = BL[1]-TL[1]
            delta_x = delta_x/8
            delta_y = delta_y/8
            x_pos = TL[0]
            y_pos = TL[1]
            global board_length
            board_length = [delta_x,delta_y]
            letters_array = ['a','b','c','d','e','f','g','h']
            # global board_dict
            for i in range(8):
                for j in range(8):
                    string = letters_array[j] + str(i+1)
                    x_first = int(x_pos+(j*delta_x))
                    x_second = int(x_pos+((j+1)*delta_x))
                    y_first = int(y_pos+(i*delta_y))
                    y_second = int(y_pos+((i+1)*delta_y))
                    borders_list = []
                    TLC = (x_first,y_first)
                    TRC = (x_second,y_first)
                    BLC = (x_first,y_second)
                    BRC = (x_second,y_second)
                    borders_list.append(TLC)
                    borders_list.append(TRC)
                    borders_list.append(BLC)
                    borders_list.append(BRC)
                    cv2.circle(frame, (x_first,y_first), 5, (0, 0, 255), -1)
                    cv2.circle(frame, (x_second,y_first), 3, (255, 0, 0), -1)
                    cv2.circle(frame, (x_first,y_second), 5, (0, 255, 0), -1)
                    cv2.circle(frame, (x_second,y_second), 3, (255,0, 255), -1)
                    board_dict[string] = borders_list

        cv2.imshow("Frame", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

board_analyser(cap)

print(board_dict)

















# 1. Reading Images
# image = cv.imread('Images/Birds.jpg')
# cv.imshow("CHECK",image)
# cv.waitKey(0)

# # 2. Read webcam (or video)
# cap = cv.VideoCapture(0) # intialize
# while True:
#     check, frame = cap.read() # function redes vudeo/webcam and return bool(frame was succefull or not) and frame
#     cv.imshow("Vid",frame)
#     if cv.waitKey(2000) & 0xFF == ord('d'): # id d is pressed and 
#         break
# cap.release()  # destroys memroy asssociated with opening wideo
# cv.destroyAllWindows

# # 3 Basic operation:
# # Resize:
# resized_img = cv.resize(image,(500,500))
# cv.imshow("New",resized_img)
# cv.waitKey(0)
# # Crop:
# cropped_img = image[100:200,50:200]
# cv.imshow("New",cropped_img)d
# cv.waitKey(0)


# # 4. Convert colour:
# gray_version = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
# cv.imshow("Gray",gray_version)
# cv.waitKey(0)

# # 5. Threshold (converty o remove discrepncies, perfect with gray scale)
# isTrue, new_frame = cv.threshold(gray_version,80,200,cv.THRESH_BINARY) # Parametres: image,lower range, upper range,type) in inverse anything less thna rdg value goes to 0 and reverse for other
# cv.imshow("Threshold", new_frame)
# cv.waitKey(0)

# # 5.1 Adaptive Threshold (Reular but better, threshold is different for each pixel)
# new_frame = cv.adaptiveThreshold(gray_version,300,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,21,30) # Parametres: image,lower range, upper range,type) in inverse anything less thna rdg value goes to 0 and reverse for other
# cv.imshow("adaptiveThreshold", new_frame)
# cv.waitKey(0)

# # 6. Edge Detection
# 3 types but use Canny
# edges = cv.Canny(image,280,30)
# cv.imshow("EDGES",edges)
# cv.waitKey(0)

# # 7. Contours and bounding boxes (For white space, makes lines around them)
# gray_version = cv.cvtColor(resized_img,cv.COLOR_BGR2GRAY)
# cv.imshow("Gray", gray_version)
# blurred = cv.GaussianBlur(gray_version, (5, 5), 0)
# cv.imshow("After Blur", blurred)
# thres = cv.adaptiveThreshold(blurred, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 11, 2)
# # isTrue, thres = cv.threshold(blurred, 127, 255, cv.THRESH_BINARY_INV)
# cv.imshow("Threshold", thres)
# countours, hierachry = cv.findContours(thres, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
# for i in countours:
#     area = cv.contourArea(i)
#     print(area)
#     if area > 100:
#         x, y, width, height = cv.boundingRect(i)
#         cv.rectangle(image, (x, y), (x+width, y+height), (0, 255, 0), 2)
# cv.imshow("BoundingBox", image)
# cv.waitKey(0)



### EXAMPLES

# # 1. Reading red on webcam:
# cap = cv.VideoCapture(0) # intialize
# while True:
#     check, frame = cap.read() # function redes video/webcam and return bool(frame was succefull or not) and frame
#     hue = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
#     colour_lower = np.array([0,130,80])
#     colour_higher = np.array([20,255,255])
#     object = cv.inRange(hue, colour_lower, colour_higher)
#     countours, hierachry = cv.findContours(object, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#     for i in countours:
#         area = cv.contourArea(i)
#         print(area)
#         if area > 100:
#             x, y, width, height = cv.boundingRect(i)
#             cv.rectangle(frame, (x, y), (x+width, y+height), (0, 255, 0), 2)
#     cv.imshow("Vid",frame)
#     if cv.waitKey(2) & 0xFF == ord('d'): # id d is pressed and 
#         break
# cap.release()  # destroys memroy asssociated with opening wideo
# cv.destroyAllWindows
