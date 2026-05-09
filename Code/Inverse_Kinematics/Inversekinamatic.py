import json
import math
with open('measurements.json', 'r') as file:
    data = json.load(file)

with open('inversekinematics.json', 'r') as file:
    degree_data = json.load(file)

new_data = []
servo_arms_length = 14.5

for key in data:
    new_data = []
    square_values = data[key]
    x = square_values[0]
    y = square_values[1]
    z = square_values[2]
    # xy-plane angle
    xy_angle_radian = math.atan2(y,x)
    xy_angle_degrees = math.degrees(xy_angle_radian)
    new_data.append(int(xy_angle_degrees)) # Hub servo
    if "b" in key:
        print(key + " " + str(90-xy_angle_degrees))
    xy_dist = math.sqrt(x**2+y**2)
    max_dist = math.sqrt(xy_dist**2+z**2)

    #Triangle angle finder
    cos_main = (servo_arms_length**2 + servo_arms_length**2 - max_dist**2) / (2 * servo_arms_length* servo_arms_length)
    print(cos_main)
    if cos_main >1 or cos_main<-1:
        print(max_dist)
        print(x)
        print(y)
        print(z)
        cos_main = 1
        new_data.append("CHECK")
    angle_C = math.acos(cos_main)  # Returns radians
    forearm_degree_inside = math.degrees(angle_C)
    smaller_angles = (180 - forearm_degree_inside)/2

    #arm movement
    new_data.append(int(135 - smaller_angles))

    #forearm movement
    new_data.append(int(180-forearm_degree_inside))

    #grabber movement
    new_data.append(int(smaller_angles))

    degree_data[key] = new_data


print(str(new_data[0]) + " " + str(new_data[-1])) # use these to set max and min abnlges of hub servo
with open('inversekinematics.json', 'w') as file:
    json.dump(degree_data,file,indent = 4)