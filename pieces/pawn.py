from piece import Piece
class Pawn(Piece):
    def __init__(self, location, image, color):
        super().__init__(location, image, color)
        self.on_back_rank = True
        self.has_moved = False

    # is_taking is an optional flag which allows a diagonal 1x1 move
    def move(self, new_location, is_taking=False):
        d_x = abs(new_location[0] - self.location[0])
        d_y = new_location[1] - self.location[1] # should be positive, cant go back
        if is_taking:
            if d_x != 1 or d_y != 1:
                return False
            else:
                self.on_back_rank = False
                return True
        if d_x != 0:
            return False
        if d_y != 1:
            if self.on_back_rank and d_y == 2:
                self.on_back_rank = False
                return True
            else:
                return False
        self.on_back_rank = False
        return True

    # function takes in position after a piece has been moved and reassigns the ending location
    # as the current location
    def update_location(self, endPos):
        self.location = endPos
        self.has_moved = True
