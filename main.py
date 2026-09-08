"""
TicTacToe - Paradigma funcional/data-driven.

Board: lista imutável de 9 posições, valores 'X', 'O' ou ' '.
Indíces 0..8 mapeados a:

    0 | 1 | 2
    3 | 4 | 5
    6 | 7 | 8

Algoritmos:
  - naive  : joga aleatoriamente.
  - bee    : minimax puro; nunca perde (ganha ou empata).
  - human  : lê input do usuário.

Tudo como funções puras retornando novos boards (sem mutar).
"""
import json
import os
import random
import sys
from functools import lru_cache
from typing import Callable, List, Optional, Tuple

Board = Tuple[str, ...]

LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)

X = "X"
O = "O"
EMPTY = " "
PLAYERS = (X, O)


def empty_board() -> Board:
    return (EMPTY,) * 9


def get_winner(board: Board) -> Optional[str]:
    for a, b, c in LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_full(board: Board) -> bool:
    return EMPTY not in board


def get_empty_cells(board: Board) -> Tuple[int, ...]:
    return tuple(i for i, v in enumerate(board) if v == EMPTY)


@lru_cache(maxsize=None)
def minimax(board: Board, player: str, depth: int = 0) -> Tuple[int, Optional[int]]:
    """
    Retorna (score, melhor_jogada) para 'player'.
    Score positivo favorece X, negativo favorece O.
    Profundidade desempata empates rápidos (ganha mais cedo).

    Cacheado: função pura sobre (board, player, depth) e o número de
    posições alcançáveis de tic-tac-toe é pequeno (~5000), então o cache
    evita recalcular a árvore inteira a cada lance de 'bee' e torna
    torneios de dezenas de milhares de partidas viáveis no mesmo processo.
    """
    winner = get_winner(board)
    if winner == X:
        return (10 - depth, None)
    if winner == O:
        return (depth - 10, None)
    if is_full(board):
        return (0, None)

    opponent = O if player == X else X
    candidates: List[Tuple[int, int]] = []

    for cell in get_empty_cells(board):
        new_board = board[:cell] + (player,) + board[cell + 1:]
        score, _ = minimax(new_board, opponent, depth + 1)
        candidates.append((score, cell))

    if not candidates:
        return (0, None)

    if player == X:
        best = max(candidates, key=lambda x: x[0])
    else:
        best = min(candidates, key=lambda x: x[0])
    return best


def naive(board: Board, player: str, rng: random.Random) -> Board:
    """Joga aleatoriamente numa célula vazia."""
    cell = rng.choice(get_empty_cells(board))
    return board[:cell] + (player,) + board[cell + 1:]


def bee(board: Board, player: str, _rng: random.Random) -> Board:
    """Minimax; nunca perde."""
    _, cell = minimax(board, player)
    if cell is None:
        cell = get_empty_cells(board)[0]
    return board[:cell] + (player,) + board[cell + 1:]


def human(board: Board, player: str, _rng: random.Random) -> Board:
    """Lê coordenada 0-8 do input até posição válida."""
    while True:
        try:
            raw = input(f"Jogador {player} -> escolha 0-8: ").strip()
        except EOFError:
            return board
        try:
            cell = int(raw)
        except ValueError:
            print("Digite um número 0-8.")
            continue
        if cell not in get_empty_cells(board):
            print("Posição ocupada ou fora do intervalo.")
            continue
        return board[:cell] + (player,) + board[cell + 1:]


STRATEGIES: dict = {
    "naive": naive,
    "bee": bee,
    "human": human,
}

REGISTRY_FILE = "strategies.json"
_external_registry: dict = {}  # nome -> ref (arquivo:funcao)


def _load_registry() -> None:
    """Carrega estratégias externas registadas do arquivo de disco."""
    global _external_registry
    if os.path.exists(REGISTRY_FILE):
        try:
            with open(REGISTRY_FILE) as f:
                _external_registry = json.load(f)
        except (json.JSONDecodeError, OSError):
            _external_registry = {}


def register_strategy(name: str, ref: str) -> None:
    """Registra estratégia (name, ref) de forma persistente no disco."""
    _external_registry[name] = ref
    with open(REGISTRY_FILE, "w") as f:
        json.dump(_external_registry, f, indent=2)
    try:
        STRATEGIES[name] = load_external(ref)
    except (ImportError, AttributeError, ValueError):
        pass


