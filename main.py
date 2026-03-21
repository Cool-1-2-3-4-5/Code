import chess
from gpiozero import Device, AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
import json

# Set up pigpio pin factory for hardware PWM (reduces servo jitter)
Device.pin_factory = PiGPIOFactory()
# import os
# os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2 as vision
import time
from time import sleep
import random
import MovementFunctions
import ChessLibrary
# import ML
import Learn

with open('inversekinematics.json', 'r') as file:
    motor_positions = json.load(file)

shoulder = AngularServo(
    23,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.5 / 1000,    # 0.5 ms
    max_pulse_width=2.5 / 1000     # 2.5 ms
)
arm = AngularServo(
    23,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.5 / 1000,    # 0.5 ms
    max_pulse_width=2.5 / 1000     # 2.5 ms
)
forearm = AngularServo(
    23,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.5 / 1000,    # 0.5 ms
    max_pulse_width=2.5 / 1000     # 2.5 ms
)
wrist = AngularServo(
    23,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.5 / 1000,    # 0.5 ms
    max_pulse_width=2.5 / 1000     # 2.5 ms
)
gripper = AngularServo(
    23,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.5 / 1000,    # 0.5 ms
    max_pulse_width=2.5 / 1000     # 2.5 ms
)

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

board_info = Learn.board_setup(cap) #return [width of square, length of square, top left corner pos]
cap.release()
vision.destroyAllWindows()

# Motor movements
motor_positions = []
with open('inversekinematics.json', 'r') as f:
    motor_positions = json.load(f)

# Chess Setup
prev_piece_locations = [
    'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
    'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'
]
bot = chess.Board()
white_won = True

# Robot goes first (Robot is White)
legal_moves = list(bot.legal_moves)
random_index = random.randint(0, len(legal_moves) - 1)
random_move = legal_moves[random_index]
bot.push(random_move)
print("done")
print(board_info)

# Black and white flip-flop (Robot is White, user is black)
while not bot.is_checkmate():
    # Black goes
    updated_piece_locations = []
    bestMove_in_UCI = ''
    bestMove_in_SAN = ''
    move_type = ''
    # return locations (x,y) of black pieces
    updated_pieces = Learn.board_update(cap)
    # Determining chess piece squares based on (x,y) of pieces
    for piece in updated_pieces:
        updated_piece_locations.append(Learn.piece_in_square(piece,board_info))
    user_move_in_UCI = Learn.eval_board(updated_piece_locations,prev_piece_locations,len(updated_piece_locations),len(prev_piece_locations))
    if chess.Move.from_uci(user_move_in_UCI) in bot.legal_moves:
        bot.push_uci(user_move_in_UCI)
    else: # ADD HERE TO ALLOW FOR USER TO FIX THEIR MOVE
        print("Not Valid move, program crashed")
    print(bot)
    print("User played: " + user_move_in_UCI)
    # Robot calculated move
    if not bot.is_checkmate():
        bestMove_in_UCI, bestMove_in_SAN = ChessLibrary.minimax(bot,3,True,-100000,100000,True)
        ChessLibrary.reset()
        # Find if best move captures or just moves piece
        if 'x' in bestMove_in_SAN: #Capture
            move_type = "Piece Won"
        else:
            move_type = "Regular"
        # movement control: Run Robot movement
        #ADD SERVOS
        go_to_pos = motor_positions[bestMove_in_UCI[0]+bestMove_in_UCI[1]]
        return_to_pos = motor_positions[bestMove_in_UCI[2]+bestMove_in_UCI[3]]
        MovementFunctions.robotTurnToPlay(move_type, shoulder, arm, forearm, wrist, gripper,go_to_pos,return_to_pos)
        pass
    else:
        white_won = False