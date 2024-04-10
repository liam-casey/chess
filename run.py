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
    font = pygame.font.SysFont("Comic Sans MS", 30)
    text = font.render("Welcome to Chess!", False, (0,0,0))
    screen.blit(text, (220, 50))
    surface = pygame.Surface((200, 200))
    surface.fill((0,0,0))
    screen.blit(surface, pygame.Rect(60, 200, 200, 200))
    surface = pygame.Surface((200, 200))
    surface.fill((0,0,0))
    screen.blit(surface, pygame.Rect(420, 200, 200, 200))
    font = pygame.font.SysFont("Comic Sans MS", 20)
    text = font.render("VS AI", False, (255, 255, 255))
    screen.blit(text, (130, 280))
    text = font.render("VS PLAYER", False, (255, 255, 255))
    screen.blit(text, (470, 280))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                location = pygame.mouse.get_pos()
                if 420 < location[0] and location[0] < 620 and 200 < location[1] and location[1]< 400:
                    screen.fill((255,255,255))
                    runTwoPLayer(screen, clock)
                elif 60< location[0] and location[0] < 260 and  200 < location[1] and location[1] < 400:
                    screen.fill((255,255,255))
                    runAI(screen, clock)
        pygame.display.flip()

def runAI(screen, clock):
    pass
    # displayWinner(screen, )

def runTwoPLayer(screen, clock):
    gameState = GameState(IMAGES, screen)
    running = True
    time_passed = 0
    font = pygame.font.SysFont("Comic Sans MS", 20)
    text = font.render("It's white's turn", False, (0,0,0))
    screen.blit(text, (50, 550))    
    # main driver of game, while loop that keeps the game running
    while running:
        if gameState.gameOver:
            running = False
        for event in pygame.event.get():
            # checks to see if they closed the window
            if event.type == pygame.QUIT:
                running = False
                exit()
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
    displayWinner(screen, clock, gameState.winner, gameState.winCon, "vs player")

def displayWinner(screen, clock, winner, winCon, typeGame):
    screen.fill((255,255,255))
    font = pygame.font.SysFont("Comic Sans MS", 30)
    text = winner + " won by " + winCon + "!"
    displayedText = font.render(text, False, (0,0,0))
    screen.blit(displayedText, (180, 50))
    surface = pygame.Surface((200, 200))
    surface.fill((0,0,0))
    screen.blit(surface, pygame.Rect(60, 200, 200, 200))
    surface = pygame.Surface((200, 200))
    surface.fill((0,0,0))
    screen.blit(surface, pygame.Rect(420, 200, 200, 200))
    font = pygame.font.SysFont("Comic Sans MS", 20)
    text = font.render("Play Again?", False, (255, 255, 255))
    screen.blit(text, (110, 280))
    text = font.render("Exit", False, (255, 255, 255))
    screen.blit(text, (490, 280))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                location = pygame.mouse.get_pos()
                if 420 < location[0] and location[0] < 620 and 200 < location[1] and location[1]< 400:
                    exit()
                elif 60< location[0] and location[0] < 260 and  200 < location[1] and location[1] < 400:
                    screen.fill((255,255,255))
                    if typeGame == "vs player":
                        runTwoPLayer(screen, clock)
                    else:
                        runAI(screen, clock)
        pygame.display.flip()

if __name__ == "__main__":
    main()