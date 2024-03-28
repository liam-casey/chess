import pygame
from engine import GameState

# TODO: ADD IN A START SCREEN AND END SCREEN (ADDING THE SCREENS THEMSELVES WILL BE EASY)
# TODO: START SCREEN SHOULD SAY WELCOME TO CHESS, CHOOSE IF YOU WANT TWO PLAYER OR ONE PLAYER (EASY TO GET THIS INPUT)
# TODO: SHOULD RUN ONE OF TWO DIFFERENT OPTIONS DEPENDING ON WHAT THEY CHOSE ABOVE (NOT SURE HOW HARD THIS WILL BE)
# TODO: END SCREEN SHOULD DISPLAY WHO WON (EASY TO DO)


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
    pygame.font.init()
    # timer for clock
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    # calls load images
    loadImages()
    # game state class, keeps track of what how the game looks currently
    gameState = GameState(IMAGES, screen)
    running = True
    time_passed = 0
    font = pygame.font.SysFont("Comic Sans MS", 20)
    text = font.render("It's white's turn", False, (0,0,0))
    screen.blit(text, (50, 550))
    # TODO: ADD IN A SCREEN THAT WILL DISPLAY 2 OPTIONS, ONE FOR 2 PLAYER, ONE FOR 1 PLAYER

    
    # main driver of game, while loop that keeps the game running
    while running:
        if gameState.gameOver:
            running = False
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
        time_passed += clock.tick(MAX_FPS)
        if time_passed >= 1000:
            gameState.displayClock()
            time_passed = 0
        if gameState.gameOver:
            running = False
        # displays everything
        pygame.display.flip()
    # TODO: AFTER GAME IS DONE, DISPLAY WHO WON

if __name__ == "__main__":
    main()