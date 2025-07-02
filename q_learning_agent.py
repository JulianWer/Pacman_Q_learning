# q_learning_agent.py
# Contains the logic for the Q-Learning agent.

import numpy as np
import random
from constants import ROWS, COLS, COOKIE_STATUS_VALUES, MAX_STATE_INDEX, EPSILON, ALPHA, GAMMA

class QLearningAgent:
    """
    Manages the Q-table, state determination, action selection, and learning process.
    """
    def __init__(self):
        # Initialize Q-table with small random values for reproducibility.
        np.random.seed(42)
        self.q_table = np.random.rand(MAX_STATE_INDEX, 4) * 0.01

    def get_cookie_status(self, pacman_pos, labyrinth):
        """
        Determines the status of cookies around Pacman, encoded as a bitmask.
        Bit 0: Up, Bit 1: Down, Bit 2: Left, Bit 3: Right
        """
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

    def get_state(self, pacman_pos, ghost_pos, labyrinth):
        """
        Calculates a unique index for the current game state.
        The state is defined by Pacman's position, the ghost's position, and the cookie status.
        """
        cookie_status = self.get_cookie_status(pacman_pos, labyrinth)

        pacman_y, pacman_x = pacman_pos
        ghost_y, ghost_x = ghost_pos

        # Convert 2D positions to a 1D linear index.
        pacman_linear = pacman_y * COLS + pacman_x
        ghost_linear = ghost_y * COLS + ghost_x

        # Combine linear indices and cookie status into a single unique state index.
        state_index = (pacman_linear * (ROWS * COLS * COOKIE_STATUS_VALUES) +
                       ghost_linear * COOKIE_STATUS_VALUES +
                       cookie_status)
        
        # Ensure the index is within the valid range.
        return min(state_index, MAX_STATE_INDEX - 1)


    def choose_action(self, state):
        """
        Selects an action based on the Epsilon-Greedy strategy.
        With probability EPSILON, a random action is chosen (exploration).
        Otherwise, the action with the highest Q-value is chosen (exploitation).
        """
        if random.uniform(0, 1) < EPSILON:
            return np.random.randint(4)  # 0: up, 1: down, 2: left, 3: right
        else:
            return np.argmax(self.q_table[state])

    def learn(self, state, action, reward, next_state):
        """
        Updates the Q-value for the given state-action pair using the Bellman equation.
        """
        predict = self.q_table[state, action]
        target = reward + GAMMA * np.max(self.q_table[next_state])
        self.q_table[state, action] += ALPHA * (target - predict)
