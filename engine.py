from board import Board
from pieces.rook import Rook
from pieces.pawn import Pawn
from pieces.queen import Queen
from pieces.king import King
from pieces.knight import Knight
from pieces.bishop import Bishop


# REMINDERS - CHANGED ALL OF THE PIECES TO NOT SELF UPDATE, ALL PIECES WILL BE UPDATED VIA UPDATE_POSITION IN BOARD
# NEED TO LOOK AT PAWN/KING/ROOK CLASS
    # PAWN SHOULDN'T UPDATE IF IT HAS MOVED ALREADY, SHOULD USE A DIFFERENT FUNCTION, POSSIBLY IN ENGINE
    # KING AND ROOK NEED TO FIGURE OUT HOW CASTLING WORKS - MAY NEED TO ADJUST SOME FUNCTIONS IN ENGINE
# PAWN STILL DOESN'T WORK



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
        self.whiteTaken = []
        self.blackTaken = []
    
    def Move(self, startPos, endPos):
        if startPos[0] > 7 or startPos[1] > 7:
            # HAVE A DRAW STATEMENT FOR INPUTING IN THE RIGHT AREAS
            return
        if endPos[0] > 7 or endPos[0] > 7:
            return
        if startPos == endPos:
            return
        # check to see if the piece is the right color
        piece = self.board.getPiece(startPos)
        # get the piece at the end position
        takenPiece = self.board.getPiece(endPos)
        # checks to see if its a piece being selected
        if piece == "":
            print("please select a piece to move")
            return
        # makes sure that the taken piece and the moved piece aren't the same color
        if takenPiece != "":
            if piece.get_color() == takenPiece.get_color():
                return
        # if piece is the right color, do the move and update the board, otherwise print something out
        if self.whiteToMove and piece.get_color() == "white":
            if piece.move(endPos) and self.noMovingThroughOthers(startPos, endPos, piece):
                # This code makes sure that the rook can't move through pieces
                self.board.updateBoard(startPos, endPos)
                self.whiteToMove = False
                self.blackTaken.append(takenPiece)
                return
            # else print bad move and return
            else:
                # then print something out that says its not a good move
                print ("This move doesn't work")
                return
        elif self.whiteToMove == False and piece.get_color() == "black":
            # also update this code to update the pieces position, could do this in board as well.
            if piece.move(endPos) and self.noMovingThroughOthers(startPos, endPos, piece):
                self.board.updateBoard(startPos, endPos)
                self.whiteToMove = True
                self.whiteTaken.append(takenPiece)
                return
            else:
                print("BAD MOVE")
                return
        # if it's not your turn, tell the opponent that its the other persons turn
        else:
            if self.whiteToMove:
                print("It's white's turn")
                return
            else: 
                print("It's black's turn")
                return
    
    def showTaken(self):
        pass

    def checkCheckMate(self):
        pass

    def noMovingThroughOthers(self, startPos, endPos, piece):
        # Rook working as intended
        if isinstance(piece, Rook):
            dy = abs(endPos[0] - startPos[0])
            dx = abs(endPos[1] - startPos[1])
            if dy == 0:
                count = 1
                while count < dx:
                    tup = (endPos[0], max(startPos[1], endPos[1]) - count)
                    if self.board.getPiece(tup) != "":
                        return False
                    count = count + 1
            else:
                count = 1
                while count < dy:
                    tup = (max(startPos[0], endPos[0]) - count, endPos[1])
                    if self.board.getPiece(tup) != "":
                        return False
                    count = count + 1
            return True
        
        # bishop is broken when moving upwards, not moving downwards
        if isinstance(piece, Bishop):
            dy = abs(startPos[0] - endPos[0])
            dx = startPos[1] - endPos[1]
            count = 1
            tup = max(startPos, endPos)
            while count < dy:
                if dx > 0:
                    if self.board.getPiece((tup[0] - count, tup[1] + count)) != "":
                        return False
                else:
                    if self.board.getPiece((tup[0] - count, tup[1] - count)) != "":
                        return False
                count = count + 1
            return True

        # queen needs to be updated with code from rook
        # queen also needs to be updated with code from bishop which is now working as intended
        if isinstance(piece, Queen):
            dy = abs(startPos[0] - endPos[0])
            dx = startPos[1] - endPos[1]
            if dy != 0 and dx != 0:
                count = 1
                tup = max(startPos, endPos)
                while count < dy:
                    if dx > 0:
                        if self.board.getPiece((tup[0] - count, tup[1] + count)) != "":
                            print("diagonal 1 is working")
                            return False
                    else:
                        if self.board.getPiece((tup[0] - count, tup[1] - count)) != "":
                            print("diagonal 2 is working")
                            return False
                    count = count + 1
            elif dx == 0:
                i = endPos[0]
                while i > startPos[0] - 1:
                    if self.board.getPiece((i, startPos[1])) != "":
                        print("dx is working")
                        return False
                    i = i - 1
            else:
                dx = abs(endPos[1] - startPos[1])
                i = endPos[1]
                while i > startPos[1] - 1:
                    if self.board.getPiece((startPos[0], i)) != "":
                        print("dy is working")
                        return False
                    i = i - 1
            print("Queen moved success")
            return True
        
        # TODO: IMPLEMENT PAWN
        # Pawn should check the space in front of it or two spaces in front
        if isinstance(piece, Pawn):
            pass
        # King doesn't matter
        if isinstance(piece, King):
            return True
        # Knight can hop over other pieces
        if isinstance(piece, Knight):
            return True

    