
# Location is a 2 length tuple in format (x, y)
class Piece():
    def __init__(self, location, image, color, piece_type):
        self.color = color
        self.location = location
        self.image = image
        self.piece_type = piece_type

    # returns image for each piece
    def get_image(self):
        return self.image
    
    def get_color(self):
        return self.color