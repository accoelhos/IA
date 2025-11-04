from quarto_game import QuartoGame
from quarto_minimax import best_move_quarto
from quarto_mcts import quarto_mcts
from colorama import Fore, init
import random
import time

init(autoreset=True)


# Funções auxiliares
def end_game_message(game: QuartoGame):
    game.print_board_with_piece()
    winner = game.winner()
    if winner:
        color = Fore.GREEN if winner == "Humano" else Fore.RED
        print(color + "\n═══════════════════════════════")
        print(color + f"{winner} venceu a partida!")
        print(color + "═══════════════════════════════\n")
    else:
        print(Fore.YELLOW + "\nEmpate! Ninguém venceu.\n")

def human_turn(game: QuartoGame):
    """Vez do humano: coloca peça e escolhe próxima peça para IA"""
    # Colocar a peça no tabuleiro
    while True:
        try:
            game.print_board_with_piece()
            row = int(input(Fore.CYAN + "Linha (0-3): "))
            col = int(input(Fore.CYAN + "Coluna (0-3): "))
            if (row, col) not in game.available_moves():
                print(Fore.RED + "Posição inválida ou ocupada.")
                continue
            game.make_move(row, col)
            break
        except (ValueError, IndexError):
            print(Fore.RED + "Entrada inválida. Digite números válidos.")

    # Se o jogo acabou, não pede próxima peça
    if game.check_win() or not game.available_moves():
        return

    # Escolher próxima peça para IA
    while True:
        try:
            game.print_available_pieces()
            # O input do usuário deve ser o índice global (0-15)
            next_idx = int(input(Fore.YELLOW + "Escolha a próxima peça para a IA (índice 0-15): "))
            game.select_next_piece(next_idx)
            break
        except (ValueError, IndexError):
            print(Fore.RED + "Índice inválido ou peça já usada. Escolha outra peça.")

def ai_turn(game: QuartoGame, ai_function, ai_name="IA"):
    """Vez da IA: coloca peça e escolhe próxima peça para humano"""
    print(Fore.BLUE + f"\n{ai_name} está pensando...")
    time.sleep(1)

    move = ai_function(game) 
    
    if move is None:
        # Fallback caso IA não retorne nada
        available_pos = game.available_moves()
        if not available_pos:
            return # Jogo acabou
        row, col = random.choice(available_pos)
        
        # Pega uma peça aleatória que ainda não foi usada
        available_next = [idx for idx, p in enumerate(game.all_pieces) if p in game.available_pieces and p != game.selected_piece]
        if not available_next:
             next_piece_index = -1 # Nenhuma peça para escolher
        else:
            next_piece_index = random.choice(available_next)
        
        move = (row, col, next_piece_index)

    # Coloca a peça no tabuleiro
    game.make_move(move[0], move[1])
    print(Fore.BLUE + f"{ai_name} colocou peça em ({move[0]}, {move[1]})")
    game.print_board_with_piece()

    # Se o jogo acabou, não escolhe próxima peça
    if game.check_win() or not game.available_moves():
        return

    # Seleciona próxima peça para humano
    try:
        if move[2] != -1: # -1 é o índice 'dummy' para fim de jogo
            game.select_next_piece(move[2])
            print(Fore.BLUE + f"{ai_name} escolheu a próxima peça para você.\n")
        else:
            print(Fore.BLUE + f"{ai_name} jogou a última peça.\n")
            
    except ValueError:
        # Fallback caso peça já tenha sido usada
        available_idx_list = [idx for idx, p in enumerate(game.all_pieces) if p in game.available_pieces]
        if available_idx_list:
            fallback_idx = random.choice(available_idx_list)
            game.select_next_piece(fallback_idx)
            print(Fore.BLUE + f"{ai_name} escolheu uma peça aleatória para você (fallback).\n")
    time.sleep(1)



