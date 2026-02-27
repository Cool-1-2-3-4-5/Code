import gpiozero as Servo

class newServo(Servo):
    def move_to_pos(self,degrees):
        self.val = (degrees/90.0)-1

rotate = newServo(1)
rotate.move_to_pos(90)