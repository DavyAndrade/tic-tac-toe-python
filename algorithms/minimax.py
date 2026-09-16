import random
from functools import lru_cache
from typing import List, Optional, Tuple

from core.board import O, Tab, X, get_empty_cells, get_winner, is_full

@lru_cache(maxsize=None)
def minimax(board: Tab, player: str, depth: int = 0) -> Tuple[int, Optional[int]]:
    winner = get_winner(board)
    if winner == X:
        return 10 - depth, None
    if winner == O:
        return depth - 10, None
    if is_full(board):
        return 0, None
    opponent = O if player == X else X
    candidates: List[Tuple[int, int]] = []
    for cell in get_empty_cells(board):
        new_board = board[:cell] + (player,) + board[cell + 1:]
        score, _ = minimax(new_board, opponent, depth + 1)
        candidates.append((score, cell))
    return (max if player == X else min)(candidates, key=lambda item: item[0])

def fera_minimax(board: Tab, player: str, _rng: random.Random) -> Tab:
    _, cell = minimax(board, player)
    if cell is None:
        cell = get_empty_cells(board)[0]
    return board[:cell] + (player,) + board[cell + 1:]
