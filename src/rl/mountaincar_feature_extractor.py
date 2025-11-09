import numpy as np
from feature_extractor import FeatureExtractor
from tile_coder import Tilecoder

class MountainCarFeatureExtractor(FeatureExtractor):
    
    def __init__(self, env, num_tilings=8, tiles_per_tiling=8):

        # (self.env = env) é definido aqui
        self.env = env 
        self.num_actions = env.action_space.n
        
        # Inicializa o Tilecoder
        self.tilecoder = Tilecoder(env, num_tilings, tiles_per_tiling)

    def get_num_features(self):
        """
        Retorna o número total de features (tamanho do vetor theta).
        """
        return self.tilecoder.get_num_features_total()

    def get_features(self, state, action):
        """
        Retorna o vetor de features one-hot do tilecoder.
        """
        return self.tilecoder.get_features(state, action)

    def is_terminal_state(self, state):
        # O estado terminal no MountainCar é quando a posição (state[0]) >= 0.5
        return state[0] >= 0.5


    def get_action_one_hot_encoded(self, action):
        """
        Método "fantasma" para satisfazer a classe abstrata FeatureExtractor.
        """
        return np.array([])