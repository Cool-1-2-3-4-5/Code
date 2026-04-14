from gpiozero import Device, AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from concurrent.futures import ThreadPoolExecutor
import json

Device.pin_factory = PiGPIOFactory()


# Typical 180-degree servo calibration.
SERVO_MIN_PULSE_WIDTH = 0.7 / 1000  # 1.0 ms
SERVO_MAX_PULSE_WIDTH = 2 / 1000  # 2.0 ms

# min_pulse_width=0.5/1000,
#     max_pulse_width=2.4/1000

# SERVO_MIN_PULSE_WIDTH = 0.5 / 1000  # 1.0 ms
# SERVO_MAX_PULSE_WIDTH = 2.38 / 1000  # 2.0 ms

# SERVO_MIN_PULSE_WIDTH = 0.5 / 1000  # 1.0 ms
# SERVO_MAX_PULSE_WIDTH = 2.4 / 1000  # 2.0 ms

# Read measurements.json and output to data array
with open('inversekinematics.json', 'r') as f:
    data = json.load(f)

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
hub = Mover(
    17,
    min_angle=0,
    max_angle=180,
    min_pulse_width= 0.7 / 1000,
    max_pulse_width= 2 / 1000
)

arm = Mover(
    27,
    min_angle=0,
    max_angle=180,
    min_pulse_width= 0.5 / 1000,
    max_pulse_width= 2.4 / 1000
)

forearm = Mover(
    22,
    min_angle=0,
    max_angle=180,
    min_pulse_width= 0.5 / 1000,
    max_pulse_width= 2.38 / 1000
)

wrist = Mover(
    23,
    min_angle=0,
    max_angle=180,
    min_pulse_width= 0.5 / 1000,
    max_pulse_width= 2.4 / 1000
)
gripper = Mover(
    24,
    min_angle=0,
    max_angle=180,
    min_pulse_width= 0.5 / 1000,
    max_pulse_width= 2.4 / 1000
)


def reset_angles():
    hub.set_angle(0)
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

def update_board(move,interval=0.5):
    first_half = move[0] + move[1]
    positions = data[first_half]

    # first set
    hub.set_angle(positions[0])
    sleep(interval)
    arm.set_angle(positions[1])
    sleep(interval)
    forearm.set_angle(positions[2])
    sleep(interval)
    wrist.set_angle(positions[3])
    sleep(interval+1)
    gripper.set_angle(37)
    sleep(interval+3)
    
    
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

def drop_piece(interval=0.5):
    arm.set_angle(arm.angle-20)
    sleep(interval)
    forearm.set_angle(90)
    sleep(interval)
    hub.set_angle(0)
    sleep(interval)
    arm.set_angle(60)
    sleep(interval)
    wrist.set_angle(40)
    sleep(interval)
    gripper.set_angle(0)
    sleep(interval)


def capture_move(move,interval=0.5):
    first_half = move[-2] + move[-1]
    positions = data[first_half]

    # first set
    hub.set_angle(positions[0])
    sleep(interval)
    arm.set_angle(positions[1])
    sleep(interval)
    forearm.set_angle(positions[2])
    sleep(interval)
    wrist.set_angle(positions[3])
    sleep(interval+1)
    gripper.set_angle(37)
    sleep(interval+3)
    
    
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

    drop_piece()

    second_half = move[0] + move[1]

    positions2 = data[second_half]
    
    # Go to next square:
    
    hub.set_angle(positions2[0])
    sleep(interval)

    move_across(positions2[1],positions2[2])
    sleep(interval)

    # second set
    wrist.set_angle(positions2[3])
    sleep(interval)

    #Go down
    move_arm_with_wrist(positions2[4])
    sleep(interval)
    
    gripper.set_angle(41)
    sleep(interval)

    #Going up
    move_arm_with_wrist(-1 * positions2[4])
    sleep(interval)

    arm.set_angle(positions[1]-20)
    sleep(interval)

    # Place piece
    hub.set_angle(positions[0])
    sleep(interval)
    arm.set_angle(positions[1])
    sleep(interval)
    forearm.set_angle(positions[2])
    sleep(interval)
    wrist.set_angle(positions[3])
    sleep(interval+1)
    gripper.set_angle(37)
    sleep(interval+3)
    
    
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


# Main program loop
print("RUN 'q' or Ctrl+C to quit")
print("Resetting servos")
reset_angles()
sleep(2)
print("configure and start")
name = None
main_array=[[],[],[],[],[]]
array = ["h","a","f","w","g"]
while True:
    try:
        user_input = input("Enter position: ")
        if user_input == "move":
            move_to_play = input("ENTER MOVE: ")
            update_board(move_to_play)
        elif user_input == "move2":
            move_to_play = input("Capture MOVE: ")
            capture_move(move_to_play)
        elif user_input == "f1":
            degrees = int(input("Enter Degrees for threading"))
            move_across(degrees)
        elif user_input == "f2":
            degrees = int(input("Enter De"))
            move_arm_with_wrist(degrees)
        else:
            if user_input == "h":
                name = hub
                appender = "h"
            elif user_input == "f":
                name = forearm
                appender = "f"
            elif user_input == "a":
                name = arm
                appender = "a"
            elif user_input == "w":
                name = wrist
                appender = "w"
            elif user_input == "g":
                name = gripper
                appender = "g"
            else:
                if 0 <= int(user_input) <= 180:
                    name.set_angle(int(user_input))
                    main_array[array.index(appender)].append(int(user_input))
                    sleep(0.5)
                else:
                    print("pass")
                    sleep(0.5)
    except KeyboardInterrupt:
        print("EXIT")
        end_angle()
        print(main_array)
        print("Hub: " + str(main_array[0][-1]))
        print("Arm: " + str(main_array[1][-1]))
        print("Forearm: " + str(main_array[2][-1]))
        print("Wrist: " + str(main_array[3][-1]))
        print("Gripper: " + str(main_array[4][-1]))
        break
# a1:
# 139
# 93
# 132
# 75

# b1:
# 135
# 93
# 122
# 87
# Recaluclate forearm: conssitently 60 degrees under target