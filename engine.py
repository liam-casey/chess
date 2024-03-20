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
    
    # checks to see if En Passant is a viable move
    # TODO
    def enPassant(self, piece):
        # rules for en passant
        # the enemy pawn advanced two squares on the previous turn;
        # the capturing pawn attacks the square that the enemy pawn passed over
        pass
    
    # checks to see if En Passant is a viable move
    # coordinates go y, x in location var
    # TODO
    def castle(self, piece):
        # Neither the king nor the rook has previously moved.
        if (piece.King.has_moved == False) and (piece.Rook.has_moved == False):
            # There are no pieces between the king and the rook.
            if () and ():
                # The king is not currently in check.
                if self.checkCheckMate == False:
                    # The king does not pass through or finish on a square that is attacked by an enemy piece
                    if (): 
                        return True



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
        
        # bishop now works
        if isinstance(piece, Bishop):
            print("is bishop")
            dy = abs(startPos[0] - endPos[0])
            dx = startPos[1] - endPos[1]
            count = 1
            while count < dy:
                # down left
                if dx > 0 and endPos[0] > startPos[0]:
                    if self.board.getPiece((endPos[0] - count, endPos[1] + count)) != "":
                        return False
                # up left
                elif dx > 0 and endPos[0] < startPos[0]:
                    if self.board.getPiece((startPos[0] - count, startPos[1] - count)) != "":
                        return False
                # down right
                # doesn't work
                elif dx < 0 and endPos[0] > startPos[0]:
                    if self.board.getPiece((endPos[0] - count, endPos[1] - count)) != "":
                        return False
                # up right
                # doenst work
                else:
                    if self.board.getPiece((startPos[0] - count, startPos[1] + count)) != "":
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
                while count < dy:
                    # down left
                    if dx > 0 and endPos[0] > startPos[0]:
                        if self.board.getPiece((endPos[0] - count, endPos[1] + count)) != "":
                            return False
                    # up left
                    elif dx > 0 and endPos[0] < startPos[0]:
                        if self.board.getPiece((startPos[0] - count, startPos[1] - count)) != "":
                            return False
                    # down right
                    elif dx < 0 and endPos[0] > startPos[0]:
                        if self.board.getPiece((endPos[0] - count, endPos[1] - count)) != "":
                            return False
                    # up right
                    else:
                        if self.board.getPiece((startPos[0] - count, startPos[1] + count)) != "":
                            return False
                    count = count + 1
                return True
            dx = abs(dx)
            if dy == 0:
                count = 1
                while count < dx:
                    tup = (endPos[0], max(startPos[1], endPos[1]) - count)
                    if self.board.getPiece(tup) != "":
                        return False
                    count = count + 1
                return True
            else:
                count = 1
                while count < dy:
                    tup = (max(startPos[0], endPos[0]) - count, endPos[1])
                    if self.board.getPiece(tup) != "":
                        return False
                    count = count + 1
                return True
        
        # TODO: IMPLEMENT PAWN
        # Pawn should check the space in front of it or two spaces in front
        if isinstance(piece, Pawn):
            dy = abs(endPos[0] - startPos[0])
            if dy > 1:
                if self.board.getPiece((endPos[0] - 1, endPos[1])) != "":
                    return False
                if self.board.getPiece((endPos[0]), endPos[1]) != "":
                    return False
            if self.board.getPiece((endPos[0], endPos[1])) != "":
                return False
            return True
        # King doesn't matter, will be accounted for above in the move function when checking to see it doesn't take its own pieces
        if isinstance(piece, King):
            return True
        # Knight can hop over other pieces
        if isinstance(piece, Knight):
            return True

    