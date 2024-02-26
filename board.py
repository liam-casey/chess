import pygame
from square import Square  

class Board:     
    def __init__(self):         
        self.width = 800         
        self.size = (self.width, self.width)         
        self.screen = pygame.display.set_mode(self.size)         
        pygame.display.set_caption("Chess")         
        self.board = pygame.Surface((self.width - 100, self.width - 100))         
        self.board.fill((255, 206, 158))         
        self.initialize_board()  # Correct indentation here
        self.draw()  # Correct indentation here

    def initialize_board(self):  # Correct indentation here
        self.squares = [[None] * 8 for _ in range(8)]
        for x in range(8):             
            for y in range(8):                 
                is_white = (x + y) % 2 == 0                 
                location = chr(ord('a') + x) + str(8 - y)                 
                self.squares[x][y] = Square(location, is_white)

    def draw(self):  # Correct indentation here
        for x in range(0, 8, 2):             
            for y in range(0, 8, 2):                 
                pygame.draw.rect(self.board, (210, 180, 140), (x*75, y*75, 75, 75))                 
                pygame.draw.rect(self.board, (210, 180, 140), ((x+1)*75, (y+1)*75, 75, 75))
        self.screen.blit(self.board, (20, 20))

    def display(self):
        pygame.display.flip()