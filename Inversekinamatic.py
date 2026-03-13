import json
import math
with open('measurements.json', 'r') as file:
    data = json.load(file)
for key in data:
    new_data = []
    square_values = data[key]
    x = square_values[0]
    y = square_values[1]
    z = square_values[2]
    # xy-plane angle
    xy_angle_radian = math.atan2(x,y)
    xy_angle_degrees = math.degrees(xy_angle_radian)
    xy_angle_degrees = -1 * xy_angle_degrees
    new_data.append(xy_angle_degrees) # Maingear servo





# main_data = []
# multiplier = 0
# m_data = ["a","b","c","d","e","f","g","h"]
# for key in data:
#     new_data = [0,0,0]
#     multiplier = m_data.index(key[0])
#     multi_sec = int(key[1])-1
#     new_data[0] = round(-9.8 + multi_sec*2.8, 2)
#     new_data[1] = round(11 + multiplier*2.8, 2)
#     new_data[2] = 3.5
#     data[key] = new_data
# print("done")

# output_lines = ["{"]
# for rank in range(1, 9):
#     rank_str = str(rank)
#     squares_in_rank = [f"{file}{rank_str}" for file in m_data]
#     rank_entries = [f'"{sq}": {json.dumps(data[sq])}' for sq in squares_in_rank]
#     line = "    " + ", ".join(rank_entries)
#     if rank < 8:
#         line += ","
#     output_lines.append(line)
# output_lines.append("}")

# with open('measurements.json', 'w') as file:
#     file.write("\n".join(output_lines))


# {
#     "a1": [-9.8, 11, 0], "b1": [0, 0, 0], "c1": [0, 0, 0], "d1": [0, 0, 0], "e1": [0, 0, 0], "f1": [0, 0, 0], "g1": [0, 0, 0], "h1": [0, 0, 0],
#     "a2": [-7, 11, 0], "b2": [0, 0, 0], "c2": [0, 0, 0], "d2": [0, 0, 0], "e2": [0, 0, 0], "f2": [0, 0, 0], "g2": [0, 0, 0], "h2": [0, 0, 0],
#     "a3": [-4.2, 11, 0], "b3": [0, 0, 0], "c3": [0, 0, 0], "d3": [0, 0, 0], "e3": [0, 0, 0], "f3": [0, 0, 0], "g3": [0, 0, 0], "h3": [0, 0, 0],
#     "a4": [-1.4, 11, 0], "b4": [0, 0, 0], "c4": [0, 0, 0], "d4": [0, 0, 0], "e4": [0, 0, 0], "f4": [0, 0, 0], "g4": [0, 0, 0], "h4": [0, 0, 0],
#     "a5": [1.4, 11, 0], "b5": [0, 0, 0], "c5": [0, 0, 0], "d5": [0, 0, 0], "e5": [0, 0, 0], "f5": [0, 0, 0], "g5": [0, 0, 0], "h5": [0, 0, 0],
#     "a6": [4.2, 11, 0], "b6": [0, 0, 0], "c6": [0, 0, 0], "d6": [0, 0, 0], "e6": [0, 0, 0], "f6": [0, 0, 0], "g6": [0, 0, 0], "h6": [0, 0, 0],
#     "a7": [7, 11, 0], "b7": [0, 0, 0], "c7": [0, 0, 0], "d7": [0, 0, 0], "e7": [0, 0, 0], "f7": [0, 0, 0], "g7": [0, 0, 0], "h7": [0, 0, 0],
#     "a8": [9.8, 11, 0], "b8": [0, 0, 0], "c8": [0, 0, 0], "d8": [0, 0, 0], "e8": [0, 0, 0], "f8": [0, 0, 0], "g8": [0, 0, 0], "h8": [0, 0, 0]
# }
