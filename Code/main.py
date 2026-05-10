import chess
from gpiozero import Device, AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
import tkinter as tk
Device.pin_factory = PiGPIOFactory() # (reduces servo jitter)
import cv2 as vision
from time import sleep
import random

import MovementFunctions
import ChessLibrary
import Learn
import View

shoulder = MovementFunctions.Mover(
    17,
    min_angle=0,
    max_angle=180,
    min_pulse_width= 0.7 / 1000,
    max_pulse_width= 2 / 1000
)

arm = MovementFunctions.Mover(
    27,
    min_angle=0,
    max_angle=180,
    min_pulse_width= 0.5 / 1000,
    max_pulse_width= 2.4 / 1000
)

forearm = MovementFunctions.Mover(
    22,
    min_angle=0,
    max_angle=180,
    min_pulse_width= 0.5 / 1000,
    max_pulse_width= 2.38 / 1000
)

wrist = MovementFunctions.Mover(
    23,
    min_angle=0,
    max_angle=180,
    min_pulse_width= 0.5 / 1000,
    max_pulse_width= 2.4 / 1000
)

gripper = MovementFunctions.Mover(
    24,
    min_angle=0,
    max_angle=180,
    min_pulse_width= 0.5 / 1000,
    max_pulse_width= 2.4 / 1000
)


# Chess Setup
prev_piece_locations = [
    'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
    'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'
]
bot = chess.Board()
white_won = True
stalemate = False
crashcheck = False

# UI
root = tk.Tk()
root.title("Chess Game GUI")
gui = View.ChessboardUI(root, bot)

# Motor movements
MovementFunctions.servo_loader(shoulder,arm,forearm,wrist,gripper)
MovementFunctions.reset_angles()

# OpenCV Setup
cap = vision.VideoCapture(0)
cap.set(vision.CAP_PROP_FRAME_WIDTH, 480)
cap.set(vision.CAP_PROP_FRAME_HEIGHT, 480)

gui.write("Welcome to the Robot vs Human\nChess Board Game! White to go\nfirst. Once turn is done press\n'space bar' to confirms your move","start",6,45)
gui.write("First set up the board! Enter\nthe four corners of the chess\nboard in any order to continue","setup",3,50)
main = Learn.board_setup(cap)
vision.destroyAllWindows()

# GAME LOGIC

# Game Opener
gui.write("Great!\nLETS START THE GAME\nIN 5 SECONDS","second_start",5,50)
gui.write("LETS BEGIN!","third_start",2,80)
gui.setboard()
gui.root.update()
gui.delay(2)

# GAME LOOP

# Robot goes first (Robot is White)
legal_moves = list(gui.chess_logic.legal_moves)
random_index = random.randint(0, len(legal_moves) - 1)
random_move = legal_moves[random_index]
gui.chess_logic.push(random_move)
gui.update_board()
MovementFunctions.robotTurnToPlay("Regular", str(random_move.uci()))


# Black and white flip-flop (Robot is White, user is black)
while not gui.chess_logic.is_checkmate() and not gui.chess_logic.is_stalemate():
    # BLACK Turn
    updated_piece_locations = []
    bestMove_in_UCI = ''
    bestMove_in_SAN = ''
    move_type = ''
    
    # Wait till user is done playing their move
    gui.root.bind('<space>',gui.pressed)
    gui.state = False
    while not gui.state:
        gui.root.update()
    
    # Return locations (x,y) of black pieces and evalute at what squares there is a piece
    locations = Learn.board_update(cap, main)
    vision.destroyAllWindows()
    setup = []
    if locations:
        for mid in locations:
            location = Learn.piece_in_square(mid)
            if location is not None:
                if location not in setup:
                    setup.append(location)    

        # Determining chess piece squares based on (x,y) of pieces
        user_move_in_UCI = Learn.eval_board(prev_piece_locations,setup)
        prev_piece_locations = setup.copy()
        if chess.Move.from_uci(user_move_in_UCI) in gui.chess_logic.legal_moves:
            gui.chess_logic.push_uci(user_move_in_UCI)
            gui.update_board()
            gui.root.update()
            if gui.chess_logic.is_check():
                gui.write("White in Check\n","Check",2,50,True)
                gui.root.update()

            # WHITE Turn

            # Robot calculated move
            if not gui.chess_logic.is_checkmate() and not gui.chess_logic.is_stalemate():
                bestMove_in_UCI, bestMove_in_SAN = ChessLibrary.minimax(gui.chess_logic, gui.chess_logic.legal_moves,5,True,-100000,100000,True)

                # Find if best move captures or just moves piece
                if 'x' in bestMove_in_SAN: #Capture
                    move_type = "Piece_Won"
                    remove_move = str(bestMove_in_UCI[-2]) + str(bestMove_in_UCI[-1])
                    prev_piece_locations.remove(remove_move)
                else:
                    move_type = "Regular"

                # movement control: Run Robot movement
                #ADD SERVOS
                MovementFunctions.robotTurnToPlay(move_type,bestMove_in_UCI)
                gui.chess_logic.push_san(bestMove_in_SAN)
                gui.update_board()
                if gui.chess_logic.is_check():
                    gui.write("Black in Check\n","Check",2,50,True)
                    gui.root.update()
            elif gui.chess_logic.is_checkmate():  #Black Won
                white_won = False
            else:
                stalemate = True
        else:
            gui.clear_text("all")
            gui.delay(1)
            gui.write("Not Valid move, program crashed","Issue",5,50)
            crashcheck = True
            break
    else:
        gui.clear_text("all")
        gui.delay(1)
        gui.write("Error with Camera Viewing","Issue",5,50)
        crashcheck = True
        break

if not crashcheck:
    if gui.chess_logic.is_stalemate():
        stalemate = True
    gui.clear_text("all")
    gui.delay(1)
    if stalemate:
        text = "Stalemate!\nPlease Play Again!"
    elif white_won:
        text = "Robot has won!\nPlease Play Again!"
    else:
        text = "Human has won!\nPlease Play Again!"
    gui.write(text,"Who_won",5,50)
gui.delay(3)
cap.release()
vision.destroyAllWindows()
