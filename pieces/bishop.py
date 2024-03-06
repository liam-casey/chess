from piece import Piece
class Bishop(Piece):
    def __init__(self,location, image, color):
        # TODO get rid of color?
        super().__init__(location, image, color)
        self.has_moved = False

    def move(self, new_location):
        # equation checks piece movements
        d_x = abs(new_location[0]) - self.location[0] 
        d_y = abs(new_location[1] - self.location[1])
        # checks to see if move is diagonal or no
        if d_x == d_y:
            self.location = new_location
            return True
        else:
            return False

    # function takes in position after a piece has been moved and reassigns the ending location
    # as the current location
    def update_location(self, endPos):
        self.location = endPos