def load_external(ref: str) -> Callable:
    """
    Carrega função de estratégia externa.
    Formato: 'arquivo.py:nome_funcao' ou 'modulo:nome_funcao'.
    Ou nome interno ('naive', 'bee', 'human').
    Assinatura: fn(board, player, rng) -> Board
    """
    import importlib.util

    if ref in STRATEGIES:
        return STRATEGIES[ref]

    if ":" in ref:
        path, attr = ref.split(":", 1)
    else:
        raise ValueError(
            f"'{ref}' não é estratégia interna. Use 'arquivo.py:funcao' ou "
            f"nome interno {list(STRATEGIES)}"
        )

    spec = importlib.util.spec_from_file_location("external_strat", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Não carregou módulo: {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fn = getattr(mod, attr, None)
    if fn is None:
        raise AttributeError(f"Função '{attr}' não encontrada em {path}")
    return fn


def resolve_strategy(ref: str) -> Tuple[str, Callable]:
    """Resolve nome interno/registrado ou 'arq.py:fn' → (label, callable)."""
    if ref in _external_registry:
        ref = _external_registry[ref]
    fn = load_external(ref)
    return getattr(fn, "__name__", ref), fn


def render(board: Board) -> str:
    rows = []
    for r in range(3):
        row = " | ".join(board[r * 3 + c] or str(r * 3 + c) for c in range(3))
        rows.append(row)
    return "\n---------\n".join(rows)


def draw_board(board: Board, cells: tuple = ()) -> None:
    """Desenha tabuleiro visual com índices como referência."""
    symbols = []
    for i in range(9):
        if board[i] != EMPTY:
            symbols.append(board[i])
        elif i in cells:
            symbols.append("*")
        else:
            symbols.append(str(i))
    print()
    print(f" {symbols[0]} | {symbols[1]} | {symbols[2]} ")
    print("---+---+---")
    print(f" {symbols[3]} | {symbols[4]} | {symbols[5]} ")
    print("---+---+---")
    print(f" {symbols[6]} | {symbols[7]} | {symbols[8]} ")
    print()


def play_with_view(fn1: Callable, fn2: Callable, seed: int = 0) -> dict:
    """Joga partida mostrando tabuleiro antes e depois de cada jogada. P1=X, P2=O."""
    board = empty_board()
    rng = random.Random(seed)
    players = ((X, fn1), (O, fn2))
    move_index = 0
    winner = None

    for _ in range(9):
        player, fn = players[move_index % 2]
        if fn is human:
            print(f"--- Tabuleiro atual (sua vez: {player}) ---")
            draw_board(board)
        board = fn(board, player, rng)
        winner = get_winner(board)
        move_index += 1
        print(f"--- Jogada {move_index} ({player}) ---")
        draw_board(board)
        if winner or is_full(board):
            break

    v = score_for(winner)
    result = {"J1": fn1.__name__, "J2": fn2.__name__, "V": v,
              "N": move_index, "board": list(board), "rounds": move_index}
    print(f"Resultado: {v} ({'J1 vence' if v == 1 else 'J2 vence' if v == -1 else 'Empate'})")
    return result


def view_games(path: str) -> None:
    """Navegador interativo de resultados num JSON. tópicos: n, p, q."""
    with open(path) as f:
        results = json.load(f)
    n = len(results)
    i = 0
    while True:
        g = results[i]
        print(f"\n=== Partida {i + 1}/{n} ===")
        print(f"J1={g['J1']}  V={g['V']}  J2={g['J2']}  N={g['N']}  rounds={g['rounds']}")
        v_map = {1: "J1 vence", -1: "J2 vence", 0: "Empate"}
        print(f"Status: {v_map.get(g['V'], '??')}")
        board_t = tuple("." if c == " " else c for c in g["board"])
        draw_board(board_t)
        cmd = input("n(ext) p(prev) g(o) <num> q(uit): ").strip().lower()
        if cmd == "q" or cmd == "":
            break
        elif cmd == "n":
            i = min(i + 1, n - 1)
        elif cmd == "p":
            i = max(i - 1, 0)
        elif cmd == "g":
            show_game_log(g)
        elif cmd.isdigit():
            i = max(0, min(int(cmd) - 1, n - 1))


SCORE_X = 1
SCORE_O = -1
SCORE_DRAW = 0


def score_for(winner: Optional[str]) -> int:
    """Score: 1 quem joga X vence, -1 quem joga O vence, 0 empate."""
    if winner == X:
        return SCORE_X
    if winner == O:
        return SCORE_O
    return SCORE_DRAW


def play_game(p1_fn: Callable, p2_fn: Callable, seed: int = 0) -> dict:
    """
    Um jogo. p1 joga X, p2 joga O.
    Score V: 1=J1(venceu X), -1=J2(venceu O), 0=DRAW.
    """
    board = empty_board()
    rng = random.Random(seed)
    log: List[dict] = []

    players = ((X, p1_fn), (O, p2_fn))
    move_index = 0
    winner = None

    for _ in range(9):
        player, fn = players[move_index % 2]
        board = fn(board, player, rng)
        winner = get_winner(board)
        move_index += 1
        log.append({
            "J1": p1_fn.__name__,
            "J2": p2_fn.__name__,
            "V": score_for(winner),
            "N": move_index,
            "board": list(board),
            "rounds": move_index,
        })
        if winner or is_full(board):
            break

    final = winner or None
    v = score_for(final)
    log.append({
        "J1": p1_fn.__name__,
        "J2": p2_fn.__name__,
        "V": v,
        "N": move_index,
        "board": list(board),
        "rounds": move_index,
    })
    return {"J1": p1_fn.__name__, "J2": p2_fn.__name__, "V": v,
            "N": move_index, "board": list(board), "rounds": move_index, "log": log}


def compete(name1: str, name2: str, rounds: int, start_player: int = 0,
            seed: int = 42) -> List[dict]:
    """
    Faz name1 vs name2 (nomes internos) por 'rounds' jogos.
    start_player=0: X sempre p1. start_player=1: X alterna.
    Usa seed fixa para reprodutibilidade (naive).
    """
    fn1 = STRATEGIES[name1]
    fn2 = STRATEGIES[name2]
    return compete_callable(fn1, fn2, name1, name2, rounds, start_player, seed)


def compete_callable(fn1: Callable, fn2: Callable, label1: str, label2: str,
                     rounds: int, start_player: int = 0, seed: int = 42) -> List[dict]:
    """Versão de compete que aceita Callables diretamente (externos ou internos)."""
    results = []
    rng_base = random.Random(seed)

    for i in range(rounds):
        actual_seed = rng_base.randint(0, 2**31 - 1)
        if start_player == 1:
            if i % 2 == 0:
                game = play_game(fn1, fn2, seed=actual_seed)
                game["J1"], game["J2"] = label1, label2
            else:
                game = play_game(fn2, fn1, seed=actual_seed)
                game["J1"], game["J2"] = label1, label2
                game["V"] = -game["V"]
        else:
            game = play_game(fn1, fn2, seed=actual_seed)
            game["J1"], game["J2"] = label1, label2
        results.append(game)
    return results


def summarize(results: List[dict]) -> dict:
    """Conta W/D/L por nome de estratégia usando score V."""
    stats = {}
    for g in results:
        v = g["V"]
        j1, j2 = g["J1"], g["J2"]
        stats.setdefault(j1, {"W": 0, "D": 0, "L": 0})
        stats.setdefault(j2, {"W": 0, "D": 0, "L": 0})
        if v == SCORE_DRAW:
            stats[j1]["D"] += 1
            stats[j2]["D"] += 1
        elif v == SCORE_X:
            stats[j1]["W"] += 1
            stats[j2]["L"] += 1
        else:
            stats[j1]["L"] += 1
            stats[j2]["W"] += 1
    return stats


def show_game_log(g: dict) -> None:
    """Mostra todas as jogadas de uma partida jogada por jogada."""
    log = g.get("log", [])
    if not log:
        print("Sem log detalhado.")
        return
    for idx, mv in enumerate(log):
        print(f"\n--- Jogada {idx + 1} ---")
        print(f"J1={mv['J1']} V={mv['V']} J2={mv['J2']} N={mv['N']}")
        board_t = tuple("." if c == " " else c for c in mv["board"])
        draw_board(board_t)


def save_json(results: List[dict], path: str) -> None:
    with open(path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


def save_txt(results: List[dict], path: str) -> None:
    lines = []
    lines.append("J1 | V(1=g1,-1=g2,0=draw) | J2 | N | board(0-8) | rounds")
    lines.append("-" * 60)
    for g in results:
        board_str = "".join("." if c == " " else c for c in g["board"])
        lines.append(f"{g['J1']} | {g['V']} | {g['J2']} | {g['N']} | {board_str} | {g['rounds']}")
    stats = summarize(results)
    lines.append("")
    lines.append("SUMÁRIO:")
    for name, s in stats.items():
        lines.append(f"  {name}: W={s['W']} D={s['D']} L={s['L']}")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


def run_matches() -> None:
    """Demonstração: naive vs bee, 100 jogos. Salva resultados."""
    results = compete("naive", "bee", rounds=100, start_player=1, seed=1234)
    save_json(results, "results_naive_bee.json")
    save_txt(results, "results_naive_bee.txt")
    print(f"Partidas: {len(results)}")
    for name, s in summarize(results).items():
        print(f"  {name}: W={s['W']} D={s['D']} L={s['L']}")


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] == "demo":
        run_matches()
        return

    if args[0] == "play":
        ref = args[1] if len(args) > 1 else "bee"
        if ref not in STRATEGIES:
            try:
                label, fn = resolve_strategy(ref)
            except (ValueError, ImportError, AttributeError) as e:
                print(f"Erro estratégia: {e}")
                return
        else:
            fn = STRATEGIES[ref]
        human_first = "--first" in args

        if human_first:
            play_with_view(human, fn, seed=0)
        else:
            play_with_view(fn, human, seed=0)
        return

    if args[0] == "view":
        path = args[1] if len(args) > 1 else "results_naive_bee.json"
        view_games(path)
        return

    if args[0] == "show":
        ref1 = args[1] if len(args) > 1 else "naive"
        ref2 = args[2] if len(args) > 2 else "bee"
        try:
            label1, fn1 = resolve_strategy(ref1)
            label2, fn2 = resolve_strategy(ref2)
        except (ValueError, ImportError, AttributeError) as e:
            print(f"Erro estratégia: {e}")
            return
        play_with_view(fn1, fn2, seed=0)
        return

    if args[0] == "vs":
        ref1 = args[1] if len(args) > 1 else "naive"
        ref2 = args[2] if len(args) > 2 else "bee"
        rounds = int(args[3]) if len(args) > 3 else 50
        fmt = args[4] if len(args) > 4 else "txt"
        try:
            label1, fn1 = resolve_strategy(ref1)
            label2, fn2 = resolve_strategy(ref2)
        except (ValueError, ImportError, AttributeError) as e:
            print(f"Erro estratégia: {e}")
            return
        results = compete_callable(fn1, fn2, label1, label2, rounds=rounds, start_player=1, seed=2025)
        out = f"results_{label1}_vs_{label2}.{fmt}"
        if fmt == "json":
            save_json(results, out)
        else:
            save_txt(results, out)
        print(f"Salvo: {out}")
        print(f"  {label1} ({ref1}) vs {label2} ({ref2})")
        for name, s in summarize(results).items():
            print(f"  {name}: W={s['W']} D={s['D']} L={s['L']}")
        return

    if args[0] == "register":
        name = args[1] if len(args) > 1 else None
        ref = args[2] if len(args) > 2 else None
        if not name or not ref:
            print("Uso: python main.py register NOME arq.py:funcao")
            print(f"Internas: {list(STRATEGIES)}")
            return
        try:
            load_external(ref)
        except (ValueError, ImportError, AttributeError) as e:
            print(f"Erro validando: {e}")
            return
        register_strategy(name, ref)
        print(f"Registrada '{name}' -> {ref} (salvo em {REGISTRY_FILE})")
        print(f"Usar: python main.py vs {name} bee 50")
        return

    if args[0] == "test":
        for names in [("naive", "bee"), ("bee", "naive")]:
            results = compete(names[0], names[1], rounds=30, start_player=1, seed=77)
            bee_loss = 0
            for g in results:
                if g["J1"] == "bee" and g["V"] == -1:  # bee J1(X), J2 venceu → bee perdeu
                    bee_loss += 1
                if g["J2"] == "bee" and g["V"] == 1:   # bee J2(O), J1 venceu → bee perdeu
                    bee_loss += 1
            print(f"{names[0]} vs {names[1]}: bee perdeu {bee_loss}/{len(results)}")
        print("PASS: bee não perde" if bee_loss == 0 else "FAIL: bee perdeu")
        return

    if args[0] == "compete":
        n1 = args[1] if len(args) > 1 else "naive"
        n2 = args[2] if len(args) > 2 else "bee"
        r = int(args[3]) if len(args) > 3 else 100
        fmt = args[4] if len(args) > 4 else "txt"
        results = compete(n1, n2, rounds=r, start_player=1, seed=2024)
        out = f"results_{n1}_vs_{n2}.{fmt}"
        if fmt == "json":
            save_json(results, out)
        else:
            save_txt(results, out)
        print(f"Salvo: {out}")
        for name, s in summarize(results).items():
            print(f"  {name}: W={s['W']} D={s['D']} L={s['L']}")
        return

    print("Uso:")
    print("  demo                          : naive vs bee, 100 jogos -> results_naive_bee.{json,txt}")
    print("  show REF1 REF2                : visualiza partida (REF = 'naive'/'bee'/'human' ou 'arq.py:fn')")
    print("  play REF [--first]            : humano vs REF; --first = humano X primeiro")
    print("  vs REF1 REF2 R fmt            : torneio externo/interno, R rounds, salva txt|json")
    print("  compete N1 N2 R fmt           : N1 vs N2 internos, R rounds")
    print("  register NOME ARQ:FN          : registra estratégia para uso futuro")
    print("  view <arquivo>                : navegador interativo de resultados (n/p/g/q)")
    print("  test                          : auto-check de integridade")
    print("  register NOME ARQ:FN          : registra estratégia externa no dicionário STRATEGIES")


if __name__ == "__main__":
    _load_registry()
    main()
