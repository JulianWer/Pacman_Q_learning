# Pacman Q-Learning

This project implements a simplified version of the classic Pac-Man game, where an agent learns to navigate optimally using Q-Learning. The goal of the Pac-Man agent is to eat all the cookies in a maze while avoiding a ghost.

## How it Works

The project uses the Pygame library for graphics and game logic. The game runs in episodes. In each episode, Pac-Man tries to eat all the cookies without being caught by the ghost or exceeding the step limit for the episode.

### Game Logic

  * **Pac-Man**: Controlled by the Q-Learning agent, it moves through the maze to collect cookies.
  * **Ghost**: Chases Pac-Man using a simple logic aimed at reducing the distance to Pac-Man.
  * **Cookies**: Scattered throughout the maze. Eating a cookie provides a positive reward.
  * **Walls**: Impassable obstacles for both Pac-Man and the Ghost.

### Q-Learning Agent

The agent makes decisions based on a Q-table, which stores the expected reward for each action in every state.

  * **State**: The state is defined by the positions of Pac-Man and the ghost, along with the status of nearby cookies. The status of cookies immediately around Pac-Man (up, down, left, right) is encoded as a bitmask.
  * **Actions**: The agent can move up, down, left, or right.
  * **Learning**: The agent uses an Epsilon-Greedy strategy to balance exploring new actions and exploiting known good ones. After each action, the Q-table is updated using the Bellman equation, which considers the reward received and the maximum Q-value of the next state.

### Reward Structure

The reward system is designed to motivate the desired behavior:

  * **+100 points**: For winning by eating all the cookies.
  * **+10 points**: For eating a single cookie.
  * **-0.1 points**: For each step taken, encouraging the agent to find the fastest route.
  * **-20 points**: For exceeding the maximum number of steps in an episode.
  * **-50 points**: For colliding with the ghost.

## Project Structure

The project is divided into several Python files:

  * **`main.py`**: The main entry point that starts the training loop and plots the results.
  * **`game.py`**: Contains the main `Game` class, which manages the game logic, state, and rendering.
  * **`game_objects.py`**: Defines the `Pacman` and `Ghost` classes, including their movement and appearance.
  * **`q_learning_agent.py`**: Implements the `QLearningAgent`, which manages the Q-table, selects actions, and learns from experience.
  * **`constants.py`**: Stores all global constants, such as screen dimensions, colors, and Q-learning parameters.
  * **`.gitignore`**: Specifies files and directories to be excluded from version control.

## Prerequisites

Ensure you have the following Python libraries installed:

  * Pygame
  * Matplotlib
  * NumPy

You can install the required libraries with the following command:

```bash
pip install pygame matplotlib numpy
```

## How to Run

To start training the Pac-Man agent, execute the main file:

```bash
python main.py
```

During training, progress is printed to the console, showing the reward for each episode and the total number of wins and losses. Once training is complete, a plot will be displayed showing the reward per episode and a moving average to visualize the agent's learning progress.
