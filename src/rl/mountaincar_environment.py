import numpy as np
from environment import Environment

class MountainCarEnvironment(Environment):
    def __init__(self, env, num_pos_bins=20, num_vel_bins=20):
        super().__init__(env)
        
        self.num_pos_bins = num_pos_bins
        self.num_vel_bins = num_vel_bins

        # espaço de observação (estado) do MountainCar tem 2 valores
        # state[0] = posição (de -1.2 a 0.6)
        # state[1] = velocidade (de -0.07 a 0.07)
        
        #  "bordas" dos bins para Posição e Velocidade
        # Para 10 bins, precisa de 9 "divisores" (o -1 é pq linspace inclui os dois lados)
        self.pos_bins = np.linspace(
            self.env.observation_space.low[0], 
            self.env.observation_space.high[0], 
            self.num_pos_bins - 1
        )
        self.vel_bins = np.linspace(
            self.env.observation_space.low[1], 
            self.env.observation_space.high[1], 
            self.num_vel_bins - 1
        )

    def get_num_states(self):
        #número total de estados é a combinação de todos os bins

        return self.num_pos_bins * self.num_vel_bins

    def get_num_actions(self):
        #  ambiente já tem ações discretas (0: esquerda, 1: neutro, 2: direita)
        return self.env.action_space.n

  # a função principal de discretização
    def get_state_id(self, state):
      
        pos, vel = state
        
        # np.digitize encontra em qual bin o valor contínuo se encaixa

        pos_bin = np.digitize(pos, self.pos_bins)
        vel_bin = np.digitize(vel, self.vel_bins)
        
        # mapeamos o par (pos_bin, vel_bin) para um ID único
        return pos_bin * self.num_vel_bins + vel_bin

    def get_random_action(self):
        return self.env.action_space.sample()