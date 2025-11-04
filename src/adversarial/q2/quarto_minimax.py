import random

def evaluate(game, player_at_root):
    """
    Avalia o estado do jogo.
    player_at_root é o jogador que iniciou a chamada do minimax (quem queremos que vença).
    """
    winner = game.winner()
    
    if winner:
        # Verifica se o vencedor é o jogador que estamos otimizando
        if (winner == "IA" and player_at_root == 1) or \
           (winner == "Humano" and player_at_root == 0):
            return 1000 + len(game.available_moves()) # Venceu! (Prefere vitórias rápidas)
        else:
            return -1000 - len(game.available_moves()) # Perdeu! (Prefere derrotas lentas)

    if not game.available_moves() and game.selected_piece is None:
        return 0 # Empate

    # Avaliação neutra se o jogo não acabou
    return 0

def minimax(game, depth, maximizing, player_at_root, alpha, beta):
    """
    Executa o minimax com poda alpha-beta.
    player_at_root: O jogador (0 ou 1) que chamou o best_move.
    """
    # Condições de parada
    if depth == 0 or game.check_win() or (not game.available_moves() and game.selected_piece is None):
        return evaluate(game, player_at_root)

    if maximizing:
        max_eval = float('-inf')
        for move in get_all_moves(game):
            new_game = game.copy()
            row, col, next_idx = move
            
   
            try:
                new_game.make_move(row, col) # Passo 1: Coloca peça
                # Se o jogo não acabou após colocar, seleciona a próxima
                if not new_game.check_win() and next_idx != -1:
                    new_game.select_next_piece(next_idx) # Passo 2: Seleciona próxima
            except ValueError:
                continue # Movimento inválido (ex: peça já usada), pular

            eval = minimax(new_game, depth - 1, False, player_at_root, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break # Poda Beta
        return max_eval
    
    else: # Minimizing
        min_eval = float('inf')
        for move in get_all_moves(game):
            new_game = game.copy()
            row, col, next_idx = move

            try:
                new_game.make_move(row, col) # Passo 1
                if not new_game.check_win() and next_idx != -1:
                    new_game.select_next_piece(next_idx) # Passo 2
            except ValueError:
                continue 

            eval = minimax(new_game, depth - 1, True, player_at_root, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break # Poda Alpha
        return min_eval

def get_all_moves(game):
    """Gera todas as jogadas (posição + próxima peça) possíveis."""
    moves = []
    available_pos = game.available_moves()
    if not available_pos:
        return []
        
    # Peças que o oponente poderá jogar
    available_next_pieces = [p for p in game.available_pieces if p != game.selected_piece]
    
    if not available_next_pieces:
        # Este é o último movimento (só há a peça atual para jogar)
        # Retorna jogadas para qualquer posição, com -1 como índice "dummy"
        return [(r, c, -1) for r, c in available_pos]

    for row, col in available_pos:
        for idx, piece in enumerate(game.all_pieces):
            if piece in available_next_pieces:
                moves.append((row, col, idx))
    return moves

def best_move_quarto(game, depth=2):
    player_at_root = game.current # 0 = Humano, 1 = IA
    best_score = float('-inf')
    best_move = None
    
    moves = get_all_moves(game)
    if not moves:
        return None # Jogo acabou

    random.shuffle(moves) # Para variedade

    for move in moves:
        new_game = game.copy()
        row, col, next_piece_index = move
  
        try:
            new_game.make_move(row, col) # Passo 1
            if not new_game.check_win() and next_piece_index != -1:
                new_game.select_next_piece(next_piece_index) # Passo 2
        except ValueError:
            continue # Pula movimento inválido

        # (Profundidade - 1) pois já fizemos um movimento
        # 'False' pois é a vez do oponente (minimizador)
        score = minimax(new_game, depth - 1, False, player_at_root, float('-inf'), float('inf')) 

        if score > best_score:
            best_score = score
            best_move = move
            
    return best_move