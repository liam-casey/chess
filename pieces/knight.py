from piece import Piece
class Knight(Piece):
    def __init__(self, location, image, color):
        super().__init__(location, image, color)
        self.has_moved = False

    def move(self, new_location):
        d_x = abs(new_location[0] - self.location[0])
        d_y = abs(new_location[1] - self.location[1])

        # Check if the move follows the L-shaped pattern of a knight
        if (d_x == 1 and d_y == 2) or (d_x == 2 and d_y == 1):
            return True
        else:
            return False

    # function takes in position after a piece has been moved and reassigns the ending location
    # as the current location
    def update_location(self, endPos):
        self.location = endPos
        self.has_moved = True