import tkinter as tk

class ChessboardUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Board")
        
        # Board parameters
        self.square_size = 60
        self.board_size = 8
        self.pieces = {}  # Dictionary to store piece positions
        
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
        
        # Draw the board
        self.draw_board()
        
    def draw_board(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                
                # Alternate black and white
                if (row + col) % 2 == 0:
                    color = 'red' 
                else:
                    color = 'white'
                
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline='gray'
                )
    
    def add_piece(self, row, col, piece):
        x = col * self.square_size + self.square_size // 2
        y = row * self.square_size + self.square_size // 2
        
        # Determine text color based on square color (contrast)
        text_color = 'white' if (row + col) % 2 == 0 else 'black'
        
        text_id = self.canvas.create_text(
            x, y,
            text=piece,
            font=('Arial', 32, 'bold'),
            fill=text_color
        )
        
        self.pieces[(row, col)] = text_id
    
    def move_piece(self, from_row, from_col, to_row, to_col):
        """Move a piece from one square to another"""
        if (from_row, from_col) in self.pieces:
            piece_id = self.pieces[(from_row, from_col)]
            
            x = to_col * self.square_size + self.square_size // 2
            y = to_row * self.square_size + self.square_size // 2
            
            self.canvas.coords(piece_id, x, y)
            
            # Update piece dictionary
            self.pieces[(to_row, to_col)] = piece_id
            del self.pieces[(from_row, from_col)]
    
    def clear_piece(self, row, col):
        """Remove a piece from the board"""
        if (row, col) in self.pieces:
            self.canvas.delete(self.pieces[(row, col)])
            del self.pieces[(row, col)]

if __name__ == "__main__":
    root = tk.Tk()
    gui = ChessboardUI(root)
    root.mainloop()
