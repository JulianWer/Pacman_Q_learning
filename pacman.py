import numpy as np
import pygame
import random
import math
import matplotlib.pyplot as plt

# -- Fester Seed für Reproduzierbarkeit --
random.seed(42)
np.random.seed(42)
# Initialize pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
CELL_SIZE = 40

# Define colors
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

initial_labyrinth = [
    "##########",
    "#........#",
    "#.##..##.#",
    "#........#",
    "##########"
]

# Labyrinth as a string
labyrinth = [
    "##########",
    "#........#",
    "#.##..##.#",
    "#........#",
    "##########"
]

ROWS = len(labyrinth)
COLS = len(labyrinth[0])

X_DIR = [-1, 1, 0, 0]
Y_DIR = [0, 0, -1, 1]

EPSILON = 0.1

ALPHA = 0.2
GAMMA = 0.9
MAX_STEPS_PER_EPISODE = 200
max_y = ROWS
max_x = COLS
cookie_status_values = 16

max_state_index = max_y * max_x * max_y * max_x * cookie_status_values
q = np.random.rand(max_state_index, 4) * 0.1
print(q)

screen = pygame.display.set_mode((COLS * CELL_SIZE, ROWS * CELL_SIZE))
pygame.display.set_caption("Micro-Pacman")

# Pacman class
class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.count = 0

    def move(self, dx, dy):
        new_x, new_y = self.x + dx, self.y + dy
        if labyrinth[new_y][new_x] != "#":
            self.x = new_x
            self.y = new_y

    def draw(self):
        radius = CELL_SIZE // 2 - 4
        start_angle = math.pi / 6
        end_angle = -math.pi / 6
        pygame.draw.circle(screen, YELLOW, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 4)
        # Calculate the points for the mouth
        start_pos = (self.x * CELL_SIZE + CELL_SIZE // 2 + int(radius * 1.3 * math.cos(start_angle)),
                     self.y * CELL_SIZE + CELL_SIZE // 2 - int(radius * 1.3 * math.sin(start_angle)))
        end_pos = (self.x * CELL_SIZE + CELL_SIZE // 2 + int(radius * 1.3 * math.cos(end_angle)),
                   self.y * CELL_SIZE + CELL_SIZE // 2 - int(radius * 1.3 * math.sin(end_angle)))
        self.count += 1
        if self.count % 2 == 0:
            # Draw the mouth by filling a polygon
            pygame.draw.polygon(screen, BLACK, [(self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), start_pos, end_pos])

# Ghost class with pixel art
class Ghost:
    # Define the pixel art for the ghost using strings
    ghost_pixels = [
        " #### ",
        "######",
        "## # #",
        "######",
        "######",
        "# # # "
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_towards_pacman(self, pacman):
        if self.x < pacman.x and labyrinth[self.y][self.x + 1] != "#":
            self.x += 1
        elif self.x > pacman.x and labyrinth[self.y][self.x - 1] != "#":
            self.x -= 1
        elif self.y < pacman.y and labyrinth[self.y + 1][self.x] != "#":
            self.y += 1
        elif self.y > pacman.y and labyrinth[self.y - 1][self.x] != "#":
            self.y -= 1

    def draw(self):
        pixel_size = CELL_SIZE // len(self.ghost_pixels)  # Size of each pixel in the ghost art
        for row_idx, row in enumerate(self.ghost_pixels):
            for col_idx, pixel in enumerate(row):
                if pixel == "#":
                    pixel_x = self.x * CELL_SIZE + col_idx * pixel_size
                    pixel_y = self.y * CELL_SIZE + row_idx * pixel_size
                    pygame.draw.rect(screen, RED, (pixel_x, pixel_y, pixel_size, pixel_size))

# Draw walls and cookies
def draw_labyrinth():
    for y, row in enumerate(labyrinth):
        for x, cell in enumerate(row):
            if cell == "#":
                pygame.draw.rect(screen, BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif cell == ".":
                pygame.draw.circle(screen, WHITE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), 5)

def get_cookie_status(pacman_pos):
    y, x = pacman_pos
    cookie_status = 0
    if y > 0 and labyrinth[y - 1][x] == '.':
        cookie_status |= 1  # Up
    if y < ROWS - 1 and labyrinth[y + 1][x] == '.':
        cookie_status |= 2  # Down
    if x > 0 and labyrinth[y][x - 1] == '.':
        cookie_status |= 4  # Left
    if x < COLS - 1 and labyrinth[y][x + 1] == '.':
        cookie_status |= 8  # Right
    return cookie_status


def getState(pacman_pos, ghost_pos):
    cookie_status = get_cookie_status(pacman_pos)

    # note: y zeilen und x spalten
    # Lineare Positionen berechnen
    pacman_linear = pacman_pos[0] * COLS + pacman_pos[1]  # Pacman y * COLS + Pacman x
    ghost_linear = ghost_pos[0] * COLS + ghost_pos[1]  # Geist y * COLS + Geist x

    state_index = (
            pacman_linear * (ROWS * COLS * cookie_status_values) +
            ghost_linear * cookie_status_values +
            cookie_status
    )
    return state_index


# Main game function
def main():
    clock = pygame.time.Clock()
    win = 0
    episode_rewards = []
    episode = 0

    initial_cookies = sum(row.count('.') for row in initial_labyrinth)

    global EPSILON
    while True:
        episode += 1
        total_reward = 0

        # Reset the labyrinth to the initial state
        global labyrinth
        labyrinth = [list(row) for row in initial_labyrinth]

        # Initialize Pacman and Ghost positions
        pacman = Pacman(1, 1)
        ghost = Ghost(COLS - 2, ROWS - 2)

        # Game loop
        running = True
        iter = 0
        previous_distance_to_ghost = float('inf')
        previous_position = (pacman.x, pacman.y)

        print(win)
        while running:
            screen.fill(BLACK)
            iter += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            reward = 0

            s = getState((pacman.y, pacman.x), (ghost.x, ghost.y))

            if random.uniform(0, 1) < EPSILON:
                a = np.random.randint(4) # 0: up, 1: down, 2: left, 3: right
            else:
                a = np.argmax(q[s])

            pacman.move(X_DIR[a], Y_DIR[a])

            if iter % 3 == 0:
                ghost.move_towards_pacman(pacman)

            if pacman.x == ghost.x and pacman.y == ghost.y:
                print("Game Over! The ghost caught Pacman.")
                win -= 1
                reward = -30
                running = False

            distance_to_ghost = abs(pacman.x - ghost.x) + abs(pacman.y - ghost.y)
            if distance_to_ghost == 1:
                reward -= 3
            elif distance_to_ghost == 2:
                reward -= 2

            if distance_to_ghost > previous_distance_to_ghost:
                reward += 0.5
            previous_distance_to_ghost = distance_to_ghost

            if (pacman.x, pacman.y) == previous_position:
                reward -= 1
            else:
                reward += 0.1
            previous_position = (pacman.x, pacman.y)

            if labyrinth[pacman.y][pacman.x] == ".":
                remaining_cookies = sum(row.count('.') for row in labyrinth)
                reward += 5 + (initial_cookies - remaining_cookies)
                labyrinth[pacman.y][pacman.x] = " "

            if all("." not in row for row in labyrinth):
                print("You Win! Pacman ate all the cookies.")
                win += 1
                reward = 50
                running = False



            new_s = getState((pacman.y, pacman.x), (ghost.x, ghost.y))

            q[s][a] += ALPHA * (reward + GAMMA * np.max(q[new_s]) - q[s][a])

            total_reward += reward

            draw_labyrinth()
            pacman.draw()
            ghost.draw()

            pygame.display.flip()

            if iter > MAX_STEPS_PER_EPISODE:
                running = False

        episode_rewards.append(total_reward)


    pygame.quit()

if __name__ == "__main__":
    main()