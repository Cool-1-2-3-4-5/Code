import gpiozero as Servo
import json

def file_Reader():
    with open("inversekinematics.json","r") as file:
        movements = json.load(file)
    return movements

class newServo(Servo):
    def move_to_pos(self,degrees):
        self.val = (degrees/90.0)-1

def reset_servos(rotate,arm,forearm,wrist,grabber):
    rotate.move_to_pos()
    arm.move_to_pos()
    forearm.move_to_pos()
    wrist.move_to_pos()
    grabber.move_to_pos()

def drop_to_side(degrees,rotate,arm,forearm,wrist,grabber):
    rotate.move_to_pos(degrees)
    arm.move_to_pos(degrees)
    forearm.move_to_pos(degrees)
    wrist.move_to_pos(degrees)
    grabber.move_to_pos(degrees)


# rotate = newServo(1)
# main_Arm = newServo(2)
# arm = newServo(3)
# grabber = newServo(4)

def robotTurnToPlay(move_type,move_to_play,rotate,arm,forearm,wrist,grabber,movesDict):

    # Case 1: If just move a piece
    if move_type == "Regular":
        gotopos = move_to_play[0] + move_to_play[1]
        rotate.move_to_pos((movesDict[gotopos])[0])
        arm.move_to_pos((movesDict[gotopos])[1])
        forearm.move_to_pos((movesDict[gotopos])[2])
        wrist.move_to_pos((movesDict[newpos])[3])
        grabber.move_to_pos(180)

        newpos = move_to_play[2] + move_to_play[3]
        rotate.move_to_pos((movesDict[newpos])[0])
        arm.move_to_pos((movesDict[newpos])[1])
        forearm.move_to_pos((movesDict[newpos])[2])
        wrist.move_to_pos((movesDict[newpos])[3])
        grabber.move_to_pos(0)

        reset_servos()
        
    # Case 2: If wins
    elif move_type == "Piece Won":
        gotopos = move_to_play[2] + move_to_play[3]
        rotate.move_to_pos((movesDict[gotopos])[0])
        arm.move_to_pos((movesDict[gotopos])[1])
        forearm.move_to_pos((movesDict[gotopos])[2])
        wrist.move_to_pos((movesDict[newpos])[3])
        grabber.move_to_pos(180)

        drop_to_side(200)

        newpos = move_to_play[0] + move_to_play[1]
        rotate.move_to_pos((movesDict[newpos])[0])
        arm.move_to_pos((movesDict[newpos])[1])
        forearm.move_to_pos((movesDict[newpos])[2])
        wrist.move_to_pos((movesDict[newpos])[3])
        grabber.move_to_pos(0)

        reset_servos()

    # Case 3.1: Kingside Castle SKIP FOR NOW
    elif move_type == "Kingside":
        pass

    # Case 3.2: Queenside Castle SKIP FOR NOW
    else:
        pass

