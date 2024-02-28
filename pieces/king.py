from piece import Piece
class King(Piece):
    def __init__(self, location, moves, image):
        super().__init__(location, moves, image)
        self.has_moved = False

    def trigger_move(self, new_location):
        d_x = abs(new_location[0] - self.location[0])
        d_y = abs(new_location[1] - self.location[1])
        if (2 > d_x >= 0) and (2 > d_y >=0):
            self.has_moved = True
