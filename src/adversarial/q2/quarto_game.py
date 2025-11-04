from quarto_board import QuartoBoard
from colorama import Fore
import random

class QuartoGame(QuartoBoard):
    def __init__(self):
        super().__init__()
        # (h, c, s, t) -> (Altura, Cor, Forma, Furo)
        self.all_pieces = [(h, c, s, t) for h in [0, 1] for c in [0, 1] for s in [0, 1] for t in [0, 1]]
        self.available_pieces = self.all_pieces.copy()
        self.current = 0  # 0 = humano, 1 = IA
        self.selected_piece = None

    def copy(self):
        new_game = QuartoGame()
        new_game.board = [row.copy() for row in self.board]
        new_game.available_pieces = self.available_pieces.copy()
        new_game.all_pieces = self.all_pieces.copy()
        new_game.current = self.current
        new_game.selected_piece = self.selected_piece
        return new_game

    def available_moves(self):
        """Retorna lista de posições (r, c) vazias."""
        return [(r, c) for r in range(4) for c in range(4) if self.board[r][c] is None]

    def make_move(self, row, col):
        """Coloca a peça selecionada no tabuleiro. Alterna jogador."""
        if self.selected_piece is None:
            raise ValueError("Nenhuma peça selecionada para jogar!")
        if self.board[row][col] is not None:
            raise ValueError("Posição já ocupada!")
        
        self.board[row][col] = self.selected_piece
        self.selected_piece = None
        self.current = 1 - self.current # Troca o jogador

    def select_next_piece(self, idx):
        """Escolhe a próxima peça que o oponente jogará (baseado no índice 0-15)."""
        if idx < 0 or idx >= len(self.all_pieces):
            raise ValueError(f"Índice inválido ({idx}). Deve ser 0-15.")
        piece = self.all_pieces[idx]
        if piece not in self.available_pieces:
            raise ValueError(f"Peça ({idx}) já usada.")
        self.selected_piece = piece
        self.available_pieces.remove(piece)

    def check_win(self):
        lines = []
        lines.extend(self.board)  # horizontais
        lines.extend([[self.board[r][c] for r in range(4)] for c in range(4)])  # verticais
        lines.append([self.board[i][i] for i in range(4)])  # diagonal principal
        lines.append([self.board[i][3 - i] for i in range(4)])  # diagonal secundária

        for line in lines:
            if None in line:
                continue
            # Se não houver linha completa
            for attr in range(4):
                if all(p[attr] == line[0][attr] for p in line):
                    return True
        return False

    def winner(self):
        if self.check_win():
            # Se check_win() é True, o jogador *anterior* (que acabou de jogar) venceu.
            # Como self.current já foi trocado em make_move, o vencedor é o oposto.
            return "Humano" if self.current == 1 else "IA"
        return None

    def print_board_with_piece(self):
        """Mostra o tabuleiro e a peça atual (se houver)."""
        self.print_board()
        if self.selected_piece:
            h, c, s, t = self.selected_piece
     
            shape = "#" if s else "O" 
            height = "▲" if h else "▼"
            color = Fore.CYAN if c else Fore.MAGENTA
            texture = "." if t else " "
            
            piece_str = color + f"{height}{shape}{texture}" + Fore.WHITE
            print(Fore.YELLOW + f"Peça atual para jogar: {piece_str}\n")

    def print_available_pieces(self):
        """Mostra peças disponíveis usando seus índices globais (0-15)."""
        print(Fore.YELLOW + "Peças disponíveis (índices 0-15):")
        count = 0
   
        # Itera sobre ALL_PIECES para usar o índice global (i)
        for i, piece in enumerate(self.all_pieces):
            if piece in self.available_pieces: # Só imprime se estiver disponível
                h, c, s, t = piece
                
                shape = "#" if s else "O" 
                height = "▲" if h else "▼"
                color = Fore.CYAN if c else Fore.MAGENTA
                texture = "." if t else " "
                
                piece_str = color + f"{height}{shape}{texture}" + Fore.WHITE
                
                print(f"{i:2d}: {piece_str}", end="  ")
                count += 1
                if count % 8 == 0:
                    print()
        print("\n")