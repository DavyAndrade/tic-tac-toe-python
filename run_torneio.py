"""Torneios rapidos (matriz em memoria + txt, sem log por jogada / sem JSON).

Uso:
  python run_torneio.py                       roda os 3 torneios padrao (1M cada):
                                                ingenuo(X) vs fera(O), fera(X) vs ingenuo(O),
                                                ingenuo(X) vs ingenuo(O)
  python run_torneio.py NOME1 NOME2 [rounds]   roda so NOME1(X) vs NOME2(O)
                                                rounds default = 1000000

Exemplos:
  python run_torneio.py ingenuo ingenuo
  python run_torneio.py fera ingenuo 500000
  python run_torneio.py ingenuo fera 200000
"""
import random
import sys
import time

import main


def simular(fn1, fn2, seed):
    """Uma partida completa; devolve so (v, n, board) - sem log por jogada."""
    board = main.tab_vazio()
    rng = random.Random(seed)
    players = ((main.X, fn1), (main.O, fn2))
    move_index = 0
    winner = None
    for _ in range(9):
        player, fn = players[move_index % 2]
        board = fn(board, player, rng)
        winner = main.get_winner(board)
        move_index += 1
        if winner or main.is_full(board):
            break
    return main.score_for(winner), move_index, board


def torneio(name1: str, name2: str, rounds: int, seed: int, label: str, out_path: str):
    """NOME1 joga X (primeiro), NOME2 joga O (segundo). W/D/L sao do ponto de vista de X."""
    fn1 = main.STRATEGIES[name1]
    fn2 = main.STRATEGIES[name2]
    rng_base = random.Random(seed)
    matriz = []  # cada linha: (v, n, board_str)
    w = d = l = 0
    t0 = time.perf_counter()
    report_every = max(1, rounds // 100)

    for i in range(rounds):
        actual_seed = rng_base.randint(0, 2**31 - 1)
        v, n, board = simular(fn1, fn2, actual_seed)
        board_vals = "".join(
            "X" if c == main.X else ("O" if c == main.O else ".") for c in board
        )
        matriz.append((v, n, board_vals))
        if v == 1:
            w += 1
        elif v == -1:
            l += 1
        else:
            d += 1

        done = i + 1
        if done % report_every == 0 or done == rounds:
            elapsed = time.perf_counter() - t0
            pct = done / rounds * 100
            rate = done / elapsed if elapsed > 0 else 0
            eta = (rounds - done) / rate if rate > 0 else 0
            print(f"\r[{label}] {done:,}/{rounds:,} ({pct:5.1f}%) "
                  f"- {rate:,.0f} jogos/s - ETA {eta:5.1f}s   ", end="", flush=True)
    print()

    linhas = [f"{v} {n} {board}" for v, n, board in matriz]
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"{name1} (X) vs {name2} (O) - {rounds} jogos\n")
        f.write("v(1=X venceu,-1=O venceu,0=empate) n board(9 chars, X/O/.)\n")
        f.write("-" * 40 + "\n")
        f.write("\n".join(linhas) + "\n")
        f.write(f"\nSUMARIO: {name1}(X) W={w} D={d} L={l} | {name2}(O) W={l} D={d} L={w}\n")

    return w, d, l


def imprime_resultado(nome_x: str, nome_o: str, w: int, d: int, l: int) -> None:
    print(f"  {nome_x} (X): W={w} D={d} L={l}")
    print(f"  {nome_o} (O): W={l} D={d} L={w}")


def rodar_um(name1: str, name2: str, rounds: int) -> None:
    out_path = f"results_{name1}_vs_{name2}.txt"
    label = f"{name1}-vs-{name2}"
    t0 = time.perf_counter()
    w, d, l = torneio(name1, name2, rounds=rounds, seed=42, label=label, out_path=out_path)
    t1 = time.perf_counter()
    print(f"\nTempo total: {t1 - t0:.2f}s | salvo em {out_path}")
    print()
    print(f"=== {name1} (X) vs {name2} (O) - {rounds:,} jogos ===")
    imprime_resultado(name1, name2, w, d, l)


def rodar_experimentos() -> None:
    """Roda os 4 experimentos: ingenuo/fera em todas as combinacoes."""
    combos = [
        ("ingenuo", "ingenuo"),
        ("ingenuo", "fera"),
        ("fera", "ingenuo"),
        ("fera", "fera"),
    ]
    rounds = 100000
    t0 = time.perf_counter()
    resultados = {}
    for n1, n2 in combos:
        out_path = f"results_{n1}_vs_{n2}.txt"
        label = f"{n1}-vs-{n2}"
        w, d, l = torneio(n1, n2, rounds=rounds, seed=42, label=label, out_path=out_path)
        resultados[(n1, n2)] = (w, d, l)
        print(f"  {n1} (X): W={w} D={d} L={l}")
        print(f"  {n2} (O): W={l} D={d} L={w}")
        print()
    t1 = time.perf_counter()
    print(f"Tempo total: {t1 - t0:.2f}s")
    return resultados


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        rodar_experimentos()
    elif len(args) == 1:
        print(f"Uso: python run_torneio.py NOME1 NOME2 [rounds]")
        print(f"Estrategias disponiveis: {list(main.STRATEGIES)}")
    else:
        n1, n2 = args[0], args[1]
        if n1 not in main.STRATEGIES or n2 not in main.STRATEGIES:
            print(f"Estrategia invalida. Disponiveis: {list(main.STRATEGIES)}")
        else:
            r = int(args[2]) if len(args) > 2 else 1000000
            rodar_um(n1, n2, r)
