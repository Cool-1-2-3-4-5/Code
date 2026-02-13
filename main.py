import chess
# import gpiozero as Servo
import json
# import os
# os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
# import cv2 as vision
import time


import MovementFunctions
import ChessLibrary
import ML



# camera = vision.VideoCapture(0)

print("Welcome to the Robot vs Human Chess Game, White to go first, once turn is done press 'space bar' to ensure you final move is confirmed")
print("LETS START THE GAME IN 5 SECONDS")
start = time.time()
end = time.time()
while ((end-start) <5):
    end = time.time()
print("LETS BEGIN:")


