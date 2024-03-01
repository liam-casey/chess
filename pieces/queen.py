from piece import Piece
class Queen(Piece):
    def __init__(self, location, moves, image):
        super().__init__(location, moves, image)

    def move(self, new_location):
        d_x = abs(new_location[0] - self.location[0])
        d_y = abs(new_location[1] - self.location[1])

        # Check if the move is diagonal, horizontal, or vertical
        if (d_x == d_y) or (d_x == 0 and d_y != 0) or (d_x != 0 and d_y == 0):
            self.location = new_location
            return True
        else:
            return False