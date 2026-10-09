# TicTacToe Agent Notes

## Verify
- Prepare graph dependency when `.venv` is absent: `uv venv .venv && uv pip install --python .venv/bin/python -r requirements.txt`.
- Run from repository root: `.venv/bin/python -m unittest test_main -v`.
- Focus minimax blocking with `.venv/bin/python -m unittest test_main.TestMinimax.test_minimax_bloqueio_critical`.
- `python main.py test` is only a 60-game smoke check; do not use it instead of unit tests.

## Architecture
- Implement board rules in `core/board.py` and strategies in `algorithms/`. Strategy contract: `fn(board, player, rng) -> Tab`; return a new immutable tuple.
- `main.py` contains compatibility copies, then rebinds public names from `core/` and `algorithms/`. Do not fix duplicated helpers in `main.py`; preserve its exported names for CLI and tests.
- Importing `main` imports `algorithms.learning`, which trains its Q policy for 10,000 episodes. Keep `main` imports out of lightweight tooling unless needed.
- External strategy registrations write cwd-relative ignored `strategies.json`; use `python main.py register NAME file.py:function`.

## Experiments
- **All learning-agent experiments run with epsilon 0** (frozen default since the 1M runs; `_EPSILON_APRENDIZ = 0.0`, guarded by `test_epsilon_zero_por_decisao`). Exploration comes only from the random tie-break on unvisited states (EC-003), EXCEPT in `treino_*` scenarios which run a per-phase schedule via `configurar_epsilon` (0.25 in `exploracao`, then 0.0 in `neutralizacao`). Datasets made before this rule carry `epsilon: 0.1` in their `q_table.json` and are historical baselines.
- **Reward weights are +10 win / +1 draw / −3 loss** (`_RECOMPENSAS_APRENDIZ`; history: +2/+1/−5 baseline → +3/+1/−1 (`eps0_pes311`) → +4/+2/−4 (`eps0_pes424`) → +2/+1/−5 (`eps0_pes215` rerun, winner of the comparison) → +10/+1/−1 (`eps0_pes1011`, lost) → +10/+1/−3 (`eps0_pes1013`, tree-stickiness variant: heavy win, softened loss; guarded by the `test_aprendiz_aplica_*` tests). Each config dir carries its own weights in its `q_table.json`.
- **Preserve experiment data always.** Never overwrite `experiments/` outputs (learning datasets, reports, `basic/` and `minimax/` markdown). Learning experiments are organized by configuration: `experiments/learning/<epsilon>_<pesos>/rodadas_<N>/<experimento>/` (e.g. `eps0_pes215/rodadas_1000/aprendiz_vs_ingenuo/aprendiz_vs_ingenuo.md`, `eps0-1_pes215/` = historical ε=0.1, `eps0_pes311/` = rewards +3/+1/−1). The report markdown lives INSIDE its experiment directory as `<name>.md`. Run new experiments with `--root experiments/learning/<config>` (or ad-hoc `--variant NAME`); never rerun into an existing directory unless reproducing the identical config.
- `python run_aprendizado.py --rounds N [--scenario NAME] [--variant NAME]` runs aprendiz experiments; `--progress <jsonl> --partida N` queries a match without rerunning.
- `python run_torneio.py X_STRATEGY O_STRATEGY ROUNDS` stores every game in memory and writes ignored `results_*.txt`; use a small round count for checks. No arguments run four 100,000-game tournaments.
- `python run_progressivo.py X_STRATEGY O_STRATEGY` always runs 1,000,000 games in eight processes and overwrites tracked `experiments/basic/` or `experiments/minimax/` markdown. Run only for requested full experiments.
- Generated `results_*.txt` and `results_*.json` are ignored. Do not force-add them; GitHub rejects the full 1M JSON outputs for size.
- `fera_basica` is rules-only; do not restore a minimax fallback.
