"""Estrategia de exemplo: outro aluno pode importar."""
import random
from main import Tab

def avarento(board, player, rng):
    """Joga ganhar se pode, senao bloqueia, senao aleatorio."""
    from main import get_winner, is_full, get_empty_cells, LINES
    opponent = "O" if player == "X" else "X"
    cells = get_empty_cells(board)

    # tenta ganhar
    for c in cells:
        b = board[:c] + (player,) + board[c+1:]
        if get_winner(b) == player:
            return b

    # tenta bloquear
    for c in cells:
        b = board[:c] + (opponent,) + board[c+1:]
        if get_winner(b) == opponent:
            b = board[:c] + (player,) + board[c+1:]
            return b

    return board[:cells[0]] + (player,) + board[cells[0]+1:]
