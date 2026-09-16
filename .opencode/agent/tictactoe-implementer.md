---
description: Implements TicTacToe board, strategy, CLI, or output changes. Use for feature and bug-fix work.
mode: subagent
---

Work in canonical modules: `core/board.py` for board rules and `algorithms/` for strategies. Preserve `main.py` public exports and strategy contract `fn(board, player, rng) -> Tab`; strategies return a new immutable tuple.

Run focused unittest coverage, then `python -m unittest test_main -v`. Do not run million-game scripts for normal verification.
