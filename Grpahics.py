from nicegui import ui
import ChessLibrary as robot


for i in range(1,9):
    num = ""
    for j in range(1,10):
        num += str(i) + str(j)
        num += " "
    ui.label(num).classes("text-blue")
print(robot.bot)

ui.run()
