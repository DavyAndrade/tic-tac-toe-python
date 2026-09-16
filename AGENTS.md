# TicTacToe Agent Notes

## Verify
- Run from repository root: `python -m unittest test_main -v`.
- Focus minimax blocking with `python -m unittest test_main.TestMinimax.test_minimax_bloqueio_critical`.
- `python main.py test` is only a 60-game smoke check; do not use it instead of unit tests.

## Architecture
- Implement board rules in `core/board.py` and strategies in `algorithms/`. Strategy contract: `fn(board, player, rng) -> Tab`; return a new immutable tuple.
- `main.py` contains compatibility copies, then rebinds public names from `core/` and `algorithms/`. Do not fix duplicated helpers in `main.py`; preserve its exported names for CLI and tests.
- Importing `main` imports `algorithms.learning`, which trains its Q policy for 10,000 episodes. Keep `main` imports out of lightweight tooling unless needed.
- External strategy registrations write cwd-relative ignored `strategies.json`; use `python main.py register NAME file.py:function`.

## Experiments
- `python run_torneio.py X_STRATEGY O_STRATEGY ROUNDS` stores every game in memory and writes ignored `results_*.txt`; use a small round count for checks. No arguments run four 100,000-game tournaments.
- `python run_progressivo.py X_STRATEGY O_STRATEGY` always runs 1,000,000 games in eight processes and overwrites tracked `experiments/basic/` or `experiments/minimax/` markdown. Run only for requested full experiments.
- Generated `results_*.txt` and `results_*.json` are ignored. Do not force-add them; GitHub rejects the full 1M JSON outputs for size.
- `fera_basica` is rules-only; do not restore a minimax fallback.
