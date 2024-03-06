from piece import Piece
class King(Piece):
    def __init__(self, location, moves, image):
        super().__init__(location, moves, image)
        self.has_moved = False

    # is_castle enforces the castle ma
    def trigger_move(self, new_location, is_castle=False):
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



