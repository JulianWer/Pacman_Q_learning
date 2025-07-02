import pygame
import matplotlib.pyplot as plt
from game import Game
from q_learning_agent import QLearningAgent

def plot_rewards(episode_rewards):
    """ Plots the rewards at the end of the training. """
    plt.figure(figsize=(10, 5))
    plt.plot(episode_rewards)
    plt.title('Reward per Episode')
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.grid(True)
    
    # Plot a moving average for better visualization
    if len(episode_rewards) >= 100:
        moving_avg = [sum(episode_rewards[i-100:i]) / 100 for i in range(100, len(episode_rewards))]
        plt.plot(range(100, len(episode_rewards)), moving_avg, color='red', linewidth=2, label='Moving Average (100 episodes)')
        plt.legend()
        
    plt.show()


def main():
    """ Initializes the game and agent, and starts the training loop. """
    agent = QLearningAgent()
    game = Game(agent)
    
    episode_rewards = []
    num_episodes = 2000

    # Main training loop
    for episode in range(num_episodes):
        total_reward = game.run_episode()
        
        # Exit the program if the window is closed
        if total_reward is None:
            break
            
        episode_rewards.append(total_reward)
        print(f"Episode: {episode + 1}, Reward: {total_reward:.2f}, Wins: {game.wins}, Losses: {game.losses}")

    pygame.quit()
    print("Training finished.")
    plot_rewards(episode_rewards)

if __name__ == "__main__":
    main()
