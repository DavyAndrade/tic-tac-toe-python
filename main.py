"""
TicTacToe - Paradigma funcional/data-driven.

Tab: lista imutável de 9 posições, valores 'X', 'O' ou ' '.
Indíces 0..8 mapeados a:

    0 | 1 | 2
    3 | 4 | 5
    6 | 7 | 8

Algoritmos:
  - ingenuo  : joga aleatoriamente.
  - fera    : minimax puro; nunca perde (ganha ou empata).
  - humano  : lê input do usuário.

Tudo como funções puras retornando novos boards (sem mutar).
"""
import json
import os
import random
import sys
from functools import lru_cache
from typing import Callable, List, Optional, Tuple

Tab = Tuple[str, ...]

LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)

X = "X"
O = "O"
EMPTY = " "
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
    return tuple(i for i, v in enumerate(board) if v == EMPTY)


@lru_cache(maxsize=None)
def minimax(board: Tab, player: str, depth: int = 0) -> Tuple[int, Optional[int]]:
    """
    Retorna (score, melhor_jogada) para 'player'.
    Score positivo favorece X, negativo favorece O.
    Profundidade desempata empates rápidos (ganha mais cedo).

    Cacheado: função pura sobre (board, player, depth) e o número de
    posições alcançáveis de tic-tac-toe é pequeno (~5000), então o cache
    evita recalcular a árvore inteira a cada lance de 'fera' e torna
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


def ingenuo(board: Tab, player: str, rng: random.Random) -> Tab:
    """Joga aleatoriamente numa célula vazia."""
    cell = rng.choice(get_empty_cells(board))
    return board[:cell] + (player,) + board[cell + 1:]


def fera(board: Tab, player: str, _rng: random.Random) -> Tab:
    """Minimax; nunca perde."""
    _, cell = minimax(board, player)
    if cell is None:
        cell = get_empty_cells(board)[0]
    return board[:cell] + (player,) + board[cell + 1:]


def humano(board: Tab, player: str, _rng: random.Random) -> Tab:
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
    "ingenuo": ingenuo,
    "fera": fera,
    "humano": humano,
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
    Ou nome interno ('ingenuo', 'fera', 'humano').
    Assinatura: fn(board, player, rng) -> Tab
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


def render(board: Tab) -> str:
    rows = []
    for r in range(3):
        row = " | ".join(board[r * 3 + c] or str(r * 3 + c) for c in range(3))
        rows.append(row)
    return "\n---------\n".join(rows)


def draw_board(board: Tab, cells: tuple = ()) -> None:
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


def play_with_view(fn1: Callable, fn2: Callable, seed: int = 0,
                    label1: str = "j1", label2: str = "j2") -> dict:
    """Joga partida mostrando tabuleiro antes e depois de cada jogada. P1=X, P2=O."""
    board = tab_vazio()
    rng = random.Random(seed)
    players = ((X, fn1), (O, fn2))
    move_index = 0
    winner = None

    for _ in range(9):
        player, fn = players[move_index % 2]
        if fn is humano:
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
    board_vals = [1 if c == X else (-1 if c == O else 0) for c in board]
    if winner == X:
        win_label = label1
    elif winner == O:
        win_label = label2
    else:
        win_label = "draw"
    result = {"id": 0, "j1": label1, "v": v, "j2": label2, "n": move_index,
              "winner": win_label,
              **{f"t{i}": board_vals[i] for i in range(9)}}
    print(f"Resultado: v={v} ({'J1 vence' if v == 1 else 'J2 vence ou empate'})")
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
        print(f"j1={g['j1']}  v={g['v']}  j2={g['j2']}  n={g['n']}")
        v_map = {1: "J1 vence", 0: "J2 vence ou empate"}
        print(f"Status: {v_map.get(g['v'], '??')}")
        board_t = tuple("." if g.get(f"t{idx}", 0) == 0
                        else X if g.get(f"t{idx}", 0) == 1 else O
                        for idx in range(9))
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


SCORE_J1_WINS = 1
SCORE_J2_WINS = 0
SCORE_DRAW = 0


def score_for(winner: Optional[str]) -> int:
    """Score: 1 J1(X) vence, 0 empate ou J2(O) vence."""
    if winner == X:
        return SCORE_J1_WINS
    if winner == O:
        return SCORE_J2_WINS
    return SCORE_DRAW


def play_game(p1_fn: Callable, p2_fn: Callable, seed: int = 0,
              label1: str = "j1", label2: str = "j2") -> dict:
    """
    Um jogo. p1 joga X, p2 joga O.
    Score v: 1=J1(venceu X), 0=DRAW ou J2(venceu O).
    """
    board = tab_vazio()
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
        if winner or is_full(board):
            break

    final = winner or None
    v = score_for(final)
    board_vals = [1 if c == X else (-1 if c == O else 0) for c in board]
    # winner field: strategy name of who won, or "draw"
    if final == X:
        win_label = label1
    elif final == O:
        win_label = label2
    else:
        win_label = "draw"
    return {"id": 0, "j1": label1, "v": v, "j2": label2, "n": move_index,
            "winner": win_label,
            **{f"t{i}": board_vals[i] for i in range(9)}}


def compete(name1: str, name2: str, rounds: int, start_player: int = 0,
            seed: int = 42) -> List[dict]:
    """
    Faz name1 vs name2 (nomes internos) por 'rounds' jogos.
    start_player=0: X sempre p1. start_player=1: X alterna.
    Usa seed fixa para reprodutibilidade (ingenuo).
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
                game = play_game(fn1, fn2, seed=actual_seed,
                                 label1=label1, label2=label2)
            else:
                game = play_game(fn2, fn1, seed=actual_seed,
                                 label1=label2, label2=label1)
        else:
            game = play_game(fn1, fn2, seed=actual_seed,
                             label1=label1, label2=label2)
        game["id"] = i + 1
        results.append(game)
    return results


