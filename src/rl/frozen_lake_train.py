import numpy as np
import gymnasium as gym
import pickle
import os

# Q-Learning Hyperparameters
ALPHA = 0.5           # Learning rate
GAMMA = 0.9           # Discount factor
EPSILON = 0.1         # Exploration rate (epsilon-greedy)
EPISODES = 1000       # Number of episodes for training

render = False

# Environment
ENV_NAME = "FrozenLake-v1"
env = gym.make(ENV_NAME, 
               is_slippery=False, 
               render_mode='human' if render else None).env  # Set is_slippery=True for stochastic behavior

# Initialize Q-table
state_size = env.observation_space.n
action_size = env.action_space.n
q_table = np.zeros((state_size, action_size))  # Q-table initialized to 0

def epsilon_greedy_policy(state, q_table, epsilon):
    """Choose an action using epsilon-greedy policy."""
    if np.random.uniform(0, 1) < epsilon:
        return env.action_space.sample()  # Explore: random action
    else:
        return np.argmax(q_table[state])  # Exploit: best action

print('Q-table before training:')
print(q_table)

# Q-Learning Algorithm
for episode in range(EPISODES):
    state, _ = env.reset()  # Reset environment
    done = False

    while not done:
        # Choose action using epsilon-greedy policy
        action = epsilon_greedy_policy(state, q_table, EPSILON)
        #print(action)

        # Take action and observe reward and next state
        next_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated

        if terminated:
            print(f'Agent reached terminal state. reward = {reward}')

        # Update Q-value using the Q-Learning formula
        #print(f'Updating q-value ({state}, {action}). New value: {q_table[state, action]}')
        #q_table[state, action] = q_table[state, action] + ALPHA * (
        #    reward + GAMMA * np.max(q_table[next_state]) - q_table[state, action]
        #)
        print(f'reward: {reward}')
        v = reward + GAMMA * np.max(q_table[next_state])
        if v > 0:
            print(f'v: {v}')
        q_table[state, action] = q_table[state, action] + ALPHA * (v - q_table[state, action])

        # Transition to the next state
        state = next_state

    # Print progress every 100 episodes
    if (episode + 1) % 100 == 0:
        print(f"Episode {episode + 1}/{EPISODES} completed.")

print()
print('===========================================')
print('Q-table after training:')
print(q_table)

# Save the Q-table to a pickle file
output_file = "frozenlake_q_table.pkl"
with open(output_file, "wb") as f:
    pickle.dump(q_table, f)
print(f"\nQ-table saved to {output_file}")