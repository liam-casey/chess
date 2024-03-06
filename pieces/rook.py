from piece import Piece
class Rook(Piece):
    def __init__(self,location, image):
        # TODO get rid of color?
        super().__init__(location, image, color)
        self.has_moved = False

    def check_move(self, new_location, is_castle=False):
        # equation checks piece movements
        d_x = abs(new_location[0]) - self.location[0]
        d_y = abs(new_location[1] - self.location[1])

        # firstly check if castling is an option
        if is_castle:
            if self.has_moved:
                return False
            # if all is fine return true
            else:
                self.location = new_location
                return True

        # checks to see if move is strictly vertical or horizontal (respectively)
        if (d_x == 0 and d_y != 0) or (d_x != 0 and d_y == 0):
            self.has_moved = True
            self.location = new_location
            return True
    


