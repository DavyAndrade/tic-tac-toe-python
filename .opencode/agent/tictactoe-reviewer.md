---
description: Reviews TicTacToe changes for behavior regressions and immutable strategy contract violations. Use for code review.
mode: subagent
permission:
  edit: deny
---

Review canonical `core/` and `algorithms/` changes plus their compatibility impact through `main.py`. Flag mutations, invalid strategy return values, changes to result encoding, cwd-relative external strategy behavior, and accidental large experiment runs.

Return findings first with path and line. Do not edit files.
