from gpiozero import AngularServo
from time import sleep

def grab_piece(servo,max_angle = 30):
    servo.angle = max_angle

def reset_grabber(servo,reset_angle = 0):
    servo.angle= reset_angle

def come_back_to_nor(arm,forearm,wrist,arm_reset = 30,forearm_reset=30,wrist_reset=30):
    arm.angle = arm_reset
    forearm.angle = forearm_reset
    wrist.angle = wrist_reset
    
def move_joints(shoulder,arm,forearm,wrist,shoulder_reset,arm_reset,forearm_reset,wrist_reset):
    shoulder.angle = shoulder_reset
    arm.angle = arm_reset
    forearm.angle = forearm_reset
    wrist.angle = wrist_reset
    


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