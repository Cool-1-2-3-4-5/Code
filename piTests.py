from gpiozero import Device, AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import json

Device.pin_factory = PiGPIOFactory()

# Read measurements.json and output to data array
with open('inversekinematics.json', 'r') as f:
    data = json.load(f)

hub = AngularServo(
    17,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.5 / 1000,    # 0.5 ms
    max_pulse_width=2.5 / 1000     # 2.5 ms
)

arm = AngularServo(
    27,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.5 / 1000,    # 0.5 ms
    max_pulse_width=2.5 / 1000     # 2.5 ms
)

forearm = AngularServo(
    22,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.5 / 1000,    # 0.5 ms
    max_pulse_width=2.5 / 1000     # 2.5 ms
)

wrist = AngularServo(
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
    
def set_angle(hub_deg, arm_deg, forearm_deg, wrist_deg, step_size=0.3, delay=0.01):
    # Move hub
    if hub.angle is not None:
        current_hub = hub.angle
    else:
        current_hub = 90
    
    if current_hub < hub_deg:
        while current_hub < hub_deg:
            current_hub = min(current_hub + step_size, hub_deg)
            hub.angle = current_hub
            sleep(delay)
    else:
        while current_hub > hub_deg:
            current_hub = max(current_hub - step_size, hub_deg)
            hub.angle = current_hub
            sleep(delay)
    
    # Move arm
    if arm.angle is not None:
        current_arm = arm.angle
    else:
        current_arm = 90
    
    if current_arm < arm_deg:
        while current_arm < arm_deg:
            current_arm = min(current_arm + step_size, arm_deg)
            arm.angle = current_arm
            sleep(delay)
    else:
        while current_arm > arm_deg:
            current_arm = max(current_arm - step_size, arm_deg)
            arm.angle = current_arm
            sleep(delay)
    
    # Move forearm
    if forearm.angle is not None:
        current_forearm = forearm.angle
    else:
        current_forearm = 90
    
    if current_forearm < forearm_deg:
        while current_forearm < forearm_deg:
            current_forearm = min(current_forearm + step_size, forearm_deg)
            forearm.angle = current_forearm
            sleep(delay)
    else:
        while current_forearm > forearm_deg:
            current_forearm = max(current_forearm - step_size, forearm_deg)
            forearm.angle = current_forearm
            sleep(delay)
    
    # Move wrist
    if wrist.angle is not None:
        current_wrist = wrist.angle
    else:
        current_wrist = 90
    
    if current_wrist < wrist_deg:
        while current_wrist < wrist_deg:
            current_wrist = min(current_wrist + step_size, wrist_deg)
            wrist.angle = current_wrist
            sleep(delay)
    else:
        while current_wrist > wrist_deg:
            current_wrist = max(current_wrist - step_size, wrist_deg)
            wrist.angle = current_wrist
            sleep(delay)
    
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
            set_angle(movement[0], movement[1], movement[2], movement[3])
            sleep(0.5)  # Small delay to let servo reach position
        except KeyError:
            print("Please enter a valid chess position (a1-h8)")
            
except KeyboardInterrupt:
    print("\nProgram stopped by user")

finally:
    # Optional: return servo to neutral/center when done
    reset_angles()
    print("Servo returned to center position")