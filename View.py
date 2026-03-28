import tkinter as tk
import chess
import time
import random

class ChessboardUI:
    def __init__(self, root, chess_logic):
        self.root = root
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
        self.square_size = 60
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
       
    def setboard(self,chess_logic):    
        # Draw the board
        self.draw_board()
        self.update_board(chess_logic)
        
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
    
    def update_board(self,chess_logic):
        self.root.update()
        self.clear_text("pieces")
        for col in range(8):
            for row in range(8):
                piece = chess_logic.piece_at(chess.square(col, row))
                if piece == None:
                    continue
                x = col * self.square_size + self.square_size // 2
                y = row * self.square_size + self.square_size // 2
                
                self.canvas.create_text(
                    x, y,
                    text=self.symbols[piece.symbol()],
                    font=('Arial', 32, 'bold'),
                    tags = "pieces"
                )
    def write(self,user_text,tag,length):
        canvas_size = self.square_size * self.board_size
        x = canvas_size // 2
        y = canvas_size // 2       
        self.canvas.create_text(
            x, y,
            text=user_text,
            font=('Arial', 32, 'bold'),
            tags = tag
        )
        self.root.update()
        self.delay(length)
        self.clear_text(tag)
        
    def delay(self, length):
        initial = time.time()
        while time.time() < initial + length:
            pass
        
        
if __name__ == "__main__":
    root = tk.Tk()
    bot = chess.Board()
    gui = ChessboardUI(root, bot)
    
    gui.write("Welcome to the Robot vs Human Chess Game, White to go first, once turn is done press 'space bar' to ensure you final move is confirmed","start",3)
    gui.write("LETS START THE GAME IN 5 SECONDS","second_start",5)
    gui.write("LETS BEGIN:","third_start",2)
    gui.setboard(bot)
    gui.root.update()
    gui.delay(2)
    # Game loop

    # Robot goes first (Robot is White)
    legal_moves = list(bot.legal_moves)
    random_index = random.randint(0, len(legal_moves) - 1)
    random_move = legal_moves[random_index]
    bot.push(random_move)
    gui.update_board(bot)
    root.mainloop()


