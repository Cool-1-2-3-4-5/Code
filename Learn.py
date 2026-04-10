import os
# os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "1"
import cv2 as cv2
import numpy as np
import time
import math
import json

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

def preprocess_frame(frame):
    frame = undistort_frame(frame)
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return frame

click_point = None

def mouse_callback(event, x, y, flags, param):
    global click_point
    if event == cv2.EVENT_LBUTTONDOWN:
        click_point = (x, y)
        print(f"Clicked at: {click_point}")

# which square piece is in
def piece_in_square(middle_of_piece,board_info):
    letters_array = ['a','b','c','d','e','f','g','h']
    x_pos = middle_of_piece[0]
    y_pos = middle_of_piece[1]
    top_corner_of_board = board_info[2]
    relative_x_pos = x_pos - top_corner_of_board[0]
    relative_y_pos = y_pos - top_corner_of_board[1]
    raw_x = relative_x_pos/board_info[0]
    raw_y = relative_y_pos/board_info[1]
    true_pos_x = math.floor(raw_x)
    true_pos_y = math.floor(raw_y)
    if 0 <= true_pos_x <= 7 and 0 <= true_pos_y <=7:
        loc = letters_array[true_pos_x] + str(8-true_pos_y)
        return loc

def eval_board(prev_setup_main,current_setup_main):
    prev_setup = prev_setup_main.copy()
    current_setup = current_setup_main.copy()
    string = ''
    x = []
    for update in prev_setup:
        if update in current_setup:
            prev_setup.remove(update)
            current_setup.remove(update)
        else: #updated move
            string += update
    string += current_setup[0]
    return string

def draw_board_grid_overlay(frame, board_info):
    if not board_info or len(board_info) < 3:
        return frame

    delta_x = board_info[0]
    delta_y = board_info[1]
    top_left = board_info[2]

    x_start = int(top_left[0])
    y_start = int(top_left[1])
    x_end = int(x_start + (8 * delta_x))
    y_end = int(y_start + (8 * delta_y))

    for idx in range(9):
        x = int(x_start + (idx * delta_x))
        y = int(y_start + (idx * delta_y))
        cv2.line(frame, (x, y_start), (x, y_end), (255, 255, 0), 1)
        cv2.line(frame, (x_start, y), (x_end, y), (255, 255, 0), 1)

    return frame

def board_setup(cap):
    cv2.namedWindow("Frame")
    # Tell OpenCV to run 'mouse_callback' when events happen in the "Frame" window
    cv2.setMouseCallback("Frame", mouse_callback)
    main_set = set()
    board_length = []
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        frame = preprocess_frame(frame)

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
            board_length = [delta_x,delta_y,TL]
            letters_array = ['a','b','c','d','e','f','g','h']
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
                    cv2.circle(frame, (x_first,y_first), 2, (0, 0, 255), -1)
                    cv2.circle(frame, (x_second,y_first), 2, (255, 0, 0), -1)
                    cv2.circle(frame, (x_first,y_second), 2, (0, 255, 0), -1)
                    cv2.circle(frame, (x_second,y_second), 2, (255,0, 255), -1)
                    # board_dict[string] = borders_list
            
            cv2.imshow("Frame", frame)
            cv2.waitKey(2000)

            return board_length

        cv2.imshow("Frame", frame)
        cv2.waitKey(20)
    cv2.destroyAllWindows()

def board_update(cap,board_info):
    success, frame = cap.read()
    if not success:
        return
    
    frame = preprocess_frame(frame)
    analysis_frame = frame.copy()
    chess_board = analysis_frame.copy()
    imgray = cv2.cvtColor(analysis_frame, cv2.COLOR_BGR2GRAY)
    ret, black_pieces = cv2.threshold(imgray, 40, 255, cv2.THRESH_BINARY_INV)
    black_countours, hierachry = cv2.findContours(black_pieces, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    locations = []
    for i in black_countours:
        noise = cv2.contourArea(i)
        if 100 < noise < 7000:
            x, y, width, height = cv2.boundingRect(i)
            cv2.rectangle(chess_board, (x, y), (x+width, y+height), (0, 255, 0), 2)
            cv2.circle(chess_board, (int(x+(width/2)), int(y+(height/2))), 2, (0, 0, 255), 2)
            locations.append((int(x+(width/2)), int(y+(height/2))))

    # Overlay grid only after analysis, as a user reference.
    draw_board_grid_overlay(chess_board, board_info)
    
    # Save or display results
    cv2.imshow("images_save/Main_Frame.jpg", chess_board)
    cv2.imshow("images_save/black_pieces.jpg", black_pieces)
    cv2.imwrite("images_save/gray.jpg", imgray)
    print("Analysis frames saved to images_save/")
    return locations
    
    
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    print("Starting chess board detection...")
    main = board_update(cap)
    # try:
    #     # Load pre-calibrated board info from file
    #     main = load_board_calibration()
    # except FileNotFoundError:
    #     print("ERROR: board_calibration.json not found!")
    #     print("Run this script with HEADLESS=False on a display-enabled machine first to calibrate.")
    #     exit(1)
    
    # locations = board_update(cap, main)
    # setup = []
    # for mid in locations:
    #     location = piece_in_square(mid,main)
    #     if location is not None:
    #         if location not in setup:
    #              setup.append(location)
    # print(setup)













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
