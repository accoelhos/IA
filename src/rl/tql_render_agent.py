import argparse
import numpy as np
import gymnasium as gym
import pickle
import os
from tql import QLearningAgentTabular

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--env_name", type=str, default="Taxi-v3", help="Environment name.")
    parser.add_argument("--successful_episode_reward_value", required=True, type=int, help="Reward value received by the agent when it reaches the end of an episode.")
    args = parser.parse_args()

    # Load the agent
    agent = QLearningAgentTabular.load_agent(args.env_name + "-tql-agent.pkl")

    # Render the agent solving the problem
    # Adicionado "agent_wrapper" como parâmetro
    def render_agent(env, agent_wrapper, q_table, episodes=1, max_steps=100):
        """Render the agent solving the problem using the learned Q-table."""
        for episode in range(episodes):
            state, _ = env.reset()
            done = False
            step_count = 0
            print(f"\nEpisode {episode + 1}:")
            env.render()

            while not done and step_count < max_steps:
                
                #  Converter o 'state' (tupla) para 'state_id' (int)
                state_id = agent_wrapper.get_state_id(state)
                
                # Usar o 'state_id' para consultar a q_table
                action = np.argmax(q_table[state_id])  # Choose the best action
                
                next_state, reward, terminated, truncated, _ = env.step(action)
                state = next_state # 'state' continua sendo a tupla para a próxima iteração
                done = terminated or truncated
                step_count += 1

                env.render()

                if done:
                    if reward == args.successful_episode_reward_value:
                        print("Agent reached the goal! 🎉")
                    else:
                        print("Agent didn't reach the goal. ☠️")
                    break

    render = True

    # Environment
    env = gym.make(args.env_name, render_mode='human' if render else None)

    print("\nRendering the agent solving the problem...")
    
    # Passar o "agent.env" (o wrapper) para a função
    render_agent(env, agent.env, agent.q_table, episodes=3)  # Render 3 episodes

    env.close()