"""Gera relatório de 1M de partidas sem salvar resultados individuais."""
import random
import sys
import time
from pathlib import Path

import main


RODADAS = 1_000_000


def simular(fn_x, fn_o, seed: int):
    board = main.tab_vazio()
    rng = random.Random(seed)
    for rodada in range(9):
        player, strategy = ((main.X, fn_x), (main.O, fn_o))[rodada % 2]
        board = strategy(board, player, rng)
        winner = main.get_winner(board)
        if winner or main.is_full(board):
            return winner
    return None


def executar(nome_x: str, nome_o: str, seed: int = 42) -> Path:
    fn_x = main.STRATEGIES[nome_x]
    fn_o = main.STRATEGIES[nome_o]
    rng = random.Random(seed)
    vitorias = derrotas = empates = 0
    inicio = time.perf_counter()

    for _ in range(RODADAS):
        winner = simular(fn_x, fn_o, rng.randrange(2**31))
        if winner == main.X:
            vitorias += 1
        elif winner == main.O:
            derrotas += 1
        else:
            empates += 1

    destino = Path("experiments") / ("basic" if "fera_basica" in (nome_x, nome_o) else "minimax")
    destino.mkdir(parents=True, exist_ok=True)
    arquivo = destino / f"{nome_x}_vs_{nome_o}.md"
    duracao = time.perf_counter() - inicio
    arquivo.write_text(
        f"# Experimento: {nome_x} vs {nome_o}\n\n"
        "**Configuracao:**\n"
        f"- X: `{nome_x}`\n"
        f"- O: `{nome_o}`\n"
        f"- Semente: {seed}\n"
        f"- Rodadas: {RODADAS:,}\n"
        f"- Tempo: {duracao:.2f}s\n\n"
        "## Resultado\n\n"
        "| Jogador | Estrategia | Venceu | Perdeu | Empatou |\n"
        "|---------|------------|--------|---------|---------|\n"
        f"| X | `{nome_x}` | {vitorias:,} | {derrotas:,} | {empates:,} |\n"
        f"| O | `{nome_o}` | {derrotas:,} | {vitorias:,} | {empates:,} |\n",
        encoding="utf-8",
    )
    return arquivo


def main_cli() -> None:
    nomes = sys.argv[1:] or ["ingenuo", "fera_basica"]
    if len(nomes) != 2:
        raise SystemExit("Uso: python run_progressivo.py ESTRATEGIA_X ESTRATEGIA_O")
    print(executar(*nomes))


if __name__ == "__main__":
    main_cli()
