
#This is a square on a chess board, a square has a boolean white
#a boolean Occupied, and a piece that specifies which piece is on it
#a square also has a string location that defines its position on the board. 


class Square:
    def __init__(self, location, isWhite):
        self.location = location
        self.isWhite = isWhite  # Assign the passed value to the isWhite attribute
        self.occupied = False
        self.piece = None
        
    def occupy(self, piece):
        self.occupied = True
        self.piece = piece

    def vacate(self):
        self.occupied = False
        self.piece = None

