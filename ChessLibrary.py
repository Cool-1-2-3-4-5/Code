import chess
from nicegui import ui
bot = chess.Board()
file_path = "output.txt"

# File write happens after every move:
# with open(file_path, 'w') as file:
#     file.write(str(bot))
hashmap = {
    "r":"♜",
    "n":"♞",
    "b":"♝",
    "q":"♛",
    "k":"♚",
    "p":"♟",
    "R":"♖",
    "N":"♘",
    "B":"♗",
    "Q":"♕",
    "K":"♔",
    "P":"♙",
    ".":""
}
status = []
with open(file_path,'r') as file:
    for line in file:
        print(line.strip())
        status.append(line.strip())
print(status)
for row in status:
    row = row.split(" ")
    with ui.row():
        for col in row:
            print(hashmap[col])
            ui.label(hashmap[col])
    print(row)
ui.run()