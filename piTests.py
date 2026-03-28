from gpiozero import Device, AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
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
    17,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.5 / 1000,    # 0.5 ms
    max_pulse_width=2.5 / 1000     # 2.5 ms
)

arm = Mover(
    27,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.5 / 1000,    # 0.5 ms
    max_pulse_width=2.5 / 1000     # 2.5 ms
)

forearm = Mover(
    22,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.5 / 1000,    # 0.5 ms
    max_pulse_width=2.5 / 1000     # 2.5 ms
)

wrist = Mover(
    23,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.5 / 1000,    # 0.5 ms
    max_pulse_width=2.5 / 1000     # 2.5 ms
)

def reset_angles():
    hub.angle = 180
    arm.angle = 0
    forearm.angle = 180
    wrist.angle = 180


# Main program loop
print("Enter1 'q' or Ctrl+C to quit")

try:
    print("Resetting servos")
    reset_angles()
    sleep(5)
    print("configure and start")
    while True:
        user_input = input("Enter position: ")
        
        if user_input.lower() in ['q', 'quit', 'exit']:
            print("Exiting...")
            break
            
        try:
            movement = data[user_input]
            hub.set_angle(movement[0])
            arm.set_angle(movement[1])
            forearm.set_angle(movement[2])
            wrist.set_angle(movement[3])
            sleep(0.5)  # Small delay to let servo reach position
        except KeyError:
            print("Please enter a valid chess position (a1-h8)")
            
except KeyboardInterrupt:
    print("\nProgram stopped by user")

finally:
    # Optional: return servo to neutral/center when done
    reset_angles()
    print("Servo returned to center position")