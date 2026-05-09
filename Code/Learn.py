import os
import cv2 as cv2
import numpy as np
import time
import math
import json


# Camera Dimensions
size = 480

# Calibration Matrixes
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
corners = []
def mouse_callback(event, x, y, flags, param):
    global click_point
    if event == cv2.EVENT_LBUTTONDOWN:
        click_point = (x, y)
        corners.append(click_point)

# which square piece is in
def piece_in_square(middle_of_piece):
    letters_array = ['a','b','c','d','e','f','g','h']
    x_pos = middle_of_piece[0]
    y_pos = middle_of_piece[1]
    raw_x = x_pos/(size/8)
    raw_y = y_pos/(size/8)
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
    for update in prev_setup_main:
        if update in current_setup:
            prev_setup.remove(update)
            current_setup.remove(update)
        else: #updated move
            string += update
    string += current_setup[0]
    return string

def draw_board_grid_overlay(frame):
    delta_x = size/8
    delta_y = size/8
    top_left = [0,0]
    x_start = int(top_left[0])
    y_start = int(top_left[1])
    x_end = int(x_start + (8 * delta_x))
    y_end = int(y_start + (8 * delta_y))

    for point in range(9):
        x = int(x_start + (point * delta_x))
        y = int(y_start + (point * delta_y))
        cv2.line(frame, (x, y_start), (x, y_end), (255, 255, 0), 1)
        cv2.line(frame, (x_start, y), (x_end, y), (255, 255, 0), 1)

    return frame

def board_setup(cap):
    # Run 'mouse_callback' when mouse clicked in the "Frame" window
    main_set = set()
    while True:
        cv2.namedWindow("Setup", cv2.WINDOW_NORMAL)
        success, frame = cap.read()
        if not success:
            break        
        frame = preprocess_frame(frame)

        # Draw a circle at the "corner"
        if click_point is not None:
            main_set.add(click_point)
        
        for i in main_set:
            cv2.circle(frame, i, 5, (0, 0, 255), -1)

        if len(main_set) == 4:
            cv2.destroyAllWindows()
            pts = list(main_set)
            pts.sort(key=lambda p: p[1])
            top_pts = sorted(pts[:2], key=lambda p: p[0])
            bot_pts = sorted(pts[2:], key=lambda p: p[0]) 
            sorted_corners = [top_pts[0], top_pts[1], bot_pts[0], bot_pts[1]]
            
            duplicate = frame.copy()
            warped_version = perspective_view(duplicate, sorted_corners)
            x_pos = 0
            y_pos = 0
            delta_x = size/8
            delta_y = size/8
            for i in range(8):
                for j in range(8):
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
                    cv2.circle(warped_version, (x_first,y_first), 2, (0, 0, 255), -1)
                    cv2.circle(warped_version, (x_second,y_first), 2, (255, 0, 0), -1)
                    cv2.circle(warped_version, (x_first,y_second), 2, (0, 255, 0), -1)
                    cv2.circle(warped_version, (x_second,y_second), 2, (255,0, 255), -1)
            warped_version = cv2.resize(warped_version,(800,800))
            cv2.imshow("Warped Frame", warped_version)
            cv2.waitKey(5000)
            cv2.destroyAllWindows()
            return sorted_corners
        cv2.resizeWindow("Setup", 800, 1000)
        cv2.imshow("Setup", frame)
        cv2.setMouseCallback("Setup", mouse_callback)
        cv2.waitKey(20)

def board_update(cap,board_info):
    for buffer in range(20):
        cap.read()
    
    success, frame = cap.read()
    if not success:
        return
    
    frame = preprocess_frame(frame)
    frame = perspective_view(frame,board_info) 
    analysis_frame = frame.copy()
    chess_board = analysis_frame.copy()
    imgray = cv2.cvtColor(analysis_frame, cv2.COLOR_BGR2GRAY)
    ret, black_pieces = cv2.threshold(imgray, 90, 255, cv2.THRESH_BINARY_INV)
    black_countours, hierachry = cv2.findContours(black_pieces, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    locations = []
    for i in black_countours:
        noise = cv2.contourArea(i)
        if 100 < noise < 7000:
            x, y, width, height = cv2.boundingRect(i)
            cv2.rectangle(chess_board, (x, y), (x+width, y+height), (0, 255, 0), 2)
            cv2.circle(chess_board, (int(x+(width/2)), int(y+(height/2))), 2, (0, 0, 255), 2)
            locations.append((int(x+(width/2)), int(y+(height/2))))

    # Overlay grid only after evaluation.
    draw_board_grid_overlay(chess_board)
    
    # Save or display results
    chess_board = cv2.resize(chess_board,(800,800))
    cv2.imshow("Updated Board", chess_board)
    cv2.waitKey(5000)
    return locations

def perspective_view(frame, board_info):
    TL = board_info[0] 
    TR = board_info[1]
    BL = board_info[2]
    BR = board_info[3]
    src_points = np.float32([TL, TR, BL, BR])
    final_pnts = np.float32([[0, 0], [size, 0], [0, size], [size, size]])
    matrix = cv2.getPerspectiveTransform(src_points, final_pnts)
    warped = cv2.warpPerspective(frame, matrix, (size, size))
    return warped