import numpy as np
import gymnasium as gym
import pickle
import os

input_file = 'frozenlake_q_table.pkl'

# Load Q-table to ensure it was saved correctly
with open(input_file, "rb") as f:
    loaded_q_table = pickle.load(f)
print("Q-table successfully loaded from file.\n")

# Render the agent solving the problem
def render_agent(env, q_table, episodes=1, max_steps=100):
    """Render the agent solving the problem using the learned Q-table."""
    for episode in range(episodes):
        state, _ = env.reset()
        done = False
        step_count = 0
        print(f"\nEpisode {episode + 1}:")
        env.render()

        while not done and step_count < max_steps:
            action = np.argmax(q_table[state])  # Choose the best action
            next_state, reward, terminated, truncated, _ = env.step(action)
            state = next_state
            done = terminated or truncated
            step_count += 1

            env.render()

            if done:
                if reward == 1:
                    print("Agent reached the goal! 🎉")
                else:
                    print("Agent fell into a hole. ☠️")
                break

render = True

# Environment
ENV_NAME = "FrozenLake-v1"
env = gym.make(ENV_NAME, 
               is_slippery=False, 
               render_mode='human' if render else None)  # Set is_slippery=True for stochastic behavior

print("\nRendering the agent solving the problem...")
render_agent(env, loaded_q_table, episodes=3)  # Render 3 episodes

env.close()
