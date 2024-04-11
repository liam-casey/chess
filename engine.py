import pygame
import copy
from board import Board
from pieces.rook import Rook
from pieces.pawn import Pawn
from pieces.queen import Queen
from pieces.king import King
from pieces.knight import Knight
from pieces.bishop import Bishop
from find_check import * 


# TODO: FIND A WAY TO IMPLEMENT CHECKMATE
# TODO: Implement an AI - Maybe in here, maybe in run, not sure yet




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
        # time for black and white, if time runs out, game over
        self.whiteMinutes = 5
        self.whiteSeconds = 0
        self.blackMinutes = 5
        self.blackSeconds = 0
        # taken pieces
        self.whiteTaken = []
        self.blackTaken = []
        self.font = pygame.font.SysFont('Comic Sans MS', 20)
        self.gameOver = False
        self.winner = "" # could be black or white
        self.winCon = "" # could be checkMate or staleMate
    
    # This function is responsible for determining whether or not a move is valid and also when a move is valid,
    # then it should carry out the move and update the board.
    def Move(self, startPos, endPos):
        # clear off the area that displays who's turn it is
        surface = pygame.Surface((450,25))
        surface.fill((255,255,255))
        self.screen.blit(surface, pygame.Rect(50, 550, 450, 30))
        # if the position is outside of the board, then just return and say it's the same person's turn
        if startPos[0] > 7 or startPos[1] > 7:
            if self.whiteToMove:
                text = self.font.render("It's white's turn", False, (0,0,0))
                self.screen.blit(text, (50, 550))
                return
            else: 
                text = self.font.render("It's black's turn", False, (0,0,0))
                self.screen.blit(text, (50, 550))
                return
        # if the position is outside of the board, then just return and say it's the same person's turn
        if endPos[0] > 7 or endPos[1] > 7:
            if self.whiteToMove:
                text = self.font.render("It's white's turn", False, (0,0,0))
                self.screen.blit(text, (50, 550))
                return
            else: 
                text = self.font.render("It's black's turn", False, (0,0,0))
                self.screen.blit(text, (50, 550))
                return
        # if they didn't move the piece, then just return and say it's the same person's turn
        if startPos == endPos:
            if self.whiteToMove:
                text = self.font.render("It's white's turn", False, (0,0,0))
                self.screen.blit(text, (50, 550))
                return
            else: 
                text = self.font.render("It's black's turn", False, (0,0,0))
                self.screen.blit(text, (50, 550))
                return
        # get the piece at the start position
        piece = self.board.getPiece(startPos)
        # get the piece at the end position
        takenPiece = self.board.getPiece(endPos)
        # checks to see if its a piece being selected
        if piece == "":
            text = self.font.render('Please Select a piece to move', False, (0,0,0))
            self.screen.blit(text, (50, 550))
            return
        # check to see if the move could be enpassent
        if self.enPassant(piece, startPos, endPos):
            if self.whiteToMove:
                self.whiteToMove = False
            else:
                self.whiteToMove = True
            return
        # checks to see if the move could be castle
        if self.castle(piece, startPos, endPos):
            if self.whiteToMove:
                self.whiteToMove = False
            else:
                self.whiteToMove = True
            return
        # makes sure that the taken piece and the moved piece aren't the same color
        if takenPiece != "":
            if piece.get_color() == takenPiece.get_color():
                text = self.font.render("You can't take your own piece", False, (0,0,0))
                self.screen.blit(text, (50,550))
                return
        # if piece is the right color, do the move and update the board, otherwise print something out
        if self.whiteToMove and piece.get_color() == "white":
            # call each individual pieces move function: this returns whether or not a piece can move from it's current position to the endPos
            # Then call noMovingThroughOthers which determines if there are no pieces between the startPos and endPos
            if piece.move(endPos) and self.noMovingThroughOthers(startPos, endPos, piece):
                # Make sure that the move you make won't put it into check
                if self.noMovingIntoCheck(startPos, endPos, "white") != True:
                    # if a pawn has movedTwo, updated bool in pawn piece: used for enpassent
                    if isinstance(piece, Pawn) and abs(endPos[0] - startPos[0]) == 2:
                        piece.movedTwo = True
                    elif isinstance(piece, Pawn):
                        piece.movedTwo = False 
                    # update the board with the valid move
                    self.board.updateBoard(startPos, endPos)
                    # it's now blacks turn
                    self.whiteToMove = False
                    # if the spot wasn't empty, append the taken piece to the list of taken pieces
                    if takenPiece != "":
                        self.blackTaken.append(takenPiece)
                    # check to see if the valid move put the black king in check
                    inCheck = self.checkCheck("black")
                    # find the black king's location
                    for i in range(8):
                        for j in range(8):
                            piece = self.board.getPiece((i, j))
                            if piece != "":
                                if piece.color == "black" and isinstance(piece, King):
                                    kingToCheck = piece
                                    kingLoc = (i,j)
                                    break
                    # check to see if the black king is in checkmate, if so the game is over
                    # inCM = find_checkmate(kingLoc, "black", self)
                    inCM = self.checkCheckMate("black")
                    if inCheck and inCM:
                        self.gameOver = True
                        self.winner = "White"
                        self.winCon = "Check Mate"
                    # elif inCM and not inCheck:
                    #     print("game over black in stale mate")
                    #     self.gameOver = True
                    #     self.winner = "black"
                    #     self.winCon = "Stale Mate"
                    # if the takenPiece is the king, the game is over
                    if isinstance(takenPiece, King):
                        self.gameOver = True
                    piece.has_moved = True
                    # display that it's now black's turn
                    text = self.font.render("It's black's turn", False, (0,0,0))
                    self.screen.blit(text, (50, 550))
                    return
                else:
                    # if your move would've put your king in check, return and make another move
                    text = self.font.render("No putting your king in check", False, (0,0,0))
                    self.screen.blit(text, (50, 550))
                    return
            else:
                # if the move wasn't valid or you couldn't move through others, display it and make another move
                text = self.font.render("This move doesn't work", False, (0,0,0))
                self.screen.blit(text, (50, 550))
                return
        # Same code as white but for black
        elif self.whiteToMove == False and piece.get_color() == "black":
            if piece.move(endPos) and self.noMovingThroughOthers(startPos, endPos, piece):
                if self.noMovingIntoCheck(startPos, endPos, "black") != True:
                    if isinstance(piece, Pawn) and abs(endPos[0] - startPos[0]) == 2:
                        piece.movedTwo = True
                    elif isinstance(piece, Pawn):
                        piece.movedTwo = False
                    self.board.updateBoard(startPos, endPos)
                    self.whiteToMove = True
                    if takenPiece != "":
                        self.whiteTaken.append(takenPiece)
                    inCheck = self.checkCheck("white")
                    for i in range(8):
                        for j in range(8):
                            piece = self.board.getPiece((i, j))
                            if piece != "":
                                if piece.color == "white" and isinstance(piece, King):
                                    kingToCheck = piece
                                    kingLoc = (i,j)
                                    break
                    # inCM = find_checkmate(kingLoc, "white", self)
                    inCM = self.checkCheckMate("white")
                    if inCheck and inCM:
                        self.gameOver = True
                        self.winner = "Black"
                        self.winCon = "Check Mate"
                    # elif inCM and not inCheck:
                    #     print("game over white in stale mate")
                    #     self.gameOver = True
                    #     self.winner = "black"
                    #     self.winCon = "Stale Mate"
                    if isinstance(takenPiece, King):
                        self.gameOver = True
                    piece.has_moved = True
                    # display that it's now white's turn
                    text = self.font.render("It's white's turn", False, (0,0,0))
                    self.screen.blit(text, (50, 550))
                    return
                else:
                    text = self.font.render("No putting your king in check", False, (0,0,0))
                    self.screen.blit(text, (50, 550))
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
                return
            else: 
                text = self.font.render("It's black's turn", False, (0,0,0))
                self.screen.blit(text, (50, 550))
                return
    
    # Displays all of the taken pieces to the side of the board
    # It takes in a screen and the width of the screen. The screen is used to display the pieces
    # The width is used to get where each piece should be displayed
    def showTaken(self, screen, WIDTH):
        for i in range(1, len(self.blackTaken) + 1):
            screen.blit(self.blackTaken[i - 1].get_image(), pygame.Rect(525, i * (WIDTH/15 + 5), WIDTH/16, WIDTH/16))
        for i in range(1, len(self.whiteTaken) + 1):
            screen.blit(self.whiteTaken[i - 1].get_image(), pygame.Rect(615, i * (WIDTH/15 + 5), WIDTH/16, WIDTH/16))
    
    # checks to see if En Passant is a viable move
    def enPassant(self, piece, startPos, endPos):
        # rules for en passant
        # the enemy pawn advanced two squares on the previous turn;
        # the capturing pawn attacks the square that the enemy pawn passed over
        # Get the piece at the end position
        newSpot = self.board.getPiece(endPos)
        takenPiece = self.board.getPiece((startPos[0], endPos[1]))
        # Check if the piece is a pawn and it's capturing another pawn en passant
        if isinstance(piece, Pawn) and newSpot == "" and abs(startPos[0] - endPos[0]) == 1 and abs(startPos[1] - endPos[1]) == 1 and isinstance(takenPiece, Pawn):
            # Check if the end position is a valid en passant capture square
            if piece.movedTwo:
                # Perform the en passant capture
                self.board.updateBoard(startPos, endPos)
                # Remove the captured pawn from the board
                if piece.get_color() == "white":
                    self.blackTaken.append(self.board.getPiece((startPos[0], endPos[1])))
                    self.board.board[endPos[0]][endPos[1]] = piece
                    piece.update_location(endPos)
                    self.board.board[startPos[0]][endPos[1]] = ""
                    piece.movedTwo = False
                    # self.board.updateBoard(startPos, (startPos[0], endPos[1]))
                else:
                    self.whiteTaken.append(self.board.getPiece((startPos[0], endPos[1])))
                    self.board.board[endPos[0]][endPos[1]] = piece
                    piece.update_location(endPos)
                    self.board.board[startPos[0]][endPos[1]] = ""
                    piece.movedTwo = False
                    # self.board.updateBoard(startPos[0], endPos[1])
                return True
        return False  
    
    # promotion function the replacement of a pawn with a new piece when the pawn is moved to its last rank
    # The player replaces the pawn immediately with a queen, rook, bishop, or knight
    def promotion(self, piece, startPos, endPos, screen):
        if isinstance(piece, Pawn):
            if(piece.get_color() == "white" and endPos[0] == 0):
                text = self.font.render("Select a piece to promote to", False, (0,0,0))
                self.screen.blit(text, (50, 650))
                self.screen.blit(Queen, (30, 750))
                self.screen.blit(Rook, (40, 750))
                self.screen.blit(Bishop, (50, 750))
                self.screen.blit(Knight, (60, 750))

                # TODO: replace pawn's space with selected piece
                
                # once a piece has been selected replace the pawn with the selected piece
                if isinstance(piece, Queen):
                    piece.update_location(endPos)
                if isinstance(piece, Rook):
                    piece.update_location(endPos)
                if isinstance(piece, Bishop):
                    piece.update_location(endPos)  
                if isinstance(piece, Knight):
                    piece.update_location(endPos)  
            else:
                text = self.font.render("Select a piece to promote to", False, (0,0,0))
                self.screen.blit(text, (50, 650))
                self.screen.blit(Queen, (30, 750))
                self.screen.blit(Rook, (40, 750))
                self.screen.blit(Bishop, (50, 750))
                self.screen.blit(Knight, (60, 750))

                # TODO: replace pawn's space with selected piece
                
                # once a piece has been selected replace the pawn with the selected piece
                if isinstance(piece, Queen):
                    piece.update_location(endPos)
                    self.board.updateBoard()
                if isinstance(piece, Rook):
                    piece.update_location(endPos)
                if isinstance(piece, Bishop):
                    piece.update_location(endPos)  
                if isinstance(piece, Knight):
                    piece.update_location(endPos) 
                

    # checks to see if castling is a viable move
    # coordinates go y, x in location var
    def castle(self, piece, startPos, endPos):
        # Check if the piece is a king
        if isinstance(piece, King):
            # Check if the king hasn't moved
            if not piece.has_moved:
                # Check if the end position is to the right of the start position
                if endPos[1] > startPos[1]:
                    # Check if there are no pieces between the king and the rook
                    for col in range(startPos[1] + 1, endPos[1]):
                        if self.board.getPiece((startPos[0], col)) != "":
                            return False
                    # Check if the rook exists at the expected position
                    rook = self.board.getPiece((startPos[0], 7))
                    # Check if the rook hasn't moved
                    if isinstance(rook, Rook) and not rook.has_moved:
                        # Update the board for the king and rook's new positions
                        self.board.updateBoard(startPos, endPos)
                        piece.has_moved = True
                        self.board.board[endPos[0]][endPos[1] - 1] = rook
                        rook.update_location((endPos[0], endPos[1] - 1))
                        rook.has_moved = True
                        return True
                # Check if the end position is to the left of the start position
                elif endPos[1] < startPos[1]:
                    # Check if there are no pieces between the king and the rook
                    for col in range(endPos[1] + 1, startPos[1]):
                        if self.board.getPiece((startPos[0], col)) != "":
                            return False
                    # Check if the rook exists at the expected position
                    rook = self.board.getPiece((startPos[0], 0))
                    # Check if the rook hasn't moved
                    if isinstance(rook, Rook) and not rook.has_moved:
                        # Update the board for the king and rook's new positions
                        self.board.updateBoard(startPos, endPos)
                        piece.has_moved = True
                        self.board.board[endPos[0]][endPos[1] + 1] = rook
                        rook.update_location((endPos[0], endPos[1] + 1))
                        rook.has_moved = True
                        return True
        return False


    # This function takes in a startPos and endPos and a piece.
    # It checks what kind of piece is moving, and then depending on the piece, will check the spots between
    # The startPos and endPos to make sure that those spaces are empty and can be moved over
    # The knight and king are the only expceptions
    # Knight can jump over other pieces and king only moves one spot
    def noMovingThroughOthers(self, startPos, endPos, piece):
        # Rook working as intended
        movedPiece = self.board.getPiece(startPos)
        takenPiece = self.board.getPiece(endPos)
        if takenPiece != "":
            if movedPiece.color == takenPiece.color:
                return False
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

        # queen is just the bishop code and the rook code put together
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
        
        # Pawn should check the space in front of it or two spaces in front
        if isinstance(piece, Pawn):
            dy = abs(endPos[0] - startPos[0])
            dx = abs(endPos[1] - startPos[1])
            if dx == 1 and dy == 1:
                return True
            if dy > 1 and piece.get_color() == 'white':
                if self.board.getPiece((endPos[0] + 1, endPos[1])) != "":
                    return False
            elif dy > 1 and piece.get_color() == 'black': 
                if self.board.getPiece((endPos[0] - 1, endPos[1])) != "":
                    return False
            
            if self.board.getPiece((endPos[0], endPos[1])):
                return False
            
            return True
        # King doesn't matter, will be accounted for above in the move function when checking to see it doesn't take its own pieces
        if isinstance(piece, King):
            return True
        # Knight can hop over other pieces
        if isinstance(piece, Knight):
            return True 

    # This function is called every second by our main function in run
    # it decrements the clock depending on whose turn it is
    # It then displays the new time on the clock
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
        # clears the screen at the position of the different clocks
        surface = pygame.Surface((100,25))
        surface.fill((255,255,255))
        if self.whiteToMove:
            self.screen.blit(surface, pygame.Rect(525, 35, 100, 25))
        else:
            self.screen.blit(surface, pygame.Rect(615, 35, 100, 25))
        # make a string for the white clock
        whiteText = str(self.whiteMinutes) + ":"
        if self.whiteSeconds >= 10:
            whiteText += str(self.whiteSeconds)
        else:
            whiteText = whiteText + "0" + str(self.whiteSeconds)
        # display the white clock
        text = self.font.render(whiteText, False, (0,0,0))
        self.screen.blit(text, (525, 35))
        # create the text for the black clock
        blackText = str(self.blackMinutes) + ":"
        if self.blackSeconds >= 10:
            blackText += str(self.blackSeconds)
        else:
            blackText = blackText + "0" + str(self.blackSeconds)
        # display the black clock
        text = self.font.render(blackText, False, (0,0,0))
        self.screen.blit(text, (615, 35))

    # This function takes in a color, finds the king of the corresponding color
    # It then iterates over the entire board and checks to see if every piece of the opposing color can reach the king in a valid move
    def checkCheck(self, color):
        # This code clears the bottom space that is used to say that a king is in check
        surface = pygame.Surface((450,30))
        surface.fill((255,255,255))
        self.screen.blit(surface, pygame.Rect(50, 650, 450, 30))
        # finds the position of the king of the correct color
        for i in range(8):
            for j in range(8):
                piece = self.board.getPiece((i, j))
                if piece != "":
                    if piece.color == color and isinstance(piece, King):
                        kingToCheck = piece
                        kingLoc = (i,j)
                        break
        # check every piece of the opposing color and see if it can validly move to the kings position
        for i in range(8):
            for j in range(8):
                piece = self.board.getPiece((i,j))
                if piece != "":
                    if piece.color != kingToCheck.color:
                        if piece.move(kingLoc) and self.noMovingThroughOthers((i,j), kingLoc, piece):
                            # display that the king is in check
                            text = self.font.render("The " + color + " King is in Check", False, (0,0,0))
                            self.screen.blit(text, (50, 650))
                            return True
        # king is not in check
        return False
    
    # This function is very similar to checkCheck except its used before you can make a move
    # It "does" the move you want, and checks to see if the opposing color can take your king in the same way CheckCheck does
    # After it checks to see if it puts your king in check, it reverts the changes of the board that it did
    def noMovingIntoCheck(self, startPos, endPos, color):
        # get the pieces
        movedPiece = self.board.getPiece(startPos)
        takenPiece = self.board.getPiece(endPos)
        # update the board
        self.board.updateBoard(startPos, endPos)
        # clear the screen where text for check is displayed
        surface = pygame.Surface((450,30))
        surface.fill((255,255,255))
        self.screen.blit(surface, pygame.Rect(50, 550, 450, 30))
        # get the position of the king
        for i in range(8):
            for j in range(8):
                piece = self.board.getPiece((i, j))
                if piece != "":
                    if piece.color == color and isinstance(piece, King):
                        kingToCheck = piece
                        kingLoc = (i,j)
                        break
        # checks to see if the oppsoing color can take the king validly
        for i in range(8):
            for j in range(8):
                piece = self.board.getPiece((i,j))
                if piece != "":
                    if piece.color != kingToCheck.get_color():
                        if piece.move(kingLoc) and self.noMovingThroughOthers((i,j), kingLoc, piece):
                            # reset the board
                            self.board.board[startPos[0]][startPos[1]] = movedPiece
                            movedPiece.update_location(startPos)
                            # put the taken piece back
                            self.board.board[endPos[0]][endPos[1]] = takenPiece
                            return True
        # reset the board
        self.board.board[startPos[0]][startPos[1]] = movedPiece
        movedPiece.update_location(startPos)
        self.board.board[endPos[0]][endPos[1]] = takenPiece
        return False
    

    # IDEA
    def checkCheckMate(self, color):
        for i in range(8):
            for j in range(8):
                piece = self.board.getPiece((i,j))
                if piece != "":
                    if piece.get_color() == color:
                        for x in range(8):
                            for y in range(8):
                                if piece.move((x, y)) and self.noMovingThroughOthers((i,j), (x,y), piece): 
                                    if self.noMovingIntoCheck((i,j), (x,y), color) == False:
                                        return False
        return True