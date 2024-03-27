import pygame
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
    def __init__(self, images, screen):
        # this creates a starting board, the "" are empty spaces
        self.board = Board(images, screen)
        self.screen = screen
        # white goes first
        self.whiteToMove = True
        self.whiteMinutes = 5
        self.whiteSeconds = 0
        self.blackMinutes = 5
        self.blackSeconds = 0
        self.whiteTaken = []
        self.blackTaken = []
        self.font = pygame.font.SysFont('Comic Sans MS', 20)
        self.gameOver = False
    
    def Move(self, startPos, endPos):
        surface = pygame.Surface((450,25))
        surface.fill((255,255,255))
        self.screen.blit(surface, pygame.Rect(50, 550, 450, 25))
        if startPos[0] > 7 or startPos[1] > 7:
            # HAVE A DRAW STATEMENT FOR INPUTING IN THE RIGHT AREAS
            return
        if endPos[0] > 7 or endPos[0] > 7:
            return
        if startPos == endPos:
            if self.whiteToMove:
                text = self.font.render("It's white's turn", False, (0,0,0))
                self.screen.blit(text, (50, 550))
                # print("It's white's turn")
                return
            else: 
                text = self.font.render("It's black's turn", False, (0,0,0))
                self.screen.blit(text, (50, 550))
                # print("It's black's turn")
                return
        # check to see if the piece is the right color
        piece = self.board.getPiece(startPos)
        # get the piece at the end position
        takenPiece = self.board.getPiece(endPos)
        # checks to see if its a piece being selected
        if piece == "":
            text = self.font.render('Please Select a piece to move', False, (0,0,0))
            self.screen.blit(text, (50, 550))
            # print("please select a piece to move")
            return
        # makes sure that the taken piece and the moved piece aren't the same color
        if takenPiece != "":
            if piece.get_color() == takenPiece.get_color():
                text = self.font.render("You can't take your own piece", False, (0,0,0))
                self.screen.blit(text, (50,550))
                return
        # if piece is the right color, do the move and update the board, otherwise print something out
        if self.whiteToMove and piece.get_color() == "white":
            if piece.move(endPos) and self.noMovingThroughOthers(startPos, endPos, piece):
                # This code makes sure that the rook can't move through pieces
                self.board.updateBoard(startPos, endPos)
                self.whiteToMove = False
                if takenPiece != "":
                    self.blackTaken.append(takenPiece)
                if isinstance(takenPiece, King):
                    self.gameOver = True
                return
            # else print bad move and return
            else:
                # then print something out that says its not a good move
                text = self.font.render("This move doesn't work", False, (0,0,0))
                self.screen.blit(text, (50, 550))
                # print ("This move doesn't work")
                return
        elif self.whiteToMove == False and piece.get_color() == "black":
            # also update this code to update the pieces position, could do this in board as well.
            if piece.move(endPos) and self.noMovingThroughOthers(startPos, endPos, piece):
                self.board.updateBoard(startPos, endPos)
                self.whiteToMove = True
                if takenPiece != "":
                    self.whiteTaken.append(takenPiece)
                if isinstance(takenPiece, King):
                    self.gameOver = True
                return
            else:
                text = self.font.render("This move doesn't work", False, (0,0,0))
                self.screen.blit(text, (50, 550))
                return
        # if it's not your turn, tell the opponent that its the other persons turn
        else:
            if self.whiteToMove:
                text = self.font.render("It's white's turn", False, (0,0,0))
                self.screen.blit(text, (50, 550))
                # print("It's white's turn")
                return
            else: 
                text = self.font.render("It's black's turn", False, (0,0,0))
                self.screen.blit(text, (50, 550))
                # print("It's black's turn")
                return
    
    def showTaken(self, screen, WIDTH):
        for i in range(1, len(self.blackTaken) + 1):
            screen.blit(self.blackTaken[i - 1].get_image(), pygame.Rect(525, i * (WIDTH/15 + 5), WIDTH/16, WIDTH/16))
        for i in range(1, len(self.whiteTaken) + 1):
            screen.blit(self.whiteTaken[i - 1].get_image(), pygame.Rect(615, i * (WIDTH/15 + 5), WIDTH/16, WIDTH/16))

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
        
        # TODO: IMPLEMENT PAWN, NEEDS TO ACCOUNT FOR TAKING
        # Pawn should check the space in front of it or two spaces in front
        if isinstance(piece, Pawn):
            dy = abs(endPos[0] - startPos[0])
            dx = abs(endPos[1] - startPos[1])
            if dx == 1 and dy == 1:
                return True
            if dy > 1:
                if self.board.getPiece((endPos[0] - 1, endPos[1])) != "":
                    return False
                if self.board.getPiece((endPos[0], endPos[1])) != "":
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


    def displayClock(self):
        # if a second has passed and its white's turn, decrement the time
        if self.whiteToMove:
            # if seconds reaches 0, subtract from minutes
            if self.whiteSeconds <= 0:
                self.whiteMinutes = self.whiteMinutes - 1
                self.whiteSeconds = self.whiteSeconds + 60
            self.whiteSeconds = self.whiteSeconds - 1
        elif self.whiteToMove == False:
            if self.blackSeconds <= 0:
                self.blackMinutes = self.blackMinutes - 1
                self.blackSeconds = self.blackSeconds + 60
            self.blackSeconds = self.blackSeconds - 1
        if self.whiteSeconds <= 0 and self.whiteMinutes <= 0:
            self.gameOver = True
            return
        if self.blackMinutes <=0 and self.blackSeconds <=0:
            self.gameOver = True
            return
        # TODO: EDIT THIS CODE TO ONLY ERASE THE CHANGING STUFF
        surface = pygame.Surface((100,25))
        surface.fill((255,255,255))
        if self.whiteToMove:
            self.screen.blit(surface, pygame.Rect(525, 35, 100, 25))
        else:
            self.screen.blit(surface, pygame.Rect(615, 35, 100, 25))
        whiteText = str(self.whiteMinutes) + ":"
        if self.whiteSeconds >= 10:
            whiteText += str(self.whiteSeconds)
        else:
            whiteText = whiteText + "0" + str(self.whiteSeconds)
        text = self.font.render(whiteText, False, (0,0,0))
        self.screen.blit(text, (525, 35))
        blackText = str(self.blackMinutes) + ":"
        if self.blackSeconds >= 10:
            blackText += str(self.blackSeconds)
        else:
            blackText = blackText + "0" + str(self.blackSeconds)
        text = self.font.render(blackText, False, (0,0,0))
        self.screen.blit(text, (615, 35))