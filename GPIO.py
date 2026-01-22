import gpiozero as Servo

class newServo(Servo):
    def move_to_pos(self,degrees):
        self.val = (degrees/90.0)-1

def reset_servos():
    rotate.move_to_pos()
    main_Arm.move_to_pos()
    arm.move_to_pos()
    grabber.move_to_pos()
def drop_to_side(degrees):
    rotate.move_to_pos(degrees)
    main_Arm.move_to_pos(degrees)
    arm.move_to_pos(degrees)
    grabber.move_to_pos(degrees)


rotate = newServo(1)
main_Arm = newServo(2)
arm = newServo(3)
grabber = newServo(4)


movesDict = {
    "a1": [0, 0, 0], "b1": [0, 0, 0], "c1": [0, 0, 0], "d1": [0, 0, 0], "e1": [0, 0, 0], "f1": [0, 0, 0], "g1": [0, 0, 0], "h1": [0, 0, 0],
    "a2": [0, 0, 0], "b2": [0, 0, 0], "c2": [0, 0, 0], "d2": [0, 0, 0], "e2": [0, 0, 0], "f2": [0, 0, 0], "g2": [0, 0, 0], "h2": [0, 0, 0],
    "a3": [0, 0, 0], "b3": [0, 0, 0], "c3": [0, 0, 0], "d3": [0, 0, 0], "e3": [0, 0, 0], "f3": [0, 0, 0], "g3": [0, 0, 0], "h3": [0, 0, 0],
    "a4": [0, 0, 0], "b4": [0, 0, 0], "c4": [0, 0, 0], "d4": [0, 0, 0], "e4": [0, 0, 0], "f4": [0, 0, 0], "g4": [0, 0, 0], "h4": [0, 0, 0],
    "a5": [0, 0, 0], "b5": [0, 0, 0], "c5": [0, 0, 0], "d5": [0, 0, 0], "e5": [0, 0, 0], "f5": [0, 0, 0], "g5": [0, 0, 0], "h5": [0, 0, 0],
    "a6": [0, 0, 0], "b6": [0, 0, 0], "c6": [0, 0, 0], "d6": [0, 0, 0], "e6": [0, 0, 0], "f6": [0, 0, 0], "g6": [0, 0, 0], "h6": [0, 0, 0],
    "a7": [0, 0, 0], "b7": [0, 0, 0], "c7": [0, 0, 0], "d7": [0, 0, 0], "e7": [0, 0, 0], "f7": [0, 0, 0], "g7": [0, 0, 0], "h7": [0, 0, 0],
    "a8": [0, 0, 0], "b8": [0, 0, 0], "c8": [0, 0, 0], "d8": [0, 0, 0], "e8": [0, 0, 0], "f8": [0, 0, 0], "g8": [0, 0, 0], "h8": [0, 0, 0]
}


# Case 1: If just move a piece
gotopos = movestr[0] + movestr[1]
rotate.move_to_pos((movesDict[gotopos])[0])
main_Arm.move_to_pos((movesDict[gotopos])[1])
arm.move_to_pos((movesDict[gotopos])[2])
grabber.move_to_pos(180)

newpos = movestr[2] + movestr[3]
rotate.move_to_pos((movesDict[gotopos])[0])
main_Arm.move_to_pos((movesDict[gotopos])[1])
arm.move_to_pos((movesDict[gotopos])[2])
grabber.move_to_pos(0)

reset_servos()

# Case 2: If wins

gotopos = movestr[2] + movestr[3]
rotate.move_to_pos((movesDict[gotopos])[0])
main_Arm.move_to_pos((movesDict[gotopos])[1])
arm.move_to_pos((movesDict[gotopos])[2])
grabber.move_to_pos(180)

drop_to_side(200)

newpos = movestr[0] + movestr[1]
rotate.move_to_pos((movesDict[gotopos])[0])
main_Arm.move_to_pos((movesDict[gotopos])[1])
arm.move_to_pos((movesDict[gotopos])[2])
grabber.move_to_pos(0)

reset_servos()

# Case 3.1: Kingside Castle SKIP FOR NOW
# Case 3.2: Queenside Castle SKIP FOR NOW

