class Pawn:
    def __init__(self,location, moves, image):
        self.location = location
        self.moves = moves
        self.image = image

    def move(startingpos,endingpos):
        #if pawn hasnt moved, valid moves are y-1 or y-2 for white pawns
        #or y+1 or y+2 for black pawns  
    def Attack(startingpos,endingpos):
        #for white pawns if piece of the other color is at (y-1, x+1 or x-1) pawn can takes
        #for black pawns if piece of the other color is at (y+1, x-1 or x+1) pawn can takes