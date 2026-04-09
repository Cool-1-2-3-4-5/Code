from gpiozero import AngularServo
from time import sleep

def smooth_set_angle(servo, target_angle, step_size=1, delay=0.05):
    if not (0 <= target_angle <= 180):
        return
    
    if servo.angle is not None:
        current_angle = servo.angle
    else:
        current_angle = 90
    
    if current_angle < target_angle:
        while current_angle < target_angle:
            current_angle = min(current_angle + step_size, target_angle)
            servo.angle = current_angle
            sleep(delay)
    else:
        while current_angle > target_angle:
            current_angle = max(current_angle - step_size, target_angle)
            servo.angle = current_angle
            sleep(delay)

def grab_piece(servo, max_angle=30):
    smooth_set_angle(servo, max_angle)

def reset_grabber(servo, reset_angle=0):
    smooth_set_angle(servo, reset_angle)

def come_back_to_nor(arm, forearm, wrist, arm_reset=30, forearm_reset=30, wrist_reset=30):
    smooth_set_angle(arm, arm_reset)
    smooth_set_angle(forearm, forearm_reset)
    smooth_set_angle(wrist, wrist_reset)
    
def move_joints(shoulder, arm, forearm, wrist, shoulder_reset, arm_reset, forearm_reset, wrist_reset):
    smooth_set_angle(shoulder, shoulder_reset)
    smooth_set_angle(arm, arm_reset)
    smooth_set_angle(forearm, forearm_reset)
    smooth_set_angle(wrist, wrist_reset)
    


def robotTurnToPlay(move_type, shoulder, arm, forearm, wrist, gripper, go_to_pos, return_to_pos):
    if move_type == "Piece Won":
        move_joints(shoulder,arm,forearm,wrist,return_to_pos[0],return_to_pos[1],return_to_pos[2],return_to_pos[3])
        grab_piece(gripper)
        sleep(0.5)
        come_back_to_nor(arm, forearm, wrist)
        sleep(0.5)
        move_joints(shoulder,arm,forearm,wrist,30,30,30,30)
        sleep(0.5)
        reset_grabber(gripper)
        sleep(0.5)
        move_joints(shoulder,arm,forearm,wrist,go_to_pos[0],go_to_pos[1],go_to_pos[2],go_to_pos[3])
        grab_piece(gripper)
        sleep(0.5)
        come_back_to_nor(arm,forearm,wrist)
        sleep(0.5)
        move_joints(shoulder,arm,forearm,wrist,return_to_pos[0],return_to_pos[1],return_to_pos[2],return_to_pos[3])
        reset_grabber(gripper)
    else:    
        move_joints(shoulder,arm,forearm,wrist,go_to_pos[0],go_to_pos[1],go_to_pos[2],go_to_pos[3])
        grab_piece(gripper)
        sleep(0.5)
        come_back_to_nor(arm, forearm, wrist)
        sleep(0.5)
        move_joints(shoulder,arm,forearm,wrist,return_to_pos[0],return_to_pos[1],return_to_pos[2],return_to_pos[3])
        reset_grabber(gripper)