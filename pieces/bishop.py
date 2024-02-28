from piece import Piece
class Bishop(Piece):
    def __init__(self,location, image):
        super().__init(location, image)
        self.has_moved = False
    
    def check_move(self, new_location):
        # equation checks piece movements
        d_x = abs(new_location[]) - 
        d_y = abs(new_location[] - self.location[1])