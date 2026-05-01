from gpiozero import Device, AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from concurrent.futures import ThreadPoolExecutor
import json

Device.pin_factory = PiGPIOFactory()

with open('inversekinematics.json', 'r') as f:
    data = json.load(f)

hub = None
arm = None
forearm = None
wrist = None
gripper = None

class Mover(AngularServo):
    def set_angle(self,degrees,step_size=0.3, delay=0.01):
        if self.angle is not None:
            current_angle = self.angle
        else:
            current_angle = 90

        if current_angle < degrees:
            while current_angle < degrees:
                current_angle = min(current_angle + step_size, degrees)
                self.angle = current_angle
                sleep(delay)
        else:
            while current_angle > degrees:
                current_angle = max(current_angle - step_size, degrees)
                self.angle = current_angle
                sleep(delay)

def servo_loader(main_hub,main_arm,main_forearm,main_wrist,main_gripper):
    global hub
    hub = main_hub
    global arm
    arm = main_arm
    global forearm
    forearm = main_forearm
    global wrist
    wrist = main_wrist
    global gripper
    gripper = main_gripper

def reset_angles(hub_angle=0):
    hub.set_angle(hub_angle)
    arm.set_angle(0)
    forearm.set_angle(45)
    wrist.set_angle(180)
    gripper.set_angle(0)

def end_angle():
    hub.set_angle(0)
    arm.set_angle(0)
    forearm.set_angle(0)
    wrist.set_angle(0)
    gripper.set_angle(0)


def move_arm_with_wrist(angle):
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(arm.set_angle, arm.angle + angle)
        executor.submit(wrist.set_angle, wrist.angle + angle)

def move_across(arm_angle, forearm_angle):
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(arm.set_angle, arm_angle)
        executor.submit(forearm.set_angle, forearm_angle)

def regular_move(move,interval=0.8):
    first_half = move[0] + move[1]
    positions = data[first_half]

    # first set
    hub.set_angle(positions[0])
    sleep(interval)
    move_across(positions[1],positions[2])
    wrist.set_angle(positions[3])
    sleep(interval+1)
    gripper.set_angle(35)
    sleep(interval+1)
    
    
    #Go down
    move_arm_with_wrist(positions[4])
    sleep(interval)
    
    gripper.set_angle(49)
    sleep(interval)

    #Go Up
    move_arm_with_wrist(-1 * positions[4])
    sleep(interval)

    arm.set_angle(positions[1]-20)
    sleep(interval)

    second_half = move[2] + move[3]

    positions2 = data[second_half]
    
    # Go to next square:

    move_across(positions2[1],positions2[2])
    sleep(interval)

    # second set
    hub.set_angle(positions2[0])
    sleep(interval)
    wrist.set_angle(positions2[3])
    sleep(interval)

    #Go down
    move_arm_with_wrist(positions2[4])
    sleep(interval)
    
    gripper.set_angle(37)
    sleep(interval)

    #Going up
    move_arm_with_wrist(-1 * (positions2[4]+10))
    sleep(interval)
    wrist.set_angle(90)
    sleep(interval)
    
    reset_angles(90)
    sleep(interval)



def capture_move(move,interval=0.5):
    first_half = move[-2] + move[-1]
    positions = data[first_half]

    # first set
    hub.set_angle(positions[0])
    sleep(interval)
    move_across(positions[1]+3,positions[2]+3)
    sleep(0.2)
    move_across(positions[1],positions[2])
    sleep(interval)
    wrist.set_angle(positions[3])
    sleep(interval)
    gripper.set_angle(37)
    sleep(interval)
    
    #Go down
    move_arm_with_wrist(positions[4])
    sleep(interval)
    
    gripper.set_angle(46)
    sleep(interval)

    #Go Up
    move_arm_with_wrist(-1 * positions[4])
    sleep(interval)

    arm.set_angle(positions[1]-20)
    sleep(interval)

    # Drop Piece
    drop_piece()
    # Next Square
    second_half = move[0] + move[1]

    positions2 = data[second_half]
    # reset_angles(positions2[0])
    # sleep(interval)
    # Go to next square:
    
    hub.set_angle(positions2[0])
    sleep(interval)
    move_across(positions2[1]+3,positions2[2]+3)
    sleep(0.2)
    move_across(positions2[1],positions2[2])
    sleep(interval)
    wrist.set_angle(positions2[3])
    sleep(interval)
    gripper.set_angle(37)
    sleep(interval)

    #Go down
    move_arm_with_wrist(positions2[4])
    sleep(interval)
    print("here")
    gripper.set_angle(46)
    sleep(interval)
    
    #Going up
    move_arm_with_wrist(-1 * positions2[4])
    sleep(interval)
    print("heraae")
    arm.set_angle(positions2[1]-20)
    sleep(interval)

    # Place piece
    hub.set_angle(positions[0])
    sleep(interval)
    move_across(positions[1],positions[2])
    sleep(interval)
    wrist.set_angle(positions[3])
    sleep(interval+1)    
    
    #Go down
    move_arm_with_wrist(positions[4])
    sleep(interval)
    
    gripper.set_angle(37)
    sleep(interval)

    #Go Up
    move_arm_with_wrist(-1 * (positions[4]+10))
    sleep(interval)

    arm.set_angle(positions[1]-20)
    sleep(interval)
    
    wrist.set_angle(90)
    sleep(interval)

    reset_angles(90)
    sleep(interval)

def drop_piece(interval=0.5):
    arm.set_angle(60)
    sleep(interval)
    forearm.set_angle(90)
    sleep(interval)
    hub.set_angle(0)
    sleep(interval)
    wrist.set_angle(15)
    sleep(interval)
    gripper.set_angle(0)
    sleep(interval)

def resting(interval=0.5):
    arm.set_angle(90)
    sleep(interval)
    forearm.set_angle(0)
    sleep(interval)
    wrist.set_angle(80)
    sleep(interval)
    hub.set_angle(0)
    sleep(interval)
    gripper.set_angle(0)
    sleep(interval)

def robotTurnToPlay(move_type, move, interval=0.5):
    if move_type == "Piece_Won":
        capture_move(move,interval)
    else:
        regular_move(move,interval)
