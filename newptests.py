from gpiozero import Device, AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import json
import json

Device.pin_factory = PiGPIOFactory()

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
    27,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.5 / 1000,    # 0.5 ms
    max_pulse_width=2.5 / 1000     # 2.5 ms
)


def reset_angles():
    hub.set_angle(180)


# Main program loop
print("RUN 'q' or Ctrl+C to quit")
print("Resetting servos")
reset_angles()
sleep(5)
print("configure and start")
print("Resetting servos")
reset_angles()
sleep(5)
print("configure and start")
while True:
    user_input = int(input("Enter position: "))
    if 0 <= user_input <= 180:
        movement = data[user_input]
        hub.set_angle(90)
        sleep(0.5)
    else:
        print("pass")
        sleep(0.5)
        