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
        if startPos[0] > 7 or startPos[1] > 7:
            # HAVE A DRAW STATEMENT FOR INPUTING IN THE RIGHT AREAS
            return
        if endPos[0] > 7 or endPos[0] > 7:
            return
        # check to see if the piece is the right color
        piece = self.board.getPiece(startPos)
        # checks to see if its a piece being selected
        if piece == "":
            print("please select a piece to move")
            return
        # if piece is the right color, do the move and update the board, otherwise print something out
        # TODO: IN the future, this if statement will change because instead of strings in the board there will be objects
        if self.whiteToMove and "white" in piece:
            piece = self.board.updateBoard(startPos, endPos)
            self.whiteToMove = False
            return
        elif self.whiteToMove == False and "black" in piece:
            piece = self.board.updateBoard(startPos, endPos)
            self.whiteToMove = True
            return
        else:
            if self.whiteToMove:
                print("It's white's turn")
                return
            else: 
                print("It's black's turn")
                return
    

    def checkCheckMate():
        pass

    