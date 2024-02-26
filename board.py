import pygame
import sys


class Board:
    def __init__(self, width):
        assert width > 500
        self.size = (width, width)
        self.screen = screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Chess")
        self.board = pygame.Surface((width - 100, width - 100))
        self.board.fill((255, 206, 158))
        self.draw()

    def draw(self):
        for x in range(0, 8, 2):
            for y in range (0, 8 ,2):
                pygame.draw.rect(self.board, (210, 180, 140), (x*75, y*75, 75, 75))
                pygame.draw.rect(self.board, (210, 180, 140), ((x+1)*75, (y+1)*75, 75, 75))
        self.screen.blit(self.board, (20,20))

    def display(self):
        pygame.display.flip()