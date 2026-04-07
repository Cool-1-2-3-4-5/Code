from gpiozero import Device, AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import json
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