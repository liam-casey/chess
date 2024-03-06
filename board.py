import pygame
from square import Square  

class Board:     
    def __init__(self, images):    
        # intialize all of pieces with the pieces in the pieces folder
        # The pieces in the board should no longer be strings, they should be a piece object    
        self.board = [
            ["black_rook", "black_knight", "black_bishop", "black_queen", "black_king", "black_bishop", "black_knight", "black_rook"],
            ["black_pawn", "black_pawn", "black_pawn", "black_pawn", "black_pawn", "black_pawn", "black_pawn", "black_pawn"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["white_pawn", "white_pawn", "white_pawn", "white_pawn", "white_pawn", "white_pawn", "white_pawn", "white_pawn"],
            ["white_rook", "white_knight", "white_bishop", "white_queen", "white_king", "white_bishop", "white_knight", "white_rook"]
            ]
        self.IMAGES = images

    # This function draws the board given the screen and screen size
    def drawBoard(self, screen, screen_size):
        # these are the tile colors
        colors = [pygame.Color("white"), pygame.Color("gray")]
        # 8 by 8 board
        for row in range(8):
            for col in range(8):
                # get the color for the specific tile
                color = colors[((row+col) % 2)]
                # draw  it
                pygame.draw.rect(screen, color, pygame.Rect(col*screen_size, row*screen_size, screen_size, screen_size))
                # get the piece at the specific row/col
                piece = self.board[row][col]
                # if its not empty, draw the piece
                if piece != "":
                    screen.blit(self.IMAGES[piece], pygame.Rect(col*screen_size, row*screen_size, screen_size, screen_size))
    
    # returns what piece is on that space
    def getPiece(self, startPos):
        return self.board[startPos[0]][startPos[1]]
    
    # updates the 8 by 8 array with the given move
    def updateBoard(self, startPos, endPos):
        piece = self.board[startPos[0]][startPos[1]]
        # update pieces position field
        self.board[startPos[0]][startPos[1]] = ""
        self.board[endPos[0]][endPos[1]] = piece
        