from gpiozero import Device, AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# Set up pigpio pin factory for hardware PWM (reduces servo jitter)
Device.pin_factory = PiGPIOFactory()

# Initialize the servo on GPIO pin 14
# Adjust min_angle, max_angle, min_pulse_width, max_pulse_width as needed for your servo
# MG90S typically works well around 0.5 ms to 2.5 ms for ~0° to 180°
servo = AngularServo(
    23,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.5 / 1000,    # 0.5 ms
    max_pulse_width=2.5 / 1000     # 2.5 ms
)

def set_angle(angle, step_size=1, delay=0.2):
    if 0 <= angle <= 180:
        if servo.angle is not None:
            current_angle = servo.angle
        else:
            current_angle = 90
        
        if current_angle < angle:
            # Move up
            while current_angle < angle:
                current_angle = min(current_angle + step_size, angle)
                servo.angle = current_angle
                sleep(delay)
        else:
            # Move down
            while current_angle > angle:
                current_angle = max(current_angle - step_size, angle)
                servo.angle = current_angle
                sleep(delay)
    else:
        print(f"Angle {angle} is out of range (0-180)")

# Main program loop
print("Servo angle control (0 to 180 degrees)")
print("Enter 'q' or Ctrl+C to quit")

try:
    while True:
        user_input = input("Enter angle (0 to 180): ").strip()
        
        if user_input.lower() in ['q', 'quit', 'exit']:
            print("Exiting...")
            break
            
        try:
            angle = int(user_input)
            set_angle(angle)
            sleep(0.5)  # Small delay to let servo reach position
        except ValueError:
            print("Please enter a valid number between 0 and 180")
            
except KeyboardInterrupt:
    print("\nProgram stopped by user")

finally:
    # Optional: return servo to neutral/center when done
    set_angle(90)
    print("Servo returned to center position")