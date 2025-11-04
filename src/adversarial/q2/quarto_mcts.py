import math, random, time

class Node:
    def __init__(self, game, parent=None, move=None):
        self.game = game.copy() # Armazena uma cópia do estado
        self.parent = parent
        self.move = move # move é (row, col, next_piece_idx)
        self.children = []
        self.visits = 0
        # self.wins é da perspectiva do JOGADOR ATUAL deste nó
        # (se o nó é da IA, wins = vitórias da IA; se é do Humano, wins = vitórias do Humano)
        self.wins = 0
        self.untried_moves = self.get_all_moves(game)
        random.shuffle(self.untried_moves)

    def get_all_moves(self, game_state):
        """Gera todas as jogadas (posição + próxima peça) possíveis."""
        moves = []
        available_pos = game_state.available_moves()
        if not available_pos:
            return []
            
        available_next_pieces = [p for p in game_state.available_pieces if p != game_state.selected_piece]
        
        if not available_next_pieces:
            return [(r, c, -1) for r, c in available_pos] # -1 como índice "dummy"

        for row, col in available_pos:
            for idx, piece in enumerate(game_state.all_pieces):
                if piece in available_next_pieces:
                    moves.append((row, col, idx))
        return moves

    def ucb1(self, c=1.41): # c = sqrt(2)
        if self.visits == 0:
            return float('inf')
        if self.parent is None or self.parent.visits == 0:
             return float('inf') # Prioriza nós não visitados
             
        # UCB1: Exploração + Explotação
        # self.wins / self.visits = Explotação (quão bom é este nó)
        # c * sqrt(log(self.parent.visits) / self.visits) = Exploração (quão incerto é este nó)
        return (self.wins / self.visits) + c * math.sqrt(math.log(self.parent.visits) / self.visits)

    def select(self):
        """Seleciona o filho com maior UCB1."""
        return max(self.children, key=lambda child: child.ucb1())

    def expand(self):
        """Expande um nó filho a partir de um movimento não tentado."""
        if not self.untried_moves:
            return None 
            
        move = self.untried_moves.pop() # move é (r, c, idx)
        new_game = self.game.copy()

        try:
            new_game.make_move(move[0], move[1]) # Passo 1
            if not new_game.check_win() and move[2] != -1:
                new_game.select_next_piece(move[2]) # Passo 2
        except ValueError:
            # Se o movimento for inválido (raro), tenta expandir o próximo
            return self.expand() if self.untried_moves else None

        child = Node(new_game, parent=self, move=move)
        self.children.append(child)
        return child

    def update(self, result_player):
        """
        Atualiza visitas e vitórias (backpropagation).
        result_player (0 ou 1) é o jogador que venceu a simulação.
        """
        self.visits += 1
        # O nó pai representa o jogador OPOSTO ao nó atual.
        # O 'current' do jogo no nó representa o jogador que fará a *próxima* jogada.
        # O jogador que *fez a jogada* para chegar a ESTE nó é (1 - game.current).
        player_who_moved_to_this_node = 1 - self.game.current
        
        if player_who_moved_to_this_node == result_player:
            self.wins += 1


def quarto_mcts(game, iterations=500, time_limit=None):
    root_game = game.copy()
    root = Node(root_game)
    # O jogador na raiz (quem está prestes a jogar)
    root_player = root_game.current 
    
    start_time = time.time()
    
    actual_iterations = 0
    while True:
        actual_iterations += 1
        if actual_iterations > iterations:
            break
        if time_limit and (time.time() - start_time) > time_limit:
            break

        node = root
        sim_game = root_game.copy()

        # 1. Seleção (Select)
        while not node.untried_moves and node.children:
            node = node.select()
            # Atualiza o sim_game para o estado do nó filho
            sim_game = node.game.copy()

        # 2. Expansão (Expand)
        if node.untried_moves:
            child_node = node.expand()
            if child_node:
                node = child_node
                sim_game = node.game.copy() # Jogo já avançado na expansão

        # 3. Simulação (Playout)
        # O estado em 'sim_game' é o resultado da expansão.
        # Agora simulamos aleatoriamente até o fim.
        while not sim_game.check_win() and (sim_game.available_moves() or sim_game.selected_piece):
            # Se não há mais movimentos (tabuleiro cheio) mas ainda há uma peça selecionada
            if not sim_game.available_moves() and sim_game.selected_piece:
                 break # Jogo empata (não há onde colocar)
                 
            # Gera movimentos aleatórios
            moves = node.get_all_moves(sim_game)
            if not moves:
                break # Fim da simulação
            
            move = random.choice(moves)
            
            try:
                sim_game.make_move(move[0], move[1])
                if not sim_game.check_win() and move[2] != -1:
                    sim_game.select_next_piece(move[2])
            except ValueError:
                break # Pára a simulação se algo der errado

        # 4. Backpropagation
        winner = sim_game.winner()
        result_player = -1 # -1 para empate
        if winner == "Humano":
            result_player = 0
        elif winner == "IA":
            result_player = 1
            
        # O 'result_player' (0, 1 ou -1) é propagado para cima
        while node is not None:
            # Atualiza o nó baseado no vencedor (result_player)
            node.visits += 1
            # Quem é o jogador que o nó PAI representa?
            # O 'current' do jogo no nó atual é quem JOGA *A PARTIR* deste nó.
            # O nó PAI é o jogador anterior, (1 - node.game.current).
            if node.parent:
                player_of_parent_node = 1 - node.game.current
                if player_of_parent_node == result_player:
                    node.wins += 1 # O pai (que escolheu este nó) ganhou
            node = node.parent

    # Retorna o movimento do filho mais visitado (política mais robusta)
    if not root.children:
        moves = root.get_all_moves(root_game)
        return random.choice(moves) if moves else None

    best_child = max(root.children, key=lambda c: c.visits)
    return best_child.move