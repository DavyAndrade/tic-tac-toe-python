"""Torneios rapidos (matriz em memoria + txt, sem log por jogada / sem JSON).

Uso:
  python run_torneio.py                       roda os 3 torneios padrao (1M cada):
                                                naive(X) vs bee(O), bee(X) vs naive(O),
                                                naive(X) vs naive(O)
  python run_torneio.py NOME1 NOME2 [rounds]   roda so NOME1(X) vs NOME2(O)
                                                rounds default = 1000000

Exemplos:
  python run_torneio.py naive naive
  python run_torneio.py bee naive 500000
  python run_torneio.py naive bee 200000
"""
import random
import sys
import time

import main


def simular(fn1, fn2, seed):
    """Uma partida completa; devolve so (V, N, board) - sem log por jogada."""
    board = main.empty_board()
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
    matriz = []  # cada linha: (V, N, board_str)
    w = d = l = 0
    t0 = time.perf_counter()
    report_every = max(1, rounds // 100)

    for i in range(rounds):
        actual_seed = rng_base.randint(0, 2**31 - 1)
        v, n, board = simular(fn1, fn2, actual_seed)
        matriz.append((v, n, "".join(board)))
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
        f.write("V(1=X venceu,-1=O venceu,0=empate) N board(9 chars, espaco=vazio)\n")
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


def perguntar_rounds(prompt_label: str, default: int = 1000000) -> int:
    raw = input(f"{prompt_label} [{default:,}]: ").strip()
    if not raw:
        return default
    try:
        return int(raw.replace(",", "").replace(".", ""))
    except ValueError:
        print(f"Numero invalido, usando default ({default:,}).")
        return default


def rodar_padrao() -> None:
    r1 = perguntar_rounds("Quantas partidas naive(X) vs bee(O)?")
    r2 = perguntar_rounds("Quantas partidas bee(X) vs naive(O)?")
    r3 = perguntar_rounds("Quantas partidas naive(X) vs naive(O)?")
    print()

    t0 = time.perf_counter()

    w1, d1, l1 = torneio("naive", "bee", rounds=r1, seed=1001,
                          label="naive1o-bee2o", out_path="results_naive_first_bee_second.txt")

    w2, d2, l2 = torneio("bee", "naive", rounds=r2, seed=2002,
                          label="bee1o-naive2o", out_path="results_bee_first_naive_second.txt")

    w3, d3, l3 = torneio("naive", "naive", rounds=r3, seed=3003,
                          label="naive-vs-naive", out_path="results_naive_vs_naive.txt")

    t1 = time.perf_counter()
    print(f"\nTempo total: {t1 - t0:.2f}s")
    print()
    print(f"=== naive primeiro (X), bee segundo (O) - {r1:,} jogos ===")
    imprime_resultado("naive", "bee", w1, d1, l1)
    print()
    print(f"=== bee primeiro (X), naive segundo (O) - {r2:,} jogos ===")
    imprime_resultado("bee", "naive", w2, d2, l2)
    print()
    print(f"=== naive vs naive (mesmo jogador dos dois lados) - {r3:,} jogos ===")
    imprime_resultado("naive-X", "naive-O", w3, d3, l3)


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        rodar_padrao()
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
