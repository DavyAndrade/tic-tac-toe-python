import random

from core.board import O, Tab, X, get_empty_cells, get_winner

def _place(board: Tab, player: str, cell: int) -> Tab:
    return board[:cell] + (player,) + board[cell + 1:]

def ingenuo(board: Tab, player: str, rng: random.Random) -> Tab:
    return _place(board, player, rng.choice(get_empty_cells(board)))

def fera_basica(board: Tab, player: str, rng: random.Random) -> Tab:
    """Prioriza vencer, bloquear, centro, cantos e qualquer casa vazia."""
    cells = get_empty_cells(board)
    opponent = O if player == X else X
    for target in (player, opponent):
        for cell in cells:
            if get_winner(_place(board, target, cell)) == target:
                return _place(board, player, cell)
    if 4 in cells:
        return _place(board, player, 4)
    corners = tuple(cell for cell in (0, 2, 6, 8) if cell in cells)
    return _place(board, player, rng.choice(corners or cells))