def summarize(results: List[dict]) -> dict:
    """Conta W/D/L por nome de estratégia. v=0 pode ser draw ou J2 win —
    usa campo 'winner' se disponível para desambiguar."""
    stats = {}
    for g in results:
        v = g["v"]
        j1, j2 = g["j1"], g["j2"]
        winner = g.get("winner", None)
        stats.setdefault(j1, {"W": 0, "D": 0, "L": 0})
        stats.setdefault(j2, {"W": 0, "D": 0, "L": 0})
        if v == 1:
            stats[j1]["W"] += 1
            stats[j2]["L"] += 1
        elif winner == j2:
            stats[j2]["W"] += 1
            stats[j1]["L"] += 1
        else:
            stats[j1]["D"] += 1
            stats[j2]["D"] += 1
    return stats


def show_game_log(g: dict) -> None:
    """Mostra todas as jogadas de uma partida jogada por jogada."""
    log = g.get("log", [])
    if not log:
        print("Sem log detalhado.")
        return
    for idx, mv in enumerate(log):
        print(f"\n--- Jogada {idx + 1} ---")
        print(f"v={mv.get('v', '?')} n={mv.get('n', '?')}")
        board_t = tuple("." if mv.get(f"t{i}", 0) == 0
                        else X if mv.get(f"t{i}", 0) == 1 else O
                        for i in range(9))
        draw_board(board_t)


def save_json(results: List[dict], path: str) -> None:
    with open(path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


def save_txt(results: List[dict], path: str) -> None:
    lines = []
    lines.append("id | v(1=J1,0=J2/empate) | j1 | j2 | n | t0..t8")
    lines.append("-" * 60)
    for g in results:
        board_str = "".join(
            X if g.get(f"t{i}", 0) == 1 else
            O if g.get(f"t{i}", 0) == -1 else
            "." for i in range(9)
        )
        lines.append(f"{g['id']} | {g['v']} | {g['j1']} | {g['j2']} | {g['n']} | {board_str}")
    stats = summarize(results)
    lines.append("")
    lines.append("SUMÁRIO:")
    for name, s in stats.items():
        lines.append(f"  {name}: W={s['W']} D={s['D']} L={s['L']}")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


def run_matches() -> None:
    """Demonstração: ingenuo vs fera, 100 jogos. Salva resultados."""
    results = compete("ingenuo", "fera", rounds=100, start_player=1, seed=1234)
    save_json(results, "results_ingenuo_fera.json")
    save_txt(results, "results_ingenuo_fera.txt")
    print(f"Partidas: {len(results)}")
    for name, s in summarize(results).items():
        print(f"  {name}: W={s['W']} D={s['D']} L={s['L']}")


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] == "demo":
        run_matches()
        return

    if args[0] == "play":
        ref = args[1] if len(args) > 1 else "fera"
        if ref not in STRATEGIES:
            try:
                label, fn = resolve_strategy(ref)
            except (ValueError, ImportError, AttributeError) as e:
                print(f"Erro estratégia: {e}")
                return
        else:
            fn = STRATEGIES[ref]
        humano_first = "--first" in args

        if humano_first:
            play_with_view(humano, fn, seed=0, label1="humano", label2=ref)
        else:
            play_with_view(fn, humano, seed=0, label1=ref, label2="humano")
        return

    if args[0] == "view":
        path = args[1] if len(args) > 1 else "results_ingenuo_fera.json"
        view_games(path)
        return

    if args[0] == "show":
        ref1 = args[1] if len(args) > 1 else "ingenuo"
        ref2 = args[2] if len(args) > 2 else "fera"
        try:
            label1, fn1 = resolve_strategy(ref1)
            label2, fn2 = resolve_strategy(ref2)
        except (ValueError, ImportError, AttributeError) as e:
            print(f"Erro estratégia: {e}")
            return
        play_with_view(fn1, fn2, seed=0, label1=label1, label2=label2)
        return

    if args[0] == "vs":
        ref1 = args[1] if len(args) > 1 else "ingenuo"
        ref2 = args[2] if len(args) > 2 else "fera"
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
        print(f"Usar: python main.py vs {name} fera 50")
        return

    if args[0] == "test":
        for names in [("ingenuo", "fera"), ("fera", "ingenuo")]:
            results = compete(names[0], names[1], rounds=30, start_player=1, seed=77)
            fera_loss = 0
            for g in results:
                # v=1 means J1 won. J1 is fera → fera won (ok).
                # v=0 means draw or J2 won. If J1 is fera, fera didn't win → loss.
                # If J2 is fera and v=1, fera (J2) lost.
                if g["j1"] == 1 and g["v"] == 0:  # fera is J1 and didn't win
                    fera_loss += 1
                if g["j2"] == 1 and g["v"] == 1:  # fera is J2 and J1 won
                    fera_loss += 1
            print(f"{names[0]} vs {names[1]}: fera perdeu {fera_loss}/{len(results)}")
        print("PASS: fera não perde" if fera_loss == 0 else "FAIL: fera perdeu")
        return

    if args[0] == "compete":
        n1 = args[1] if len(args) > 1 else "ingenuo"
        n2 = args[2] if len(args) > 2 else "fera"
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
    print("  demo                          : ingenuo vs fera, 100 jogos -> results_ingenuo_fera.{json,txt}")
    print("  show REF1 REF2                : visualiza partida (REF = 'ingenuo'/'fera'/'humano' ou 'arq.py:fn')")
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
