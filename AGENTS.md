# TicTacToe Agent Notes

## Verify
- No package manager, linter, formatter, or typechecker is configured; run from repository root: `python -m unittest test_main -v`.
- Focus one test with `python -m unittest test_main.TestMinimax.test_minimax_bloqueio_critical`.
- `python main.py test` is a lightweight behavioral smoke check, not replacement for unit tests.

## Structure
- `core/board.py` owns immutable board primitives. `algorithms/` houses strategies; each must implement `fn(board, player, rng) -> Tab` and return a new tuple.
- `main.py` provides the CLI. Strategy imports are reassigned at lines 131‑134; edit `core/` or `algorithms/`, preserving `main` exports used by tests and CLI.
- Importing `main` triggers Q‑learning policy training (`algorithms/learning.py` calls `treinar()` on import). Keep imports intentional in test/benchmark paths.

## Runs And Output
- Run commands from repo root. `strategies.json` is cwd‑relative and ignored by Git.
- `python run_torneio.py` executes four 100 k tournaments, stores all games in memory, and writes ignored `results_*.txt`. Use explicit names or a smaller round count for quick checks.
- `python run_progressivo.py X_STRATEGY O_STRATEGY` runs exactly 1 000 000 games, overwriting the markdown report at `experiments/basic/X_vs_O.md`. Use this for full‑scale benchmarking only.

## Experiment Guidance
- `fer a_basica` now blocks all naïve wins: runs of 1 M games show `ingenuo` wins 0, loses ≈ 882 k, draws ≈ 117 k.
- When updating or adding strategies, ensure they follow the same `fn(board, player, rng) -> Tab` signature.
- Do not rely on the fallback minimax in `fera_basica`; it has been removed.
- To regenerate experiment tables, rerun `run_progressivo.py` with the desired strategies; the markdown files will be rewritten with updated counts and timings.

## Misc
- `strategies.json` is excluded from version control; keep it in the repo root if custom external strategies are needed.
- The repository has no CI configuration; manual testing is performed via the commands above.
