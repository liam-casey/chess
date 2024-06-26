from piece import Piece

class Pawn(Piece):
    def __init__(self, location, image, color,board):
        super().__init__(location, image, color, 'pawn')
        self.on_back_rank = True
        self.has_moved = False
        self.board = board
        self.movedTwo = False
    def update_location(self, endPos):
        self.location = endPos
        
    def move(self, new_location):
        d_x = abs(new_location[1] - self.location[1])
        d_y = new_location[0] - self.location[0]

        # white pawn case
        if self.color == "white":
            direction = -1  # White pawns move upwards (positive y direction)
            if d_y == -1 and (d_x == 1 or d_x == -1):
                takenPiece = self.board.getPiece(new_location)
                if takenPiece == "":
                    return False  
                elif takenPiece.color != "white":
                    return True
        # black pawn case
        else:
            direction = 1  # Black pawns move downwards (negative y direction)
            if d_y == 1 and (d_x == 1 or d_x == -1):
                takenPiece = self.board.getPiece(new_location)
                if takenPiece == "":
                    return False  
                elif takenPiece.color == "white":
                    return True
        if d_x != 0:
            return False  # Pawns can only move vertically


        if d_y == direction:
            return True
        
        # allows movement forward two spots    
        elif not self.has_moved and d_y == 2 * direction:
            return True
        else:
            return False
    
        