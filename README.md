# TicTacToe - Paradigma Funcional/Data-Driven

Implementação em estilo funcional: funções puras recebem um **board imutável** e
retornam um **novo board**. Board é tupla imutável de 9 posições (índices `0..8`):

```
 0 | 1 | 2
 3 | 4 | 5
 6 | 7 | 8
```

Valores: `'X'`, `'O'` ou `' '`.

## Algoritmos

| nome    | função | estratégia |
|---------|--------|------------|
| `naive`  | `naive()`  | escolhe jogada aleatória entre células vazias |
| `bee`    | `bee()`    | algoritmo **minimax** puro — nunca perde (ganha ou empata) |
| `human`  | `human()`  | lê coordenada `0-8` do input |

### Bee (minimax)

Busca exaustiva do espaço de jogadas. Avalia terminal:

- vitória de **X** → score `10 - depth` (ganha mais cedo vale mais)
- vitória de **O** → score `depth - 10`
- empate → `0`

X (máximo) e O (mínimo) alternam. Resultado garantido: **bee nunca perde**.

## API (funções puras)

```python
empty_board() -> Board                    # nova tupla vazia
get_winner(board) -> 'X' | 'O' | None     # vencedor ou None
is_full(board) -> bool
get_empty_cells(board) -> tuple[int,..]
minimax(board, player, depth=0) -> (score, cell)
naive(board, player, rng) -> Board        # jogada aleatória
bee(board, player, _rng) -> Board         # minimax
human(board, player, _rng) -> Board       # input
play_game(p1_fn, p2_fn, seed=0) -> dict   # partida única
compete(name1, name2, rounds, start_player=0) -> list[dict]
```

## Formato de resultado (JSON / TXT)

Cada partida produz:

```json
{
  "J1": "naive",          // nome estratégia jogador 1 (joga X)
  "V": 1,                 // 1=J1 vence, -1=J2 vence, 0=empate
  "J2": "bee",            // nome estratégia jogador 2 (joga O)
  "N": 5,                 // número de jogadas até fim
  "board": [...9 posições],
  "rounds": 5
}
```

`V` (vitória/score):
- `1`  → **J1** venceu
- `-1` → **J2** venceu
- `0`  → empate

Arquivo `.txt` inclui tabela jogada por jogada + sumário `W/D/L` por estratégia.

## Uso

```bash
# Demo: naive vs bee, 100 partidas, salva results_naive_bee.{json,txt}
python main.py demo

# Visualiza partida jogada por jogada (tabuleiro desenhado)
python main.py show naive bee       # bee vence visualmente
python main.py show bee naive

# Humano vs algoritmo (mostra tabuleiro a cada jogada)
python main.py play bee --first    # humano joga X (primeiro)
python main.py play naive          # humano joga O (segundo)
# durante play: tabuleiro desenhado antes de sua jogada, digite 0-8

# Competição: N1 vs N2, R rounds, formato txt|json
python main.py compete naive bee 100 json
python main.py compete bee naive 50 txt

# Navegador interativo de resultados (n=next p=prev g=log <num> q=quit)
python main.py view results_naive_bee.json

# Auto-teste: bee não deve perder em nenhuma partida
python main.py test

# Help
python main.py
```

## Resultados (demo padrão)

```
Partidas: 100
  naive: W=0 D=8 L=92
  bee:   W=92 D=8 L=0
```

Bee: **nunca perde**. Naive: 0 vitórias (bee sempre empata ou vence).

## Arquivos

| arquivo | descrição |
|---------|-----------|
| `main.py` | implementação (funcional, imutável) |
| `test_main.py` | testes unitários (`python -m pytest test_main.py`) |
| `results_naive_bee.json` | partidas individuais (100 jogos demo) |
| `results_naive_bee.txt` | partidas + sumário |
| `results_naive_vs_bee.json`/`.txt` | gerado por `compete` |
| `README.md` | este documento |

## Testes

```bash
python -m pytest test_main.py -v    # ou
python main.py test                   # auto-check integrado
```
