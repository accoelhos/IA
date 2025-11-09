from timeit import default_timer as timer
import pickle
import numpy as np
from environment import Environment

from taxi_feature_extractor import TaxiFeatureExtractor
from blackjack_feature_extractor import BlackjackFeatureExtractor

from cliffwalking_feature_extractor import CliffWalkingFeatureExtractor
from frozenlake_feature_extractor import FrozenLakeFeatureExtractor
from mountaincar_feature_extractor import MountainCarFeatureExtractor

feature_extractors_dict = {
    "Blackjack-v1": BlackjackFeatureExtractor,
    "Taxi-v3": TaxiFeatureExtractor,
    # novos
    "CliffWalking-v1": CliffWalkingFeatureExtractor,
    "FrozenLake-v1": FrozenLakeFeatureExtractor,
    "MountainCar-v0": MountainCarFeatureExtractor
}

class QLearningAgentLinear:

    def __init__(self, 
                 gym_env: Environment, 
                 epsilon_decay_rate, 
                 learning_rate, 
                 gamma):
        self.env = gym_env
        env_name = self.env.get_id() # get_id() vem do wrapper (ex: BlackjackEnvironment)

        print(f"Inicializando LQL para o ambiente: {env_name}")

        print("Carregando extrator de features...")
        
        self.fex = feature_extractors_dict[env_name](gym_env.env) 

        # w agora tem o tamanho exato retornado pelo extrator
        self.w = np.random.rand(self.fex.get_num_features())
        print(f"Vetor de pesos (w) inicializado com tamanho: {len(self.w)}")
        
        self.steps = 0

        self.epsilon = 1.0 # Epsilon inicial 1.0 para mais exploração
        self.max_epsilon = 1.0
        self.min_epsilon = 0.01 # Min epsilon menor
        self.epsilon_decay_rate = epsilon_decay_rate
        self.learning_rate = learning_rate
        self.gamma = gamma 
        self.epsilon_history = []

    def choose_action(self, state, is_in_exploration_mode = True):
        exploration_tradeoff = np.random.uniform(0, 1)
        if is_in_exploration_mode and exploration_tradeoff < self.epsilon:
            # exploration
            action = self.env.get_random_action()
        else:
            action = self.policy(state)
        return action

    def policy(self, state):
        # exploitation (taking the biggest Q value for this state)
        return self.__get_action_and_value(state)[0]

    def get_value(self, state):
        return self.__get_action_and_value(state)[1]

    def get_qvalues(self, state):
        q_values = {}
        # mod: usa get_num_actions() do wrapper
        for action in range(self.env.get_num_actions()): 
            q_values[action] = self.get_qvalue(state, action)
        return q_values

    def get_features(self, state, action):
        # mod: Apenas chama o extrator. Não adiciona mais features extras.
        feature_vector = self.fex.get_features(state, action)
        # Assegura que é 1D
        feature_vector = feature_vector.flatten()
        return feature_vector

    def get_qvalue(self, state, action):
        features = self.get_features(state, action)
        return np.dot(self.w, features)

    def __get_action_and_value(self, state):
        max_qvalue = float("-inf")
        best_action = 0
        # mod: usa get_num_actions() do wrapper
        for action in range(self.env.get_num_actions()):
            q_value = self.get_qvalue(state, action)
            if q_value > max_qvalue:
                max_qvalue = q_value
                best_action = action
        return [best_action, max_qvalue]

    def update(self, state, action, reward, next_state):
        next_state_value = self.get_value(next_state)
        
        # Se o extrator de features diz que é terminal
        if self.fex.is_terminal_state(next_state):
            next_state_value = 0
            
        difference = (reward + (self.gamma * next_state_value)) - self.get_qvalue(state, action)
        
        # Clipping (bom para estabilidade)
        if difference < -100:
             difference = -100
        if difference > 100:
             difference = 100
             
        features = self.get_features(state, action)
        
        # Atualização dos pesos
        # w <- w + alpha * delta * fi(s,a)
        new_w = self.w + self.learning_rate * difference * features
        self.w = new_w

    def train(self, num_episodes: int):
        successful_episodes = 0
        rewards_per_episode = []
        penalties_per_episode = []
        cumulative_successful_episodes = []
        start_time = timer() 

        for episode in range(num_episodes):
            terminated = False
            truncated = False

            state, _ = self.env.reset() # O wrapper lida com a tradução do estado (se houver)

            total_rewards = 0
            self.steps = 0
            total_penalties = 0

            while not (terminated or truncated):
                self.steps += 1
                
                # Para ambientes contínuos, 'state' é o vetor (ex: [-0.5, 0.01])
                # Para ambientes discretos, 'state' é o ID (ex: 32)
                # O extrator de features (fex) lida com ambos
                action = self.choose_action(state)
                
                new_state, reward, terminated, truncated, _ = self.env.step(action)

                if reward == -10: # Específico do Taxi
                    total_penalties += 1

                self.update(state, action, reward, new_state)
                total_rewards += reward

                assert not np.isnan(self.get_weights()).any()
                assert not (any(abs(self.get_weights()) > 1e6)), f"Weigths explosion: {self.get_weights()}"

                if (terminated or truncated):
                    self.epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon) * \
                        np.exp(-self.epsilon_decay_rate * episode)
                    self.epsilon_history.append(self.epsilon)
                    
                    if terminated and total_rewards > -200: # Sucesso para MountainCar e outros
                         successful_episodes += 1
                
                state = new_state

            rewards_per_episode.append(total_rewards)
            penalties_per_episode.append(total_penalties)
            cumulative_successful_episodes.append(successful_episodes)

            if episode % 100 == 0: # Imprime a cada 100 episódios
                end_time = timer()
                execution_time = end_time - start_time
                print(f"Episódio# {episode}/{num_episodes} ({successful_episodes} sucessos)")
                print(f"\tTempo (desde o último log): {execution_time:.2f}s")
                print(f"\tRecompensa Total: {total_rewards}")
                print(f"\tPassos: {self.steps}")
                print(f"\tEpsilon: {self.epsilon:.4f}")
      
                start_time = timer()

        return penalties_per_episode, rewards_per_episode, cumulative_successful_episodes

    def get_weights(self):
        return self.w

    def save(self, filename):
        file = open(filename, 'wb')
        pickle.dump(self, file)
        file.close()

    @staticmethod
    def load_agent(filename):
        file = open(filename, 'rb')
        agent = pickle.load(file)
        return agent