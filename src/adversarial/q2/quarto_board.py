from colorama import Fore

class QuartoBoard:
    def __init__(self):
        self.board = [[None for _ in range(4)] for _ in range(4)]

    def print_board(self):
        """Imprime o tabuleiro alinhado e legível."""
        print(Fore.WHITE + "\n     0   1   2   3")
        print(Fore.WHITE + "   +---+---+---+---+")
        for i, row in enumerate(self.board):
            row_str = f" {i} |" 
            for piece in row:
                if piece is None:
                    cell = "   "
                else:
                    cell = self.format_piece(piece)
                row_str += cell + "|"
            print(Fore.WHITE + row_str)
            print(Fore.WHITE + "   +---+---+---+---+")
        print()

    def format_piece(self, piece):
        """Formata peça com símbolos ASCII, seguro e legível."""
        if piece is None:
            return "   "
        h, c, s, t = piece
 
        shape = "#" if s else "O" 
        height = "▲" if h else "▼"
        color = Fore.CYAN if c else Fore.MAGENTA
        texture = "." if t else " "
        # Os símbolos # e O têm a mesma largura
        return color + f"{height}{shape}{texture}" + Fore.WHITE