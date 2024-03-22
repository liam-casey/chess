import pygame
from engine import GameState


# constants
WIDTH = 700
HEIGHT = 700 # size of window
DIMENSION = 8 # size of board
SQ_SIZE = 512 // DIMENSION # size of each square
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
    # calls load images
    loadImages()
    # game state class, keeps track of what how the game looks currently
    gameState = GameState(IMAGES)
    running = True
    squareSelected = ()
    # main driver of game, while loop that keeps the game running
    while running:
        for event in pygame.event.get():
            # checks to see if they closed the window
            if event.type == pygame.QUIT:
                running = False
            # mouse button down, grab a piece
            if event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0]// SQ_SIZE
                row = location[1] // SQ_SIZE
                startPos = (row, col)
            # mouse button up, move the piece to new destination
            if event.type == pygame.MOUSEBUTTONUP:
                location = pygame.mouse.get_pos()
                col = location[0]// SQ_SIZE
                row = location[1] // SQ_SIZE
                endPos = (row, col)
                gameState.Move(startPos, endPos)
        # draw
        gameState.board.drawBoard(screen, SQ_SIZE)
        gameState.showTaken(screen, WIDTH)
        # frame rate
        clock.tick(MAX_FPS)
        # displays everything
        pygame.display.flip()


if __name__ == "__main__":
    main()