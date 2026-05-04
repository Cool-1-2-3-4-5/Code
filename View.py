import tkinter as tk
import chess
import time

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
        self.square_size = 125
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
        self.state = True