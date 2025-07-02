import pygame
import math
from constants import SCREEN, CELL_SIZE, YELLOW, RED, BLACK

class Pacman:
    """ Represents the Pacman character, its movement, and rendering. """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mouth_open = True
        self.mouth_counter = 0

    def move(self, dx, dy, labyrinth):
        """ Moves Pacman if the target cell is not a wall. """
        new_x, new_y = self.x + dx, self.y + dy
        if labyrinth[new_y][new_x] != "#":
            self.x = new_x
            self.y = new_y

    def draw(self):
        """ Draws Pacman on the screen with an animated mouth. """
        center_x = self.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.y * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 4

        # Animate mouth
        self.mouth_counter += 1
        if self.mouth_counter > 10:
            self.mouth_open = not self.mouth_open
            self.mouth_counter = 0

        if self.mouth_open:
            start_angle = math.pi / 6
            end_angle = -math.pi / 6
            pygame.draw.circle(SCREEN, YELLOW, (center_x, center_y), radius)
            # Draw mouth as a black polygon
            points = [(center_x, center_y),
                      (center_x + radius * math.cos(start_angle), center_y - radius * math.sin(start_angle)),
                      (center_x + radius * math.cos(end_angle), center_y - radius * math.sin(end_angle))]
            pygame.draw.polygon(SCREEN, BLACK, points)
        else:
            pygame.draw.circle(SCREEN, YELLOW, (center_x, center_y), radius)


class Ghost:
    """ Represents the Ghost character, its movement, and rendering. """
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

    def move_towards_pacman(self, pacman, labyrinth):
        """ A simple logic to move the ghost towards Pacman. """
        # Prefer horizontal movement
        if self.x < pacman.x and labyrinth[self.y][self.x + 1] != "#":
            self.x += 1
        elif self.x > pacman.x and labyrinth[self.y][self.x - 1] != "#":
            self.x -= 1
        # Move vertically if horizontal is not possible or already aligned
        elif self.y < pacman.y and labyrinth[self.y + 1][self.x] != "#":
            self.y += 1
        elif self.y > pacman.y and labyrinth[self.y - 1][self.x] != "#":
            self.y -= 1

    def draw(self):
        """ Draws the ghost as pixel art. """
        pixel_size = CELL_SIZE // len(self.ghost_pixels)
        for row_idx, row in enumerate(self.ghost_pixels):
            for col_idx, pixel in enumerate(row):
                if pixel == "#":
                    pixel_x = self.x * CELL_SIZE + col_idx * pixel_size
                    pixel_y = self.y * CELL_SIZE + row_idx * pixel_size
                    pygame.draw.rect(SCREEN, RED, (pixel_x, pixel_y, pixel_size, pixel_size))
