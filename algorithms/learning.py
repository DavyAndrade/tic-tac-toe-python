import json
import random
from collections import defaultdict
from pathlib import Path

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

_Q_APRENDIZ = {}
_HISTORICO_APRENDIZ = {X: [], O: []}
_EPSILON_APRENDIZ = 0.0
_RECOMPENSAS_APRENDIZ = {"vitoria": 2.0, "empate": 1.0, "derrota": -5.0}
_EPISODIO_APRENDIZ = 0
_PERSISTENCIA_APRENDIZ = {"episodes": None, "q": None}
_CONTEXTO_APRENDIZ = {"experiment": None, "phase": "direto", "opponent": None}


def configurar_epsilon(valor: float) -> None:
    global _EPSILON_APRENDIZ
    _EPSILON_APRENDIZ = float(valor)


def resetar_aprendizado() -> None:
    global _EPISODIO_APRENDIZ, _EPSILON_APRENDIZ
    _Q_APRENDIZ.clear()
    for historico in _HISTORICO_APRENDIZ.values():
        historico.clear()
    _EPISODIO_APRENDIZ = 0
    _EPSILON_APRENDIZ = 0.0


def configurar_persistencia(episodes_path, q_path=None) -> None:
    _PERSISTENCIA_APRENDIZ["episodes"] = Path(episodes_path) if episodes_path else None
    _PERSISTENCIA_APRENDIZ["q"] = Path(q_path) if q_path else None
    for path in _PERSISTENCIA_APRENDIZ.values():
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)


def configurar_contexto(experiment=None, phase="direto", opponent=None) -> None:
    _CONTEXTO_APRENDIZ.update(
        experiment=experiment,
        phase=phase,
        opponent=opponent,
    )


def _serializar_estado(state) -> str:
    board, player = state
    return "".join("." if cell == EMPTY else cell for cell in board) + f"|{player}"


def salvar_q(path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    states = {}
    for state, actions in _Q_APRENDIZ.items():
        states[_serializar_estado(state)] = {
            str(cell): {"value": value, "visits": visits}
            for cell, (value, visits) in actions.items()
        }
    payload = {
        "schema_version": 1,
        "algorithm": "monte_carlo_q_table",
        "epsilon": _EPSILON_APRENDIZ,
        "episodes": _EPISODIO_APRENDIZ,
        "states": states,
    }
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    temporary.replace(path)


def carregar_q(path) -> None:
    global _EPISODIO_APRENDIZ
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise ValueError("schema_version de Q desconhecido")
    _Q_APRENDIZ.clear()
    for encoded_state, actions in payload.get("states", {}).items():
        encoded_board, player = encoded_state.rsplit("|", 1)
        board = tuple(EMPTY if cell == "." else cell for cell in encoded_board)
        _Q_APRENDIZ[(board, player)] = {
            int(cell): (data["value"], data["visits"])
            for cell, data in actions.items()
        }
    _EPISODIO_APRENDIZ = payload.get("episodes", 0)


def _persistir_episodio(player, winner, reward, history) -> None:
    global _EPISODIO_APRENDIZ
    _EPISODIO_APRENDIZ += 1
    payload = {
        "schema_version": 1,
        "partida": _EPISODIO_APRENDIZ,
        "player": player,
        "moves": [
            {"state": _serializar_estado(state), "action": cell}
            for state, cell in history
        ],
        "winner": winner,
        "reward": reward,
        **_CONTEXTO_APRENDIZ,
    }
    episodes_path = _PERSISTENCIA_APRENDIZ["episodes"]
    if episodes_path:
        with episodes_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(payload, ensure_ascii=False) + "\n")


def aprendiz(board: Tab, player: str, rng: random.Random) -> Tab:
    cells = get_empty_cells(board)
    state = (board, player)
    values = _Q_APRENDIZ.get(state, {})
    if rng.random() < _EPSILON_APRENDIZ:
        cell = rng.choice(cells)
    else:
        best_value = max((values.get(option, (0.0, 0))[0] for option in cells), default=0.0)
        best_cells = tuple(option for option in cells
                           if values.get(option, (0.0, 0))[0] == best_value)
        cell = rng.choice(best_cells)
    _HISTORICO_APRENDIZ[player].append((state, cell))
    return board[:cell] + (player,) + board[cell + 1:]


def _finalizar_aprendizado(player: str, winner: str | None) -> None:
    if winner is None:
        reward = _RECOMPENSAS_APRENDIZ["empate"]
    elif winner == player:
        reward = _RECOMPENSAS_APRENDIZ["vitoria"]
    else:
        reward = _RECOMPENSAS_APRENDIZ["derrota"]
    history = _HISTORICO_APRENDIZ[player]
    for state, cell in history:
        values = _Q_APRENDIZ.setdefault(state, {})
        value, visits = values.get(cell, (0.0, 0))
        visits += 1
        value += (reward - value) / visits
        values[cell] = (value, visits)
    _persistir_episodio(player, winner, reward, history)
    history.clear()


aprendiz.on_game_end = _finalizar_aprendizado


def fera_aprendizado(board: Tab, player: str, _rng: random.Random) -> Tab:
    cells = get_empty_cells(board)
    cell = max(cells, key=lambda option: (_Q[(board, player)].get(option, 0), -option))
    return board[:cell] + (player,) + board[cell + 1:]
