import tkinter as tk
import chess
import time
import random

class ChessboardUI:
    def __init__(self, root, chess_logic):
        self.root = root
        self.chess_logic = chess_logic
        self.state = False
        self.symbols = {
            # White pieces (uppercase)
            "K": "♔",  # King
            "Q": "♕",  # Queen
            "R": "♖",  # Rook
            "B": "♗",  # Bishop
            "N": "♘",  # Knight
            "P": "♙",  # Pawn
            # Black pieces (lowercase)
            "k": "♚",  # King
            "q": "♛",  # Queen
            "r": "♜",  # Rook
            "b": "♝",  # Bishop
            "n": "♞",  # Knight
            "p": "♟",  # Pawn
            ".": "",
        }


        # Board parameters
        self.square_size = 110
        self.board_size = 8
        
        # Create canvas
        canvas_size = self.square_size * self.board_size
        self.canvas = tk.Canvas(
            root,
            width=canvas_size,
            height=canvas_size,
            bg='white',
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)
       
    def setboard(self):    
        # Draw the board
        self.draw_board()
        self.update_board()
        
    def draw_board(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                
                if (row + col) % 2 == 0:
                    colour = "#8B4513" 
                else:
                    colour = 'white'
                
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=colour,
                    outline= colour
                )
    def clear_text(self,tag):
        self.canvas.delete(tag)
    
    def update_board(self):
        self.root.update()
        self.clear_text("pieces")
        for col in range(7,-1,-1):
            for row in range(7,-1,-1):
                piece = self.chess_logic.piece_at(chess.square(col, row))
                if piece == None:
                    continue
                else:
                    print(chess.square(col, row))
                x = (7-col) * self.square_size + (self.square_size // 2)
                y = row * self.square_size + (self.square_size // 2)
                
                self.canvas.create_text(
                    x, y,
                    text=self.symbols[piece.symbol()],
                    font=('Arial', 32, 'bold'),
                    tags = "pieces"
                )
    def write(self,user_text,tag,length,font_size, Background = False):
        text_array = user_text.split("\n")
        highest = 0
        canvas_size = self.square_size * self.board_size
        if Background:
            for i in range(len(text_array)):
                if highest < len(text_array[i]):
                    highest = len(text_array[i])
            height = (len(text_array) + (len(text_array) -1)) * font_size + 20
            width =  highest*40
            x1 = (canvas_size - width) // 2
            y1 = (canvas_size // 2) - 2
            x2 = width + ((canvas_size - width) // 2)
            y2 = canvas_size // 2 + (font_size+2)*(len(text_array)) 
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill= '#CBBDBD',
                outline= '#CBBDBD',
                tag = tag
            )
        for i in range(len(text_array)):
            x = canvas_size // 2
            y = canvas_size // 2 + ((font_size+2)*(i+1))       
            self.canvas.create_text(
                x, y,
                text=text_array[i],
                font=('Arial', font_size, 'bold'),
                tags = tag
            )
        self.root.update()
        self.delay(length)
        self.clear_text(tag)
        
    def delay(self, length):
        initial = time.time()
        while time.time() < initial + length:
            pass
    def pressed(self,event):
        print("pressed")
        self.state = True
        
if __name__ == "__main__":
    root = tk.Tk()
    bot = chess.Board()
    gui = ChessboardUI(root, bot)
    gui.write("First set up the board! Enter\nthe four corners of the chess\nboard in any order to continue","setup",3,45)

    gui.setboard()
    gui.root.update()
    gui.delay(2)

    gui.root.bind('<space>',gui.pressed)
    gui.state = False
    while not gui.state:
        gui.root.update()
    gui.chess_logic.push_uci("f2f4")
    gui.update_board()
    if gui.chess_logic.is_check():
        gui.write("Black in Check\n","Check",2,50,True)
    
    gui.root.bind('<space>',gui.pressed)
    gui.state = False
    while not gui.state:
        gui.root.update()
    gui.chess_logic.push_uci("f7f5")
    gui.update_board()
    if gui.chess_logic.is_check:
        gui.write("White in Check\n","Check",2,50,True)
    
    gui.root.bind('<space>',gui.pressed)
    gui.state = False
    while not gui.state:
        gui.root.update()
    gui.chess_logic.push_uci("c2c4")
    gui.update_board()
    if gui.chess_logic.is_check:
        gui.write("Black in Check\n","Check",2,50,True)

    gui.root.bind('<space>',gui.pressed)
    gui.state = False
    while not gui.state:
        gui.root.update()
    gui.chess_logic.push_uci("b8c6")
    gui.update_board()
    if gui.chess_logic.is_check:
        gui.write("White in Check\n","Check",2,50,True)

    gui.root.bind('<space>',gui.pressed)
    gui.state = False
    while not gui.state:
        gui.root.update()
    gui.chess_logic.push_uci("a2a4")
    gui.update_board()
    if gui.chess_logic.is_check:
        gui.write("Black in Check\n","Check",2,50,True)

    gui.root.bind('<space>',gui.pressed)
    gui.state = False
    while not gui.state:
        gui.root.update()
    gui.chess_logic.push_uci("c6b4")
    gui.update_board()
    if gui.chess_logic.is_check:
        gui.write("White in Check\n","Check",2,50,True)

    gui.root.bind('<space>',gui.pressed)
    gui.state = False
    while not gui.state:
        gui.root.update()
    gui.chess_logic.push_uci("d1b3")
    gui.update_board()
    if gui.chess_logic.is_check:
        gui.write("Black in Check\n","Check",2,50,True)

    gui.root.bind('<space>',gui.pressed)
    gui.state = False
    while not gui.state:
        gui.root.update()
    gui.chess_logic.push_uci("b4c2")
    gui.update_board()
    if gui.chess_logic.is_check:
        gui.write("White in Check\n","Check",2,50,True)

    gui.root.bind('<space>',gui.pressed)
    gui.state = False
    while not gui.state:
        gui.root.update()
    gui.chess_logic.push_uci("b3c2")
    gui.update_board()
    if gui.chess_logic.is_check:
        gui.write("Black in Check\n","Check",2,50,True)

    gui.root.bind('<space>',gui.pressed)
    gui.state = False
    while not gui.state:
        gui.root.update()
    gui.chess_logic.push_uci("a7a5")
    gui.update_board()
    if gui.chess_logic.is_check:
        gui.write("White in Check\n","Check",2,50,True)

    # Game loop
    # Robot goes first (Robot is White)
    while not gui.chess_logic.is_checkmate() and not gui.chess_logic.is_stalemate():
        print("Hi")
        gui.root.bind('<space>',gui.pressed)
        gui.state = False
        while not gui.state:
            gui.root.update()
        legal_moves = list(gui.chess_logic.legal_moves)
        random_index = random.randint(0, len(legal_moves) - 1)
        random_move = legal_moves[random_index]
        gui.chess_logic.push_uci("f2f4")
        gui.update_board()
        print(gui.chess_logic)
        gui.write("Black in Check\n","New",2,50,True)
        if not gui.chess_logic.is_checkmate() and not gui.chess_logic.is_stalemate():
            gui.root.bind('<space>',gui.pressed)
            gui.state = False
            while not gui.state:
                gui.root.update()
            legal_moves = list(gui.chess_logic.legal_moves)
            random_index = random.randint(0, len(legal_moves) - 1)
            random_move = legal_moves[random_index]
            gui.chess_logic.push(random_move)
            gui.update_board()
            print("Done")
    gui.root.mainloop()