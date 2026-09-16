from typing import Optional, Tuple

Tab = Tuple[str, ...]
LINES = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
X, O, EMPTY = "X", "O", " "
PLAYERS = (X, O)

def tab_vazio() -> Tab:
    return (EMPTY,) * 9

def get_winner(board: Tab) -> Optional[str]:
    for a, b, c in LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None

def is_full(board: Tab) -> bool:
    return EMPTY not in board

def get_empty_cells(board: Tab) -> Tuple[int, ...]:
    return tuple(i for i, value in enumerate(board) if value == EMPTY)
