import chess
# import gpiozero as Servo
import json
# import os
# os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2 as vision
import time
import random


import MovementFunctions
import ChessLibrary
# import ML
import Learn

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

board_info = Learn.board_setup(cap)
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

# Robot goes first (Rbot is White)
legal_moves = list(bot.legal_moves)
random_index = random.randint(0, len(legal_moves) - 1)
random_move = legal_moves[random_index]
bot.push(random_move)
print("done")
print(board_info)
while not bot.is_checkmate():
    # Black goes
    updated_piece_locations = []
    bestMove_in_UCI = ''
    bestMove_in_SAN = ''
    move_type = ''
    updated_pieces = Learn.board_update(cap)
    # Finding which piece moved
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
        MovementFunctions.robotTurnToPlay(move_type,bestMove_in_UCI,rotate,arm,forearm,wrist,grabber,motor_positions)
        pass
    else:
        white_won = False