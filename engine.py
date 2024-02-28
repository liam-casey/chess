from board import Board

# This class is responsible for storing all of the information about the current state of the game. It will be resposible for checking
# if a move is valid as well.

# The board can probably be initialized in its own seperate board class
# the pieces themselves can also probably be put in a seperate class as well, which would be initialized in the board class
class GameState:
    def __init__(self, images):
        # this creates a starting board, the "" are empty spaces
        self.board = Board(images)
        # white goes first
        self.whiteToMove = True
    
    def Move(self, startPos, endPos):
        piece = self.board[startPos[0]][startPos[1]]
        # check to see if the piece is the right color
    

    def checkCheckMate():
        pass

    