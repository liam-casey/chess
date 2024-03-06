from piece import Piece
class King(Piece):
    def __init__(self, location, image, color):
        super().__init__(location, image, color)
        self.has_moved = False

    # is_castle enforces the castle ma
    def move(self, new_location, is_castle=False):
        d_x = abs(new_location[0] - self.location[0])
        d_y = abs(new_location[1] - self.location[1])
        if is_castle:
            if self.has_moved:
                return False
            else:
                # assume the board is valid for a castle
                self.location = new_location
                return True
        if (2 > d_x >= 0) and (2 > d_y >=0):
            self.has_moved = True
            self.location = new_location
            return True

    # function takes in position after a piece has been moved and reassigns the ending location
    # as the current location
    def update_location(self, endPos):
        self.location = endPos



