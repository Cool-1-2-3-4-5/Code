from gpiozero import AngularServo
from time import sleep

servo = AngularServo(24, min_angle=0, max_angle=180)

print("Starting servo test...")

try: 
    while True:
        servo.angle = 0
        sleep(1)
        servo.angle = 90
        sleep(1)
        servo.angle = 180
        sleep(1)
except KeyboardInterrupt:
    print("Test stopped.")
    servo.detach()