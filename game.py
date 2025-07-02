# game.py
# The main Game class that controls the game logic and flow.

import pygame
from constants import *
from game_objects import Pacman, Ghost

class Game:
    """ Manages the entire game flow, state, and rendering. """
    def __init__(self, agent):
        self.agent = agent
        self.clock = pygame.time.Clock()
        self.wins = 0
        self.losses = 0
        self.initial_cookies = sum(row.count('.') for row in INITIAL_LABYRINTH)
        self._reset_episode()

    def _reset_episode(self):
        """ Resets the game for a new episode. """
        self.labyrinth = [list(row) for row in INITIAL_LABYRINTH]
        self.pacman = Pacman(1, 1)
        self.ghost = Ghost(COLS - 2, ROWS - 2)
        self.steps = 0
        self.total_reward = 0

    def _draw(self):
        """ Draws all game elements to the screen. """
        SCREEN.fill(BLACK)
        # Draw walls and cookies
        for y, row in enumerate(self.labyrinth):
            for x, cell in enumerate(row):
                if cell == "#":
                    pygame.draw.rect(SCREEN, BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif cell == ".":
                    pygame.draw.circle(SCREEN, WHITE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), 5)
        
        self.pacman.draw()
        self.ghost.draw()
        pygame.display.flip()

    def run_episode(self):
        """ Runs a single game episode. """
        self._reset_episode()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None # Signal to quit the program

            reward = -0.1 # Small negative reward for each step to encourage speed

            # 1. Get current state
            state = self.agent.get_state((self.pacman.y, self.pacman.x), (self.ghost.x, self.ghost.y), self.labyrinth)

            # 2. Choose action
            action = self.agent.choose_action(state)

            # 3. Perform action and move Pacman
            self.pacman.move(X_DIR[action], Y_DIR[action], self.labyrinth)

            # 4. Move ghost (e.g., every 3 steps)
            if self.steps % 3 == 0:
                self.ghost.move_towards_pacman(self.pacman, self.labyrinth)

            # 5. Calculate reward
            # Collision with ghost
            if self.pacman.x == self.ghost.x and self.pacman.y == self.ghost.y:
                reward = -50
                self.losses += 1
                running = False
            
            # Ate a cookie
            if self.labyrinth[self.pacman.y][self.pacman.x] == ".":
                self.labyrinth[self.pacman.y][self.pacman.x] = " "
                reward = 10
            
            # Ate all cookies (win)
            if not any("." in row for row in self.labyrinth):
                reward = 100
                self.wins += 1
                running = False

            # Game lost due to too many steps
            if self.steps > MAX_STEPS_PER_EPISODE:
                reward = -20
                self.losses += 1
                running = False

            # 6. Get new state
            next_state = self.agent.get_state((self.pacman.y, self.pacman.x), (self.ghost.x, self.ghost.y), self.labyrinth)

            # 7. Agent learns from the experience
            self.agent.learn(state, action, reward, next_state)

            self.total_reward += reward
            self.steps += 1

            # 8. Draw the game
            self._draw()
            self.clock.tick(15) # Limit frame rate

        return self.total_reward
