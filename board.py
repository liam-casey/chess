import pygame
from pieces.rook import Rook
from pieces.pawn import Pawn
from pieces.queen import Queen
from pieces.king import King
from pieces.knight import Knight
from pieces.bishop import Bishop

class Board:     
    def __init__(self, images, screen):    
        # intialize all of pieces with the pieces in the pieces folder
        self.IMAGES = images
        self.font = pygame.font.SysFont("Comic Sans MS", 20)
        self.screen = screen

        # The pieces in the board should no longer be strings, they should be a piece object 
        # black_rook1 = Rook((0,0), self.IMAGES["black_rook"], "black")
        # black_knight1 = Knight((0,1), self.IMAGES["black_knight"], "black")
        # black_bishop1 = Bishop((0,2), self.IMAGES["black_bishop"], "black")
        # black_queen = Queen((0,3), self.IMAGES["black_queen"], "black")
        # black_king = King((0,4), self.IMAGES["black_king"], "black")
        # black_bishop2 = Bishop((0,5), self.IMAGES["black_bishop"], "black")
        # black_knight2 = Knight((0,6), self.IMAGES["black_knight"], "black")
        # black_rook2 = Rook((0,7), self.IMAGES["black_rook"], "black")
        # black_pawn1 = Pawn((1, 0), self.IMAGES["black_pawn"], "black",self)
        # black_pawn2 = Pawn((1, 1), self.IMAGES["black_pawn"], "black",self)
        # black_pawn3 = Pawn((1, 2), self.IMAGES["black_pawn"], "black",self)
        # black_pawn4 = Pawn((1, 3), self.IMAGES["black_pawn"], "black",self)
        # black_pawn5 = Pawn((1, 4), self.IMAGES["black_pawn"], "black",self)
        # black_pawn6 = Pawn((1, 5), self.IMAGES["black_pawn"], "black",self)
        # black_pawn7 = Pawn((1, 6), self.IMAGES["black_pawn"], "black",self)
        # black_pawn8 = Pawn((1, 7), self.IMAGES["black_pawn"], "black",self)

        # white_rook1 = Rook((7,0), self.IMAGES["white_rook"], "white")
        # white_knight1 = Knight((7,1), self.IMAGES["white_knight"], "white")
        # white_bishop1 = Bishop((7,2), self.IMAGES["white_bishop"], "white")
        # white_queen = Queen((7,3), self.IMAGES["white_queen"], "white")
        # white_king = King((7,4), self.IMAGES["white_king"], "white")
        # white_bishop2 = Bishop((7,5), self.IMAGES["white_bishop"], "white")
        # white_knight2 = Knight((7,6), self.IMAGES["white_knight"], "white")
        # white_rook2 = Rook((7,7), self.IMAGES["white_rook"], "white")
        # white_pawn1 = Pawn((6, 0), self.IMAGES["white_pawn"], "white",self)
        # white_pawn2 = Pawn((6, 1), self.IMAGES["white_pawn"], "white",self)
        # white_pawn3 = Pawn((6, 2), self.IMAGES["white_pawn"], "white",self)
        # white_pawn4 = Pawn((6, 3), self.IMAGES["white_pawn"], "white",self)
        # white_pawn5 = Pawn((6, 4), self.IMAGES["white_pawn"], "white",self)
        # white_pawn6 = Pawn((6, 5), self.IMAGES["white_pawn"], "white",self)
        # white_pawn7 = Pawn((6, 6), self.IMAGES["white_pawn"], "white",self)
        # white_pawn8 = Pawn((6, 7), self.IMAGES["white_pawn"], "white",self)

        # This is used for testing to make sure all pieces are working properly
        # white_rook3 = Rook((5,4), self.IMAGES["white_rook"], "white")
        # white_queen2 = Queen((4,4), self.IMAGES["white_queen"], "white")

        # self.board = [
        #     [black_rook1, black_knight1, black_bishop1, black_queen, black_king, black_bishop2, black_knight2, black_rook2],
        #     [black_pawn1, black_pawn2, black_pawn3, black_pawn4, black_pawn5, black_pawn6, black_pawn7, black_pawn8],
        #     ["", "", "", "", "", "", "", ""],
        #     ["", "", "", "", "", "", "", ""],
        #     ["", "", "", "", "", "", "", ""],
        #     ["", "", "", "", "", "", "", ""],
        #     [white_pawn1, white_pawn2, white_pawn3, white_pawn4, white_pawn5, white_pawn6, white_pawn7, white_pawn8],
        #     [white_rook1, white_knight1, white_bishop1, white_queen, white_king, white_bishop2, white_knight2, white_rook2]
        #     ]
        # top left = 0,0
        # bottom left = 7,0
        # top right = 0,7
        # bottom right = 7,7
        white_pawn1 = Pawn((1,7), self.IMAGES['white_pawn'], "white",self)
        self.board = [
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", white_pawn1],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""]
            ]

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
                    screen.blit(piece.get_image(), pygame.Rect(col*screen_size, row*screen_size, screen_size, screen_size))
        text = self.font.render("White", False, (0,0,0))
        screen.blit(text, (525, 10))
        text = self.font.render("Black", False, (0,0,0))
        screen.blit(text, (615, 10))
    
    # returns what piece is on that space
    def getPiece(self, startPos):
        return self.board[startPos[0]][startPos[1]]
    
    # updates the 8 by 8 array with the given move
    def updateBoard(self, startPos, endPos):
        # clear the board
        surface = pygame.Surface((512,512))
        surface.fill((255,255,255))
        self.screen.blit(surface, pygame.Rect(0, 0, 512, 512))
        piece = self.board[startPos[0]][startPos[1]]
        # update pieces position field
        piece.update_location(endPos)
        # set the startPos to nothing
        self.board[startPos[0]][startPos[1]] = ""
        # set the endPos to the piece moved
        self.board[endPos[0]][endPos[1]] = piece