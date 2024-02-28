import pygame
from square import Square  

class Board:     
    def __init__(self, images):         
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

    def drawBoard(self, screen, screen_size):
        colors = [pygame.Color("white"), pygame.Color("gray")]
        for row in range(8):
            for col in range(8):
                color = colors[((row+col) % 2)]
                pygame.draw.rect(screen, color, pygame.Rect(col*screen_size, row*screen_size, screen_size, screen_size))
                piece = self.board[row][col]
                if piece != "":
                    screen.blit(self.IMAGES[piece], pygame.Rect(col*screen_size, row*screen_size, screen_size, screen_size))