# constants.py
# Contains all global constants and configurations for the game.

import pygame

# -- Pygame Setup --
pygame.init()
pygame.display.set_caption("Micro-Pacman Q-Learning")

# -- Screen and Grid Dimensions --
CELL_SIZE = 40

INITIAL_LABYRINTH = [
    "##########",
    "#........#",
    "#.##..##.#",
    "#........#",
    "##########"
]
ROWS = len(INITIAL_LABYRINTH)
COLS = len(INITIAL_LABYRINTH[0])
SCREEN_WIDTH = COLS * CELL_SIZE
SCREEN_HEIGHT = ROWS * CELL_SIZE
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# -- Colors --
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# -- Game Mechanics --
X_DIR = [-1, 1, 0, 0]  # Movement directions: Up, Down, Left, Right
Y_DIR = [0, 0, -1, 1]

# -- Q-Learning Parameters --
ALPHA = 0.1  # Learning rate
GAMMA = 0.9  # Discount factor
EPSILON = 0.1  # Epsilon for Epsilon-Greedy strategy
MAX_STEPS_PER_EPISODE = 200

# -- State Space Configuration --
# State is defined by (pacman_y, pacman_x, ghost_y, ghost_x, cookie_status).
# This is mapped to a single index for the Q-table.
COOKIE_STATUS_VALUES = 16  # 2^4, for 4 possible cookie directions
MAX_STATE_INDEX = (ROWS * COLS) * (ROWS * COLS) * COOKIE_STATUS_VALUES
