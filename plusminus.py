import pygame, sys, random
from pygame.locals import *
from math import floor, ceil

# Set up pygame.
pygame.init()

# Set up window.
windowSurface = pygame.display.set_mode((500,400), 0, 32)
pygame.display.set_caption('Plus-Minus')

mainClock = pygame.time.Clock()

# Set up the colours.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (69, 136, 255)
RED = (255, 69, 74)
DARK_RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 128, 0)

TILE_COLOUR = (RED, BLUE, WHITE, ORANGE, GREEN)

# Set up the fonts.
basicFont = pygame.font.SysFont(None, 24)

# Set up the text.
PLUS_SIGN = basicFont.render('+', True, WHITE, BLUE)
S_PLUS_SIGN = basicFont.render('+', True, WHITE, GREEN)
MINUS_SIGN = basicFont.render('-', True, WHITE, RED)
S_MINUS_SIGN = basicFont.render('-', True, WHITE, ORANGE)
plusRect = PLUS_SIGN.get_rect()
sPlusRect = S_PLUS_SIGN.get_rect()
minusRect = MINUS_SIGN.get_rect()
sMinusRect = S_MINUS_SIGN.get_rect()

def setToDefault():
    global selectedTile, targetScore, maxTime, timer, score, boardSize, tileSize, frameSize, board

    selectedTile = []
    targetScore = 500
    maxTime = 200
    timer = 200
    score = 0
    boardSize = 8
    tileSize = 45
    frameSize = 50
    board = generateBoard()

def drawText(text, pos):
    text = basicFont.render(text, True, BLACK, WHITE)
    textRect = text.get_rect()
    textRect.left = pos[0]
    textRect.top = pos[1]
    windowSurface.blit(text, textRect)

def drawMenu():
    drawText('Score: ' + str(score), (400, 300))
    drawText('Controls:', (400, 10))
    drawText('R to reset', (400, 30))
    drawText('Time left:', (400, 70))

def generateBoard():
    board = []
    for y in range(boardSize):
        board.append([])
        for x in range(boardSize):
            board[y].append(random.randint(0,1))
    return board

def drawBoard(board):
    # Draw tiles in 2D
    for y in range(boardSize):
        for x in range(boardSize):
            colour = TILE_COLOUR[board[y][x]]
            pygame.draw.rect(windowSurface, colour, (x*frameSize, y*frameSize, tileSize, tileSize))
            if board[y][x] == 0:
                minusRect.left = x*frameSize+17.5
                minusRect.top = y*frameSize+17.5
                windowSurface.blit(MINUS_SIGN, minusRect)
            elif board[y][x] == 1:
                plusRect.left = x*frameSize+17.5
                plusRect.top = y*frameSize+17.5
                windowSurface.blit(PLUS_SIGN, plusRect)
            # Draw selected tiles as different colours
            for item in selectedTile:
                if item[0] == x and item[1] == y:
                    colour = TILE_COLOUR[board[y][x]+3]
                    pygame.draw.rect(windowSurface, colour, (x*frameSize, y*frameSize, tileSize, tileSize))
                    if not board[y][x]:
                        sMinusRect.left = x*frameSize+17.5
                        sMinusRect.top = y*frameSize+17.5
                        windowSurface.blit(S_MINUS_SIGN, sMinusRect)
                    else:
                        sPlusRect.left = x*frameSize+17.5
                        sPlusRect.top = y*frameSize+17.5
                        windowSurface.blit(S_PLUS_SIGN, sPlusRect)

    drawMenu()

# Set the game variables.
setToDefault()

# Main game loop.
while True:
    # Draw the background.
    windowSurface.fill(WHITE)

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            # Reset game if 'r' key is pressed
            if event.key == K_r:
                setToDefault()
        if event.type == MOUSEBUTTONDOWN and timer > 0:
            if event.button == 3 and len(selectedTile) > 1:
                for tile in selectedTile:
                    board[tile[1]][tile[0]] = 2
                    score = score + 2**len(selectedTile)
                    selectedTile = []  
            elif event.button == 1:
                x, y = pygame.mouse.get_pos()
                x = floor(x/frameSize)
                y = floor(y/frameSize)
                # Check if coordinates are within range of board
                if x <= 7:
                    if board[y][x] != 2:
                        if len(selectedTile) == 0:  # If no tiles are selected
                            selectedTile.append([x,y])
                        else:   # If at least one tile is selected
                            if [x,y] in selectedTile and len(selectedTile) == 1: # If a selected tile is clicked on
                                selectedTile.remove([x,y])
                            elif [x,y+1] in selectedTile: # If tile directly below is selected
                                if board[y][x] != board[y+1][x]:
                                    selectedTile.append([x,y])
                            elif [x,y-1] in selectedTile: # If tile directly above is selected
                                if board[y][x] != board[y-1][x]:
                                    selectedTile.append([x,y])
                            elif [x+1,y] in selectedTile: # If tile directly right is selected
                                if board[y][x] != board[y][x+1]:
                                    selectedTile.append([x,y])
                            elif [x-1,y] in selectedTile: # If tile directly left is selected
                                if board[y][x] != board[y][x-1]:
                                    selectedTile.append([x,y])

        # Ensure game closes correctly
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if timer > 0:
        timer -= 0.1
        timerBox = pygame.Rect(400, 90, ceil(timer/maxTime*90), 10)
        pygame.draw.rect(windowSurface, DARK_RED, timerBox)
        drawBoard(board)
    else:
        drawText('Game over!', (210, 160))
        drawText('Your score: ' + str(score), (175, 200))
        drawText('Press R to play again.', (175, 220))

    pygame.display.update()

    mainClock.tick(40)
