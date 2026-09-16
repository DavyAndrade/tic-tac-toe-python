---
description: Runs and interprets TicTacToe tournament and strategy experiments. Use only when an experiment is explicitly requested.
mode: subagent
---

Run from repository root. Prefer `python run_torneio.py X_STRATEGY O_STRATEGY SMALL_ROUND_COUNT` for checks; no-argument tournament runs four 100k in-memory tournaments.

`python run_progressivo.py X_STRATEGY O_STRATEGY` always runs 1,000,000 games and overwrites a tracked report under `experiments/`; require explicit request before running it. Report command, seed, round count, output path, and X-versus-O interpretation.
