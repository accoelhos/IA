import numpy as np
from environment import Environment # Precisamos disso para o tipo 'env'

class Tilecoder:
    """
    Implementação de Tile Coding (Codificação por Ladrilhos).
    """
    def __init__(self, env: Environment, num_tilings: int, tiles_per_tiling: int):
        self.env = env
        self.num_tilings = num_tilings # Número de grades 
        self.tiles_per_tiling = tiles_per_tiling # Divisões por dimensão
        
        self.dim = len(self.env.observation_space.low) # Dimensão do estado (2 para MountainCar)

        self.min_val = self.env.observation_space.low
        self.max_val = self.env.observation_space.high
        
        # Tamanho de cada "ladrilho" por dimensão
        self.tile_size = (self.max_val - self.min_val) / (self.tiles_per_tiling - 1)
        
        # Número total de tiles em UMA grade (ex: 10 * 10 = 100)
        self.num_tiles_per_tiling = self.tiles_per_tiling ** self.dim
        
        # Número total de tiles em TODAS as grades (ex: 100 * 8 = 800)
        self.num_tiles_total = self.num_tiles_per_tiling * self.num_tilings
        
        self.actions = self.env.action_space.n # Número de ações

        # Offsets de deslocamento para cada grade
        # Cria vetores de offset para cada grade
        
        self.offsets = (
            np.arange(self.num_tilings).reshape(-1, 1) * (self.max_val - self.min_val) / (self.tiles_per_tiling - 1) / self.num_tilings
        ) % self.tile_size


    def get_num_features_total(self):
        """
        Retorna o número total de features (pesos theta) no vetor global.
        É o número total de tiles * número de ações.
        """
        return self.num_tiles_total * self.actions

    def get_features_indices(self, state):
        """
        Calcula os índices dos tiles ativados para um dado estado.
        Retorna uma lista de índices (inteiros), um para cada tiling.
        """
        # Normalizar o estado para a "escala de tiles"
        normalized_state = (state - self.min_val)
        
        active_tiles_indices = []
        
        for i in range(self.num_tilings):
            # Adicionar o offset de deslocamento para esta grade
            offset_state = normalized_state + self.offsets[i]
            
            # Calcular as coordenadas do tile (ex: [3, 5])
            tile_coords = np.floor(offset_state / self.tile_size).astype(int)
            
            # Mapear as coordenadas para um índice único 
            # Usando base (tiles_per_tiling)
            tile_index_in_tiling = 0
            for j in range(self.dim):
                tile_index_in_tiling += tile_coords[j] * (self.tiles_per_tiling ** j)
            
            # Adicionar o offset global da grade (ex: 35 + 100*i)
            global_tile_index = tile_index_in_tiling + (i * self.num_tiles_per_tiling)
            
            active_tiles_indices.append(global_tile_index)
            
        return active_tiles_indices

    def get_features(self, state, action):
        """
        Retorna o vetor de features ONE-HOT (fi(s,a)) para o par (estado, ação).
        """
        features_indices = self.get_features_indices(state)
        
        # Criar o vetor de features global (theta)
        one_hot_vector = np.zeros(self.get_num_features_total())
        
        for tile_idx in features_indices:
            # Calcular a posição global no vetor theta para a ação específica
            global_theta_index = int(tile_idx + (self.num_tiles_total * action))
            
            # Checagem de segurança (pode ser removida após o debug)
            if global_theta_index < 0 or global_theta_index >= self.get_num_features_total():
                print(f"Erro de índice! state={state}, idx={tile_idx}, g_idx={global_theta_index}")
                continue

            one_hot_vector[global_theta_index] = 1.0
            
        return one_hot_vector