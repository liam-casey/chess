
# Location is a 2 length tuple in format (x, y)
class Piece():
    def __init__(self, location, image, color):
        self.color = color
        self.location = location
        self.image = image