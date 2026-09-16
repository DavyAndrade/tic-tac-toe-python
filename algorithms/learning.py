import random
from collections import defaultdict

from core.board import EMPTY, O, Tab, X, get_empty_cells, get_winner, is_full


def treinar(episodes: int = 10_000, seed: int = 0):
    """Treina política Q simples por autojogo."""
    rng = random.Random(seed)
    q = defaultdict(dict)
    alpha, gamma = 0.2, 0.95
    for episode in range(episodes):
        board, player, history = (EMPTY,) * 9, X, []
        while not is_full(board) and not get_winner(board):
            cells = get_empty_cells(board)
            state = (board, player)
            values = q[state]
            epsilon = max(0.05, 1 - episode / episodes)
            cell = rng.choice(cells) if rng.random() < epsilon else max(cells, key=lambda c: values.get(c, 0))
            next_board = board[:cell] + (player,) + board[cell + 1:]
            history.append((state, cell, next_board))
            board, player = next_board, O if player == X else X
        winner = get_winner(board)
        for state, cell, next_board in reversed(history):
            reward = 1 if winner == state[1] else -1 if winner else 0
            next_player = O if state[1] == X else X
            future = max(q[(next_board, next_player)].values(), default=0)
            old = q[state].get(cell, 0)
            q[state][cell] = old + alpha * (reward + gamma * future - old)
    return q


_Q = treinar()


def fera_aprendizado(board: Tab, player: str, _rng: random.Random) -> Tab:
    cells = get_empty_cells(board)
    cell = max(cells, key=lambda option: (_Q[(board, player)].get(option, 0), -option))
    return board[:cell] + (player,) + board[cell + 1:]
