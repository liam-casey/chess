import pygame

WIDTH = 800

WIN = pygame.display.set_mode((WIDTH,WIDTH))

pygame.display.set_caption("Chess")
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.color = WHITE
        self.occupied = None
    def draw(self, WIN):
        pygame.draw.rect(WIN, self.color, (self.x, self.y, WIDTH/8, WIDTH/8))

def make_grid(rows, width):
    grid = []
    gap = WIDTH / rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i,j,gap)
            grid[i].append(node)
            if(i+j)%2 == 1:
                grid[i][j].color = GREY
    return grid

def draw_grid(win, rows, width):
    gap = width // 8
    for i in range(rows):
        pass