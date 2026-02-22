import chess
# import gpiozero as Servo
import json
# import os
# os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2 as vision
import time
import random


# import MovementFunctions
# import ChessLibrary
# import ML
import Learn



# camera = vision.VideoCapture(0)

print("Welcome to the Robot vs Human Chess Game, White to go first, once turn is done press 'space bar' to ensure you final move is confirmed")
print("LETS START THE GAME IN 5 SECONDS")
start = time.time()
end = time.time()
while ((end-start) <2):
    end = time.time()
print("LETS BEGIN:")

# OpenCV Setup
cap = vision.VideoCapture(0)
cap.set(vision.CAP_PROP_FRAME_WIDTH, 640)
cap.set(vision.CAP_PROP_FRAME_HEIGHT, 480)

x = Learn.board_setup(cap)
cap.release()
vision.destroyAllWindows()

# Chess Setup
start_board = [
    'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
    'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'
]
bot = chess.Board()
white_won = True

# Robot goes first (Rbot is White)
legal_moves = list(bot.legal_moves)
random_index = random.randint(0, len(legal_moves) - 1)
random_move = legal_moves[random_index]
bot.push(random_move)
print("done")
print(x)
while not bot.is_checkmate():
    #Black goes
    pass