import chess
# from gpiozero import Device, AngularServo
# from gpiozero.pins.pigpio import PiGPIOFactory
import json
import tkinter as tk

# Set up pigpio pin factory for hardware PWM (reduces servo jitter)
# Device.pin_factory = PiGPIOFactory()

import time
from time import sleep
import random

# import MovementFunctions
import ChessLibrary
# import Learn
import View

# shoulder = MovementFunctions.Mover(
#     17,
#     min_angle=0,
#     max_angle=180,
#     min_pulse_width= 0.7 / 1000,
#     max_pulse_width= 2 / 1000
# )
# 
# arm = MovementFunctions.Mover(
#     27,
#     min_angle=0,
#     max_angle=180,
#     min_pulse_width= 0.5 / 1000,
#     max_pulse_width= 2.4 / 1000
# )
# 
# forearm = MovementFunctions.Mover(
#     22,
#     min_angle=0,
#     max_angle=180,
#     min_pulse_width= 0.5 / 1000,
#     max_pulse_width= 2.38 / 1000
# )
# 
# wrist = MovementFunctions.Mover(
#     23,
#     min_angle=0,
#     max_angle=180,
#     min_pulse_width= 0.5 / 1000,
#     max_pulse_width= 2.4 / 1000
# )
# 
# gripper = MovementFunctions.Mover(
#     24,
#     min_angle=0,
#     max_angle=180,
#     min_pulse_width= 0.5 / 1000,
#     max_pulse_width= 2.4 / 1000
# )

# Chess Setup - Load FEN
fen_string = "3k4/2ppp3/7Q/p4p2/P1P2P2/8/1P1PP1PP/RNB1KBNR w KQ - 0"
bot = chess.Board(fen_string)
white_won = True

# UI
root = tk.Tk()
root.title("Chess Game GUI")
gui = View.ChessboardUI(root, bot)

# Motor movements
# MovementFunctions.servo_loader(shoulder, arm, forearm, wrist, gripper)
# MovementFunctions.reset_angles(90)

# Set hub to 90 degrees
gui.setboard()
gui.root.update()

# Wait 5 seconds before moving
print("Waiting 5 seconds before robot moves...")
gui.delay(5)

# Robot Move from h6 to h8
print("Robot moving from h6 to h8...")
move_uci = "h6h8"
move_type = "Regular"

# Execute robot movement
# MovementFunctions.robotTurnToPlay(move_type, move_uci)

# Update the board with the move
gui.chess_logic.push_uci(move_uci)
gui.update_board()
gui.root.update()
gui.delay(2)

gui.clear_text("all")
gui.delay(1)
if white_won:
    text = "Robot has won!\nPlease Play Again!"
else:
    text = "Human has won!\nPlease Play Again!"
gui.write(text,"Who_won",5,50)
root.mainloop()
