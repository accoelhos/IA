from timeit import default_timer as timer
import numpy as np
import pickle
from environment import Environment

class QLearningAgentTabular:

    def __init__(self, 
                 env: Environment, 
                 decay_rate, 
                 learning_rate, 
                 gamma):
        self.env = env

        self.q_table = np.zeros((env.get_num_states(), env.get_num_actions()))
        print(f"self.q_table.shape: {self.q_table.shape}")
        
        self.epsilon = 1.0
        self.max_epsilon = 1.0
        self.min_epsilon = 0.01
        self.decay_rate = decay_rate
        self.learning_rate = learning_rate
        self.gamma = gamma # discount rate
        self.epsilons_ = []
        
    def choose_action(self, state, is_in_exploration_mode=True):
      
        # CONVERTER O ESTADO "CRU" PARA ID AQUI
        state_id = self.env.get_state_id(state)

        exploration_tradeoff = np.random.uniform(0, 1)

        if is_in_exploration_mode and exploration_tradeoff < self.epsilon:
            # exploration
            action = np.random.randint(self.env.get_num_actions())
        else:
            # exploitation (usando o state_id convertido)
            action = np.argmax(self.q_table[state_id, :])
        
        return action

    def update(self, state, action, reward, next_state):
        # CONVERTER OS ESTADOS "CRUS" PARA IDs AQUI
        state_id = self.env.get_state_id(state)
        next_state_id = self.env.get_state_id(next_state)
        
        '''
        Apply update rule Q(s,a):= Q(s,a) + lr * [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
        '''
        # Usar os IDs convertidos para acessar a q_table
        self.q_table[state_id, action] = self.q_table[state_id, action] + \
            self.learning_rate * (reward + self.gamma * \
            np.max(self.q_table[next_state_id, :]) - self.q_table[state_id, action])

    def train(self, num_episodes: int):
        rewards_per_episode = []
        start_time = timer() 

        print()
        print('===========================================')
        print('Q-table before training:')
        print(self.q_table)

        for episode in range(num_episodes):
    
            terminated = False
            truncated = False

            #REMOVE A CONVERSÃO MANUAL DAQUI
            # 'state' agora é o estado "cru" (ex: [-0.5, 0.01])
            state, _ = self.env.reset()

            rewards_in_episode = []
            total_penalties = 0

            while not (terminated or truncated):
                
                # Passa o estado "cru" para o choose_action
                action = self.choose_action(state)

                # new_state é o estado cru retornado pelo ambiente
                new_state, reward, terminated, truncated, info = self.env.step(action)

                assert (not truncated)

                if reward < 0:
                    total_penalties += reward

                # Passa os estados crus para o update
                self.update(state, action, reward, new_state)

                if (terminated or truncated):
                    self.epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon) * \
                        np.exp(-self.decay_rate * episode)
                    self.epsilons_.append(self.epsilon)

                # state agora se torna o próximo estado cru
                state = new_state
                
                rewards_in_episode.append(reward)

            sum_rewards = np.sum(rewards_in_episode)
            rewards_per_episode.append(sum_rewards)

            if episode % 100 == 0:
                end_time = timer() 
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
        print(self.q_table)

        return rewards_per_episode

    def save(self, filename):
        file = open(filename, 'wb')
        pickle.dump(self, file)
        file.close()

    @staticmethod
    def load_agent(filename):
        file = open(filename, 'rb')
        agent = pickle.load(file)
        return agent