# Loop principal de jogo
def play_human_vs_ai(ai_function, ai_name="IA"):
    """Loop completo de jogo humano vs IA"""
    game = QuartoGame()

    # Peça inicial aleatória
    start_idx = random.randrange(len(game.all_pieces))
    game.select_next_piece(start_idx)

    while not game.check_win() and game.available_moves():
        if game.current == 0:
            human_turn(game)
        else:
            # Verifica se há peça selecionada para a IA jogar
            if game.selected_piece is None:
                # Isso acontece se o humano jogou a última peça e ganhou
                break
            ai_turn(game, ai_function, ai_name)
            
        # Checagem extra caso o humano tenha jogado a última peça e não ganhou
        if not game.available_moves() and game.selected_piece is None:
            break

    end_game_message(game)


# Tutorial
def show_tutorial():
    print(Fore.CYAN + "\n═══════════════════════════════════════════")
    print(Fore.CYAN + " BEM-VINDO AO TUTORIAL DO JOGO QUARTO 🎓")
    print(Fore.CYAN + "═══════════════════════════════════════════\n")
    time.sleep(1)

    print(Fore.YELLOW + "OBJETIVO DO JOGO:")
    print(Fore.WHITE + "Formar uma linha (horizontal, vertical ou diagonal) com 4 peças que compartilhem um mesmo atributo.\n")
    time.sleep(1)

    print(Fore.YELLOW + "AS PEÇAS:")
    print(Fore.WHITE + "Cada peça tem 4 características binárias:")
    print(" - Forma: " + Fore.CYAN + "# Quadrada" + Fore.WHITE + " ou " + Fore.MAGENTA + "O Redonda")
    print(" - Cor:   " + Fore.CYAN + "Ciano" + Fore.WHITE + " ou " + Fore.MAGENTA + "Magenta")
    print(" - Altura: " + Fore.WHITE + "Baixa (▼)" + " ou Alta (▲)")
    print(" - Furo:   " + Fore.WHITE + "Sólida ( )" + " ou Furada (.)\n")
    time.sleep(1)

    print(Fore.YELLOW + "COMO JOGAR:")
    print(Fore.WHITE + "1. O jogo começa com uma peça sorteada.")
    print("2. Na sua vez, coloque a peça atual no tabuleiro (linha e coluna).")
    print("3. Escolha a PRÓXIMA PEÇA que o oponente jogará (pelo índice 0-15).")
    print("4. O jogo alterna entre você e a IA até formar um 'Quarto'.\n")
    time.sleep(2)

    print(Fore.YELLOW + "COMO VENCER:")
    print(Fore.WHITE + "Você vence quando 4 peças em linha compartilham ao menos um mesmo atributo.\n")
    # --- TUTORIAL CORRIGIDO ---
    print(Fore.MAGENTA + "Exemplo: O▲.  O▼.  O▲.  O▼   → todas são REDONDAS → vitória!\n")
    time.sleep(2)

    print(Fore.CYAN + "═══════════════════════════════════════════\n")

# ----------------------
# Menu principal
# ----------------------
def main_menu():
    while True:
        print(Fore.CYAN + "\n========== MENU QUARTO ==========")
        print("1. Humano vs Minimax (Fácil/Médio)")
        print("2. Humano vs MCTS (Desafiador)")
        print("3. Tutorial do Jogo")
        print("4. Sair")
        op = input(Fore.YELLOW + "Escolha uma opção: ")

        if op == "1":
            # Depth 2 é rápido e joga razoavelmente
            play_human_vs_ai(lambda g: best_move_quarto(g, depth=2), ai_name="Minimax")
        elif op == "2":
            # 5000 iterações ou 2 segundos, o que vier primeiro
            play_human_vs_ai(lambda g: quarto_mcts(g, iterations=5000, time_limit=2.0), ai_name="MCTS")
        elif op == "3":
            show_tutorial()
        elif op == "4":
            print(Fore.MAGENTA + "Encerrando o jogo. Até a próxima!")
            break
        else:
            print(Fore.RED + "Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main_menu()