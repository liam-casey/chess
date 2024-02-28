import pygame
from engine import GameState


# constants
WIDTH = 600
HEIGHT = 512 # size of window
DIMENSION = 8 # size of board
SQ_SIZE = HEIGHT // DIMENSION # size of each square
MAX_FPS = 60 # max frames per second
IMAGES = {} # dictionary to keep all images

# Takes all pieces and loads all images to matching piece
def loadImages():
    pieces = ["black_rook", "black_knight", "black_bishop", "black_queen", "black_king", "black_pawn", "white_pawn", "white_rook", "white_knight", "white_bishop", "white_queen", "white_king"]
    for piece in pieces:
        IMAGES[piece] = pygame.image.load("images/" + piece + ".png")
    
def main():
    # initialize the screen display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # timer for clock
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    # game state class, keeps track of what how the game looks currently
    gameState = GameState()
    # calls load images
    loadImages()
    running = True
    squareSelected = ()
    # main driver of game, while loop that keeps the game running
    while running:
        for event in pygame.event.get():
            # checks to see if they closed the window
            if event.type == pygame.QUIT:
                running = False
            # mouse button
            if event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0]// SQ_SIZE
                row = location[1] // SQ_SIZE
                print(str(row) + ":" + str(col))
            if event.type == pygame.MOUSEBUTTONUP:
                location = pygame.mouse.get_pos()
                col = location[0]// SQ_SIZE
                row = location[1] // SQ_SIZE
                print(str(row) + ":" + str(col))
        # draw
        drawGameState(screen, gameState)
        # frame rate
        clock.tick(MAX_FPS)
        # displays everything
        pygame.display.flip()


# Can probably get rid of this function and just call Draw Board
def drawGameState(screen, gameState):
    drawBoard(screen, gameState.board)

# Can probably put this function in its own board class
def drawBoard(screen, board):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row+col) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            piece = board[row][col]
            if piece != "":
                screen.blit(IMAGES[piece], pygame.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()