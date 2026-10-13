import pygame
import numpy as np
import time
import sys
import math

# using yoinked code
COLUMN_COUNT = 6
ROW_COUNT = 5
SQUARESIZE = 100

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

print("Max out of row and column is:", max(COLUMN_COUNT, ROW_COUNT))

#width = COLUMN_COUNT * SQUARESIZE
width = 875 # my code

#height = (ROW_COUNT + 1) * SQUARESIZE
height = 875 # my code

size = (width, height)

MostUpOrDown = max(ROW_COUNT, COLUMN_COUNT) # my code
SQUARESIZE = height // MostUpOrDown # my code

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)

def draw_board(board):
    for c in range(COLUMN_COUNT): # goes through each column
        time.sleep(0.05)
        for r in range(ROW_COUNT): # then goes through each row
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE)) # this draws a filled in square in which, later, you can place stuff inside
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)# this then removes the centre of that square, so it has a hole in for the counter
            #pygame.draw.circle(screen, BLACK, (int((c+0.5) * SQUARESIZE), int((r+1.5) * SQUARESIZE)), RADIUS)  # this then removes the centre of that square, so it has a hole in for the counter

            pygame.display.update()


    for c in range(COLUMN_COUNT): # this for loop is used later on - it will redraw the board each time
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)

            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    # for testing below this
    r = 1
    c = 3
    #pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board
board = create_board()

def PlacingCounter():
    turn = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                # print(event.pos)
                # Ask for Player 1 Input
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            label = myfont.render("Player 1 wins!!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True


                # # Ask for Player 2 Input
                else:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
                            label = myfont.render("Player 2 wins!!", 1, YELLOW)
                            screen.blit(label, (40, 10))
                            game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

                if game_over:
                    pygame.time.wait(3000)

draw_board(board)
pygame.display.update()

while True:
    PlacingCounter()