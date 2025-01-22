import pygame
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 600
HEIGHT = 600
CELL_SIZE = WIDTH // 3
LINE_WIDTH = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the game board
board = [['', '', ''], ['', '', ''], ['', '', '']]
font = pygame.font.Font(None, 100)
playing_X = True

# Win conditions
win_conditions = [
    [[0, 0], [0, 1], [0, 2]],
    [[1, 0], [1, 1], [1, 2]],
    [[2, 0], [2, 1], [2, 2]],
    [[0, 0], [1, 0], [2, 0]],
    [[0, 1], [1, 1], [2, 1]],
    [[0, 2], [1, 2], [2, 2]],
    [[0, 0], [1, 1], [2, 2]],
    [[0, 2], [1, 1], [2, 0]]
]


def check_win():
    for condition in win_conditions:
        a, b, c = condition
        if board[a[0]][a[1]] == board[b[0]][b[1]] == board[c[0]][c[1]] != '':
            return True
    return False


def draw_board():
    window.fill(BLACK)

    # Draw grid lines
    for i in range(1, 3):
        pygame.draw.line(window, WHITE, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(window, WHITE, (0, i * CELL_SIZE), (HEIGHT, i * CELL_SIZE), LINE_WIDTH)

    # Draw X's and O's
    for row in range(3):
        for col in range(3):
            if board[row][col] == 'X':
                text = font.render('X', True, WHITE)
                window.blit(text, (col * CELL_SIZE + CELL_SIZE / 2 - text.get_width() / 2,
                                   row * CELL_SIZE + CELL_SIZE / 2 - text.get_height() / 2))
            elif board[row][col] == 'O':
                text = font.render('O', True, WHITE)
                window.blit(text, (col * CELL_SIZE + CELL_SIZE / 2 - text.get_width() / 2,
                                   row * CELL_SIZE + CELL_SIZE / 2 - text.get_height() / 2))


def display_result(message):
    result_font = pygame.font.Font(None, 74)
    text = result_font.render(message, True, WHITE)
    window.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.flip()
    pygame.time.wait(1500)


# Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            col = x // CELL_SIZE
            row = y // CELL_SIZE

            # Check if the cell is empty
            if board[row][col] == '':
                if playing_X:
                    board[row][col] = 'X'
                else:
                    board[row][col] = 'O'

                # Check for a win
                if check_win():
                    display_result(f"{'X' if playing_X else 'O'} Wins!")
                    board = [['', '', ''], ['', '', ''], ['', '', '']]
                    playing_X = True
                else:
                    # Check for draw
                    if all(cell != '' for row in board for cell in row):
                        display_result("Draw!")
                        board = [['', '', ''], ['', '', ''], ['', '', '']]
                        playing_X = True
                    else:
                        playing_X = not playing_X

    window.fill(BLACK)
    draw_board()
    pygame.display.flip()