"""Gera relatórios progressivos para duas estratégias."""
import random
import sys
import time
from pathlib import Path

import main


MARCOS = range(100_000, 1_000_001, 100_000)


def executar(nome_x: str, nome_o: str, seed: int = 42) -> Path:
    fn_x = main.STRATEGIES[nome_x]
    fn_o = main.STRATEGIES[nome_o]
    rng = random.Random(seed)
    vitorias = derrotas = empates = 0
    linhas = []
    inicio = time.perf_counter()

    for rodada in range(1, max(MARCOS) + 1):
        resultado = main.play_game(fn_x, fn_o, rng.randrange(2**31), nome_x, nome_o)
        if resultado["winner"] == 1:
            vitorias += 1
        elif resultado["winner"] == -1:
            derrotas += 1
        else:
            empates += 1
        if rodada in MARCOS:
            linhas.append((rodada, vitorias, derrotas, empates, time.perf_counter() - inicio))

    destino = Path("experiments") / ("basic" if "fera_basica" in (nome_x, nome_o) else "minimax")
    destino.mkdir(parents=True, exist_ok=True)
    arquivo = destino / f"{nome_x}_vs_{nome_o}.md"
    tabela = "\n".join(
        f"| {rodada:,} | {vitorias:,} | {derrotas:,} | {empates:,} | {duracao:.2f}s |"
        for rodada, vitorias, derrotas, empates, duracao in linhas
    )
    arquivo.write_text(
        f"# Experimento: {nome_x} vs {nome_o}\n\n"
        "**Configuracao:**\n"
        f"- X: `{nome_x}`\n"
        f"- O: `{nome_o}`\n"
        f"- Semente: {seed}\n\n"
        "## Resultados progressivos\n\n"
        "| Rodadas | V (X) | D (X) | E | Tempo |\n"
        "|---------|-------|-------|---|-------|\n"
        f"{tabela}\n",
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
