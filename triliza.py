import pygame
import sys
import numpy as np
import random
from pygame.locals import *

pygame.init()

# Χρώματα
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
dark_bg = (30, 30, 30)

# Μέγεθος παραθύρου
width, height = 700, 700
size = 3
block_size = width // size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tic Tac Toe')

# Πίνακας παιχνιδιού
board = np.array([['' for _ in range(size)] for _ in range(size)])

# Ρυθμίσεις γραμμών
line_color = white
line_width = 10

# Σύμβολα παικτών
x_symbol = 'X'
o_symbol = 'O'

# Σχεδίαση ταμπλό
def draw_lines():
    for i in range(1, size):
        pygame.draw.line(screen, line_color, (0, i * block_size), (width, i * block_size), line_width)
        pygame.draw.line(screen, line_color, (i * block_size, 0), (i * block_size, height), line_width)

# Σχεδίαση συμβόλων
def draw_symbols():
    for row in range(size):
        for col in range(size):
            if board[row][col] == x_symbol:
                pygame.draw.line(screen, red, (col * block_size + 50, row * block_size + 50), (col * block_size + block_size - 50, row * block_size + block_size - 50), 10)
                pygame.draw.line(screen, red, (col * block_size + block_size - 50, row * block_size + 50), (col * block_size + 50, row * block_size + block_size - 50), 10)
            elif board[row][col] == o_symbol:
                pygame.draw.circle(screen, green, (col * block_size + block_size//2, row * block_size + block_size//2), block_size//2 - 50, 10)

# Έλεγχος νίκης
def is_winner(player_symbol):
    for i in range(size):
        if all(board[i, :] == player_symbol) or all(board[:, i] == player_symbol):
            return True
    if all(board[i, i] == player_symbol for i in range(size)) or all(board[i, size - 1 - i] == player_symbol for i in range(size)):
        return True
    return False

# Έλεγχος γεμάτου ταμπλό
def is_board_full():
    return not any('' in row for row in board)

# Εμφάνιση μηνύματος

def draw_message(message, color, sub_message='Κάνε κλικ για νέο παιχνίδι ή ESC για έξοδο'):
    screen.fill(dark_bg)
    draw_lines()
    draw_symbols()
    font = pygame.font.SysFont(None, 80)
    sub_font = pygame.font.SysFont(None, 40)
    text = font.render(message, True, color)
    sub_text = sub_font.render(sub_message, True, white)
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2 - 30))
    screen.blit(sub_text, (width // 2 - sub_text.get_width() // 2, height // 2 + 50))
    pygame.display.update()

# Επαναφορά ταμπλό
def reset_board():
    global board
    board = np.array([['' for _ in range(size)] for _ in range(size)])

# Τυχαία κίνηση όταν ο παίκτης καθυστερεί
def random_move(symbol):
    empty_cells = [(row, col) for row in range(size) for col in range(size) if board[row][col] == '']
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = symbol

# Κύρια επανάληψη
player_symbol = x_symbol
running = True
clock = pygame.time.Clock()

while running:
    move_made = False
    start_ticks = pygame.time.get_ticks()

    while not move_made:
        seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                clicked_row, clicked_col = mouseY // block_size, mouseX // block_size
                if board[clicked_row][clicked_col] == '':
                    board[clicked_row][clicked_col] = player_symbol
                    move_made = True

        if seconds_passed >= 5:
            random_move(player_symbol)
            move_made = True

        screen.fill(dark_bg)
        draw_lines()
        draw_symbols()
        pygame.display.update()
        clock.tick(60)

    if is_winner(player_symbol):
        draw_message(f'Ο {player_symbol} κέρδισε!', red if player_symbol == x_symbol else green)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_n:
                        running = waiting = False
                    elif event.key == K_y:
                        reset_board()
                        waiting = False
    elif is_board_full():
        draw_message('Ισοπαλία!', white)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_n:
                        pygame.quit()
                        sys.exit()
                    elif event.key == K_y:
                        reset_board()
                        waiting = False

    player_symbol = o_symbol if player_symbol == x_symbol else x_symbol

    screen.fill(dark_bg)
    draw_lines()
    draw_symbols()
    pygame.display.update()
    clock.tick(60)