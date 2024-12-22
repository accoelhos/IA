import matplotlib.pyplot as plt
import numpy as np
import gymnasium as gym
from timeit import default_timer as timer
from scipy.signal import savgol_filter

max_epsilon = 1.0
min_epsilon = 0.01
decay_rate = 0.0001
epsilons_ = []

def epsilon_greedy_policy(state, q_table, epsilon):
    """Choose an action using epsilon-greedy policy."""
    if np.random.uniform(0, 1) < epsilon:
        action = env.action_space.sample()  # Explore: random action
    else:
        action = np.argmax(q_table[state, :])  # Exploit: best action
    assert (action >= 0) and (action <= 3)
    return action


# Environment
ENV_NAME = "FrozenLake-v1"
env = gym.make(ENV_NAME, 
               is_slippery=False)  # Set is_slippery=True for stochastic behavior

plt.rcParams['figure.dpi'] = 300
plt.rcParams.update({'font.size': 7})

# We re-initialize the Q-table
q_table = np.zeros((env.observation_space.n, env.action_space.n))

# Hyperparameters
episodes = 10000        # Total number of episodes
learning_rate = 0.001
gamma = 0.99            # Discount factor

# List of outcomes to plot
outcomes = []

epsilon = 1.0         # Exploration rate (epsilon-greedy)


def choose_action(state, is_in_exploration_mode=True):
    exploration_tradeoff = np.random.uniform(0, 1)

    if is_in_exploration_mode and exploration_tradeoff < epsilon:
      # exploration
      action = np.random.randint(env.action_space.n)    
    else:
      # exploitation (taking the biggest Q value for this state)
      action = np.argmax(q_table[state, :])
    
    return action

def update(state, action, reward, next_state):
    '''
    Apply update rule Q(s,a):= Q(s,a) + lr * [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
    '''
    q_table[state, action] = q_table[state, action] + \
      learning_rate * (reward + gamma * \
        np.max(q_table[next_state, :]) - q_table[state, action])

def train(num_episodes: int):
    rewards_per_episode = []

    start_time = timer()  # Record the start time

    print()
    print('===========================================')
    print('Q-table before training:')
    print(q_table)

    for episode in range(num_episodes):
  
      terminated = False
      truncated = False

      state, _ = env.reset()

      rewards_in_episode = []
      
      total_penalties = 0

      while not (terminated or truncated):
          
        # print(f"state: {state}")
        action = choose_action(state)

        # transição
        new_state, reward, terminated, truncated, info = env.step(action)
        #print(new_state)

        if reward < 0:
            total_penalties += reward

        update(state, action, reward, new_state)

        if (terminated or truncated):
          # Reduce epsilon to decrease the exploration over time
          epsilon = min_epsilon + (max_epsilon - min_epsilon) * \
            np.exp(-decay_rate * episode)
          epsilons_.append(epsilon)

        state = new_state
            
        rewards_in_episode.append(reward)

      sum_rewards = np.sum(rewards_in_episode)
      rewards_per_episode.append(sum_rewards)

      if episode % 100 == 0:
        end_time = timer()  # Record the end time
        execution_time = end_time - start_time
        n_actions = len(rewards_in_episode)
        print(f"Stats for episode {episode}/{num_episodes}:") 
        print(f"\tNumber of actions: {n_actions}")
        print(f"\tTotal reward: {sum_rewards:#.2f}")
        print(f"\tExecution time: {execution_time:.2f}s")
        print(f"\tTotal penalties: {total_penalties}")
        start_time = end_time

    print()
    print('===========================================')
    print('Q-table after training:')
    print(q_table)

    return rewards_per_episode

rewards = train(num_episodes = episodes)

plt.plot(savgol_filter(rewards, 101, 2))
plt.title(f"Curva de aprendizado suavizada ({ENV_NAME})")
plt.xlabel('Episódio')
plt.ylabel('Recompensa total')
plt.savefig("FrozenLake-tql-learning_curve.png")
plt.close()