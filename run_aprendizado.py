"""Executa experimentos do aprendiz e gera progresso cumulativo em SVG."""
import argparse
import html
import json
from pathlib import Path

import main
from algorithms import learning


DEFAULT_ROOT = Path("experiments/learning")


SCENARIOS = {
    "aprendiz_vs_ingenuo": (("aprendiz", "ingenuo", "direto", "ingenuo"),),
    "ingenuo_vs_aprendiz": (("ingenuo", "aprendiz", "direto", "ingenuo"),),
    "aprendiz_ingenuo_para_fera": (
        ("aprendiz", "ingenuo", "ingenuo", "ingenuo"),
        ("aprendiz", "fera", "fera", "fera"),
    ),
    "aprendiz_fera_para_ingenuo": (
        ("aprendiz", "fera", "fera", "fera"),
        ("aprendiz", "ingenuo", "ingenuo", "ingenuo"),
    ),
    "ingenuo_aprendiz_para_fera": (
        ("ingenuo", "aprendiz", "ingenuo", "ingenuo"),
        ("fera", "aprendiz", "fera", "fera"),
    ),
    "fera_aprendiz_para_ingenuo": (
        ("fera", "aprendiz", "fera", "fera"),
        ("ingenuo", "aprendiz", "ingenuo", "ingenuo"),
    ),
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


def gerar_svg(progress_path, svg_path, title) -> Path:
    rows = carregar_progresso(progress_path)
    width, height = 900, 500
    left, top, right, bottom = 70, 45, 25, 60
    chart_width = width - left - right
    chart_height = height - top - bottom
    max_match = max((row["partida"] for row in rows), default=1) or 1
    max_count = max(
        (max(row.get("J1", 0), row.get("V", 0), row.get("J2", 0)) for row in rows),
        default=1,
    ) or 1

    def point(row, key):
        x = left + row["partida"] / max_match * chart_width
        y = top + chart_height - row.get(key, 0) / max_count * chart_height
        return f"{x:.2f},{y:.2f}"

    def polyline(key, color):
        points = " ".join(point(row, key) for row in rows)
        return f'<polyline fill="none" stroke="{color}" stroke-width="2" points="{points}" />'

    transitions = []
    previous_phase = None
    for row in rows:
        phase = row.get("fase")
        if previous_phase is not None and phase != previous_phase:
            x = left + row["partida"] / max_match * chart_width
            transitions.append(
                f'<line x1="{x:.2f}" y1="{top}" x2="{x:.2f}" '
                f'y2="{top + chart_height}" stroke="#777" stroke-dasharray="5,5" />'
            )
        previous_phase = phase

    content = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        f'<title>{html.escape(title)}</title>',
        f'<rect width="100%" height="100%" fill="white" />',
        f'<text x="{left}" y="25" font-size="18">{html.escape(title)}</text>',
        f'<line x1="{left}" y1="{top + chart_height}" x2="{width - right}" '
        f'y2="{top + chart_height}" stroke="#333" />',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + chart_height}" stroke="#333" />',
        *transitions,
        polyline("J1", "#2563eb"),
        polyline("V", "#6b7280"),
        polyline("J2", "#dc2626"),
        f'<text x="{left}" y="{height - 20}" font-size="12">Partida</text>',
        f'<text x="{width - 135}" y="{height - 20}" fill="#2563eb">J1</text>',
        f'<text x="{width - 105}" y="{height - 20}" fill="#6b7280">V</text>',
        f'<text x="{width - 75}" y="{height - 20}" fill="#dc2626">J2</text>',
        "</svg>",
    ]
    svg_path = Path(svg_path)
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.write_text("\n".join(content), encoding="utf-8")
    return svg_path


def executar_experimento(name, phases, rounds_per_phase=100, root=DEFAULT_ROOT, seed=42):
    output = Path(root) / name
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
    gerar_svg(progress_path, svg_path, name.replace("_", " "))
    return {
        "directory": output,
        "episodes": episodes_path,
        "progress": progress_path,
        "q_table": q_path,
        "svg": svg_path,
    }


def executar_matriz(rounds_per_phase=100, root=DEFAULT_ROOT, seed=42):
    return {
        name: executar_experimento(name, phases, rounds_per_phase, root, seed)
        for name, phases in SCENARIOS.items()
    }


def main_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rounds", type=int, default=100)
    parser.add_argument("--root", default=str(DEFAULT_ROOT))
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
        executar_matriz(args.rounds, args.root)
    else:
        executar_experimento(args.scenario, SCENARIOS[args.scenario], args.rounds, args.root)


if __name__ == "__main__":
    main_cli()
