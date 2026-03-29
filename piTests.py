from gpiozero import Device, AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import json

Device.pin_factory = PiGPIOFactory()

# Read measurements.json and output to data array
with open('inversekinematics.json', 'r') as f:
    data = json.load(f)

class Mover(AngularServo):
    def set_angle(self, degrees, speed_dps=20.0, update_interval=0.03, min_step=0.8):
        if self.angle is not None:
            current_angle = float(self.angle)
        else:
            current_angle = 90.0

        target_angle = float(degrees)
        step = max(float(min_step), float(speed_dps) * float(update_interval))

        if current_angle < target_angle:
            while current_angle < target_angle:
                current_angle = min(current_angle + step, target_angle)
                self.angle = current_angle
                sleep(update_interval)
        else:
            while current_angle > target_angle:
                current_angle = max(current_angle - step, target_angle)
                self.angle = current_angle
                sleep(update_interval)
arm = Mover(
    17,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.5 / 1000,    # 0.5 ms
    max_pulse_width=2.5 / 1000     # 2.5 ms
)

# arm = Mover(
#     27,
#     min_angle=0,
#     max_angle=180,
#     min_pulse_width=0.5 / 1000,    # 0.5 ms
#     max_pulse_width=2.5 / 1000     # 2.5 ms
# )

# forearm = Mover(
#     22,
#     min_angle=0,
#     max_angle=180,
#     min_pulse_width=0.5 / 1000,    # 0.5 ms
#     max_pulse_width=2.5 / 1000     # 2.5 ms
# )

# wrist = Mover(
#     23,
#     min_angle=0,
#     max_angle=180,
#     min_pulse_width=0.5 / 1000,    # 0.5 ms
#     max_pulse_width=2.5 / 1000     # 2.5 ms
# )

def reset_angles():
    # hub.angle = 180
    arm.angle = 180
    # forearm.angle = 180
    # wrist.angle = 180


# Main program loop
print("Enter2sss13 'q' or Ctrl+C to quit")

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
            arm.set_angle(movement[0])
            # arm.set_angle(movement[1])
            # forearm.set_angle(movement[2])
            # wrist.set_angle(movement[3])
            sleep(0.5)  # Small delay to let servo reach position
        except KeyError:
            print("Please enter a valid chess position (a1-h8)")
            
except KeyboardInterrupt:
    print("\nProgram stopped by user")

finally:
    # Optional: return servo to neutral/center when done
    reset_angles()
    print("Servo returned to center position")