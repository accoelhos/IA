import argparse
import numpy as np
import gymnasium as gym
import pickle
import os
from lql import QLearningAgentLinear 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--env_name", type=str, default="Taxi-v3", help="Environment name.")
    parser.add_argument("--successful_episode_reward_value", required=True, type=float, help="Reward value threshold for a successful episode.")
    args = parser.parse_args()

    # Carrega o agente linear
    agent = QLearningAgentLinear.load_agent(args.env_name + "-lql-agent.pkl")

    # Render the agent solving the problem
    def render_agent(env, agent, episodes=1, max_steps=200):
        """Render the agent solving the problem using the learned policy."""
        for episode in range(episodes):
            
 
            state, _ = env.reset()
            
            done = False
            step_count = 0
            print(f"\nEpisode {episode + 1}:")
            env.render()
            
            total_reward = 0 # Para checar o sucesso

            while not done and step_count < max_steps:
                
                # Não lemos a q_table, pedimos a política do agente
                action = agent.policy(state)  
                
                next_state, reward, terminated, truncated, _ = env.step(action)
                state = next_state
                done = terminated or truncated
                step_count += 1
                total_reward += reward

                env.render()

                if done:
                    # Usamos >= pois o MountainCar pode ter recompensas melhores que -199
                    if total_reward >= args.successful_episode_reward_value:
                        print(f"Agent reached the goal! (Total Reward: {total_reward}) 🎉")
                    else:
                        print(f"Agent didn't reach the goal. (Total Reward: {total_reward}) ☠️")
                    break

    render = True

    # Criamos o ambiente "cru" do gym
    env = gym.make(args.env_name, render_mode='human' if render else None)

    print("\nRendering the LQL agent solving the problem...")
    
    # Passamos o próprio agente para a função
    render_agent(env, agent, episodes=3)  # Render 3 episodes

    env.close()