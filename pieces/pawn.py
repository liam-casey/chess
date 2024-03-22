from piece import Piece

class Pawn(Piece):
    def __init__(self, location, image, color):
        super().__init__(location, image, color)
        self.on_back_rank = True
        self.has_moved = False
    def update_location(self, endPos):
        self.location = endPos
        self.has_moved = True    

    def move(self, new_location):
        d_x = abs(new_location[1] - self.location[1])
        d_y = new_location[0] - self.location[0]

        if self.color == "white":
            direction = -1  # White pawns move upwards (positive y direction)
        else:
            direction = 1  # Black pawns move downwards (negative y direction)

        if d_x != 0:
            return False  # Pawns can only move vertically


        if d_y == direction:
            print("in dy if statement")
            return True
            
        elif not self.has_moved and d_y == 2 * direction:
            return True
        else:
            return False
        