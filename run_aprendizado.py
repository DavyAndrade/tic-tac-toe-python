"""Executa experimentos do aprendiz e gera progresso cumulativo em SVG."""
import argparse
import json
from pathlib import Path

import main
from algorithms import learning


DEFAULT_ROOT = Path("experiments/learning")


SCENARIOS = {
    "aprendiz_vs_ingenuo": (("aprendiz", "ingenuo", "direto", "ingenuo"),),
    "ingenuo_vs_aprendiz": (("ingenuo", "aprendiz", "direto", "ingenuo"),),
    "aprendiz_vs_fera_basica": (("aprendiz", "fera_basica", "direto", "fera_basica"),),
    "fera_basica_vs_aprendiz": (("fera_basica", "aprendiz", "direto", "fera_basica"),),
}


def consultar_partida(path, partida: int) -> dict:
    for row in carregar_progresso(path):
        if row.get("partida") == partida:
            return row
    raise KeyError(f"Partida {partida} não encontrada em {path}")


def carregar_progresso(path) -> list[dict]:
    rows = []
    with Path(path).open(encoding="utf-8") as file:
        for line in file:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _winner_label(winner: int) -> str:
    return "J1" if winner == 1 else "J2" if winner == -1 else "V"


def _progress_row(partida, phase, opponent, phase_match, counts, phase_counts, winner):
    return {
        "partida": partida,
        "fase": phase,
        "oponente": opponent,
        "fase_partida": phase_match,
        "J1": counts["J1"],
        "V": counts["V"],
        "J2": counts["J2"],
        "fase_J1": phase_counts["J1"],
        "fase_V": phase_counts["V"],
        "fase_J2": phase_counts["J2"],
        "vencedor": winner,
    }


def _write_jsonl(path, rows):
    with Path(path).open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")


def _rotulo(nome: str) -> str:
    return nome.replace("_", " ").capitalize()


def gerar_svg(progress_path, svg_path, title, j1_name=None, j2_name=None) -> Path:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    label_j1 = f"J1 ({_rotulo(j1_name)})" if j1_name else "J1"
    label_j2 = f"J2 ({_rotulo(j2_name)})" if j2_name else "J2"
    rows = carregar_progresso(progress_path)
    partidas = [row["partida"] for row in rows]
    max_match = max(partidas, default=0)
    tick_values = [0]
    if max_match:
        tick_step = max(1, (max_match + 9) // 10)
        tick_values = list(range(0, max_match + 1, tick_step))
        if tick_values[-1] != max_match:
            tick_values.append(max_match)

    svg_path = Path(svg_path)
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    with matplotlib.rc_context({"svg.fonttype": "none"}):
        figure, axis = plt.subplots(figsize=(9, 5), dpi=100)
        axis.plot(partidas, [row.get("J1", 0) for row in rows], color="#2563eb", label=label_j1)
        axis.plot(partidas, [row.get("V", 0) for row in rows], color="#6b7280", label="V")
        axis.plot(partidas, [row.get("J2", 0) for row in rows], color="#dc2626", label=label_j2)
        previous_phase = None
        for row in rows:
            phase = row.get("fase")
            if previous_phase is not None and phase != previous_phase:
                axis.axvline(row["partida"], color="#777", linestyle="--", linewidth=0.8)
            previous_phase = phase
        axis.set_title(title)
        axis.set_xlabel("Partida")
        axis.set_ylabel("Contagem cumulativa")
        axis.set_xlim(0, max_match or 1)
        axis.set_xticks(tick_values)
        axis.set_ylim(bottom=0)
        axis.grid(axis="y", alpha=0.2)
        axis.legend()
        figure.tight_layout()
        figure.savefig(svg_path, format="svg")
        plt.close(figure)
    return svg_path


def executar_experimento(name, phases, rounds_per_phase=100, root=DEFAULT_ROOT, seed=42, variant=None):
    suffix = f"_{variant}" if variant else ""
    output = Path(root) / f"rodadas_{rounds_per_phase}{suffix}" / name
    output.mkdir(parents=True, exist_ok=True)
    episodes_path = output / "episodes.jsonl"
    progress_path = output / "progress.jsonl"
    q_path = output / "q_table.json"
    episodes_path.write_text("", encoding="utf-8")

    learning.resetar_aprendizado()
    learning.configurar_persistencia(episodes_path, q_path)
    counts = {"J1": 0, "V": 0, "J2": 0}
    rows = []
    first_opponent = phases[0][3]
    initial_phase = "direto" if len(phases) == 1 else phases[0][2]
    rows.append(_progress_row(0, initial_phase, first_opponent, 0, counts, counts, None))
    partida = 0

    try:
        for j1_name, j2_name, phase, opponent in phases:
            learning.configurar_contexto(name, phase, opponent)
            phase_counts = {"J1": 0, "V": 0, "J2": 0}
            for phase_match in range(1, rounds_per_phase + 1):
                partida += 1
                game = main.play_game(
                    main.STRATEGIES[j1_name],
                    main.STRATEGIES[j2_name],
                    seed=seed + partida - 1,
                    label1=j1_name,
                    label2=j2_name,
                )
                winner = _winner_label(game["winner"])
                counts[winner] += 1
                phase_counts[winner] += 1
                rows.append(
                    _progress_row(
                        partida,
                        "direto" if len(phases) == 1 else phase,
                        opponent,
                        phase_match,
                        counts,
                        phase_counts,
                        winner,
                    )
                )
    finally:
        learning.salvar_q(q_path)
        learning.configurar_persistencia(None)
        learning.configurar_contexto()

    _write_jsonl(progress_path, rows)
    svg_path = output / "progress.svg"
    first_j1, first_j2 = phases[0][0], phases[0][1]
    title = f"J1 ({_rotulo(first_j1)}) vs J2 ({_rotulo(first_j2)})"
    gerar_svg(progress_path, svg_path, title, first_j1, first_j2)
    return {
        "directory": output,
        "episodes": episodes_path,
        "progress": progress_path,
        "q_table": q_path,
        "svg": svg_path,
    }


def executar_matriz(rounds_per_phase=100, root=DEFAULT_ROOT, seed=42, variant=None):
    return {
        name: executar_experimento(name, phases, rounds_per_phase, root, seed, variant)
        for name, phases in SCENARIOS.items()
    }


def main_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rounds", type=int, default=100)
    parser.add_argument("--root", default=str(DEFAULT_ROOT))
    parser.add_argument("--variant", help="sufixo do diretorio, ex.: eps0 -> rodadas_<N>_eps0")
    parser.add_argument("--scenario", choices=("all", *SCENARIOS), default="all")
    parser.add_argument("--progress")
    parser.add_argument("--partida", type=int)
    args = parser.parse_args()

    if args.progress:
        if args.partida is None:
            parser.error("--partida é obrigatório com --progress")
        print(json.dumps(consultar_partida(args.progress, args.partida), ensure_ascii=False))
        return

    if args.scenario == "all":
        executar_matriz(args.rounds, args.root, variant=args.variant)
    else:
        executar_experimento(
            args.scenario, SCENARIOS[args.scenario], args.rounds, args.root,
            variant=args.variant,
        )


if __name__ == "__main__":
    main_cli()
