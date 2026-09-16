import random

from core.board import O, Tab, X, get_empty_cells, get_winner

def _place(board: Tab, player: str, cell: int) -> Tab:
    return board[:cell] + (player,) + board[cell + 1:]


def _winning_cells(board: Tab, player: str) -> tuple[int, ...]:
    return tuple(
        cell for cell in get_empty_cells(board)
        if get_winner(_place(board, player, cell)) == player
    )


def _fork_cells(board: Tab, player: str) -> tuple[int, ...]:
    return tuple(
        cell for cell in get_empty_cells(board)
        if len(_winning_cells(_place(board, player, cell), player)) >= 2
    )


def _safe_forcing_cells(board: Tab, player: str, opponent: str) -> tuple[int, ...]:
    cells = []
    for cell in get_empty_cells(board):
        next_board = _place(board, player, cell)
        threats = _winning_cells(next_board, player)
        if threats and all(
            not _fork_cells(_place(next_board, opponent, threat), opponent)
            for threat in threats
        ):
            cells.append(cell)
    return tuple(cells)


def ingenuo(board: Tab, player: str, rng: random.Random) -> Tab:
    return _place(board, player, rng.choice(get_empty_cells(board)))

def fera_basica(board: Tab, player: str, rng: random.Random) -> Tab:
    """Prioriza vencer, bloquear, garfos, centro, cantos e laterais."""
    cells = get_empty_cells(board)
    opponent = O if player == X else X
    for target in (player, opponent):
        winning_cells = _winning_cells(board, target)
        if winning_cells:
            return _place(board, player, winning_cells[0])
    own_forks = _fork_cells(board, player)
    if own_forks:
        return _place(board, player, own_forks[0])
    opponent_forks = _fork_cells(board, opponent)
    if len(opponent_forks) == 1:
        return _place(board, player, opponent_forks[0])
    if len(opponent_forks) > 1:
        if board[4] == player:
            sides = tuple(cell for cell in (1, 3, 5, 7) if cell in cells)
            if sides:
                return _place(board, player, rng.choice(sides))
        forcing_cells = _safe_forcing_cells(board, player, opponent)
        if forcing_cells:
            return _place(board, player, rng.choice(forcing_cells))
    if 4 in cells:
        return _place(board, player, 4)
    opposite_corners = tuple(
        opposite_cell for cell, opposite_cell in ((0, 8), (2, 6), (6, 2), (8, 0))
        if board[cell] == opponent and opposite_cell in cells
    )
    if opposite_corners:
        return _place(board, player, opposite_corners[0])
    corners = tuple(cell for cell in (0, 2, 6, 8) if cell in cells)
    sides = tuple(cell for cell in (1, 3, 5, 7) if cell in cells)
    return _place(board, player, rng.choice(corners or sides))
