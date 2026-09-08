# TicTacToe — Paradigma Funcional/Data-Driven

Jogo da Velha em Python com paradigma funcional: funcoes puras, tabuleiros imutaveis, sem estado compartilhado.

## Tabuleiro

Tupla imutavel de 9 posicoes (indices `0..8`):

```
 0 | 1 | 2
 3 | 4 | 5
 6 | 7 | 8
```

Valores: `'X'` (Jogador 1), `'O'` (Jogador 2) ou `' '` (vazio).

## Algoritmos

| nome | funcao | estrategia |
|------|--------|------------|
| `ingenuo` | `ingenuo()` | jogada aleatoria entre celulas vazias |
| `fera` | `fera()` | minimax puro — **nunca perde** (ganha ou empata) |
| `humano` | `humano()` | le coordenada `0-8` do input |

### Fera (minimax)

Busca exaustiva do espaco de jogadas (~5000 nos unicos, com `lru_cache`).

| Terminal | Score |
|----------|-------|
| vitoria X | `10 - depth` (ganha mais cedo vale mais) |
| vitoria O | `depth - 10` |
| empate | `0` |

X (maximo) e O (minimo) alternam. **Resultado garantido: fera nunca perde.**

## API

```python
# Tabuleiro
tab_vazio() -> Tab                          # tupla vazia de 9 espacos
get_winner(board) -> 'X' | 'O' | None       # vencedor ou None
is_full(board) -> bool                      # True se sem espacos vazios
get_empty_cells(board) -> tuple[int, ...]   # indices das celulas vazias

# Algoritmos
ingenuo(board, player, rng) -> Tab          # jogada aleatoria
fera(board, player, _rng) -> Tab            # minimax (ignora rng)
humano(board, player, _rng) -> Tab          # input do usuario

# Minimax (usado internamente pelo fera)
minimax(board, player, depth=0) -> (score, cell)

# Partida
play_game(p1_fn, p2_fn, seed=0) -> dict     # partida unica
compete(name1, name2, rounds) -> list[dict]  # torneio

# Utilitarios
render(board) -> str                         # tabuleiro como string
draw_board(board) -> None                    # imprime tabuleiro visual
score_for(winner) -> int                     # 1=X, 0=O/empate
summarize(results) -> dict                   # W/D/L por estrategia
save_json(results, path) -> None             # salva JSON
save_txt(results, path) -> None              # salva TXT
```

## Formato de resultado

Cada partida retorna:

```json
{
  "id": 1,
  "j1": 1,
  "v": 0,
  "j2": 0,
  "winner": 1,
  "n": 5,
  "j1_name": "ingenuo",
  "j2_name": "fera",
  "t0": 1, "t1": 1, "t2": 1,
  "t3": 0, "t4": 0, "t5": 0,
  "t6": 0, "t7": 0, "t8": 0
}
```

| campo | tipo | descricao |
|-------|------|-----------|
| `id` | int | ID sequencial |
| `j1` | 0/1 | `1` se J1 venceu |
| `v` | 0/1 | `1` se empate/velha |
| `j2` | 0/1 | `1` se J2 venceu |
| `winner` | -1/0/1 | `1`=J1, `-1`=J2, `0`=empate |
| `n` | int | numero de jogadas |
| `j1_name` | str | estrategia do J1 |
| `j2_name` | str | estrategia do J2 |
| `t0`-`t8` | -1/0/1 | `1`=marca J1, `0`=vazio, `-1`=marca J2 |

**Exemplos:**

| Resultado | j1 | v | j2 | winner |
|-----------|----|---|----|----|
| J1 vence | 1 | 0 | 0 | 1 |
| J2 vence | 0 | 0 | 1 | -1 |
| Empate | 0 | 1 | 0 | 0 |

## Uso

```bash
# Demo: ingenuo vs fera, 100 partidas
python main.py demo

# Visualizar partida jogada por jogada
python main.py show ingenuo fera
python main.py show fera ingenuo

# Humano vs algoritmo
python main.py play fera --first   # humano joga X (primeiro)
python main.py play fera           # humano joga O (segundo)
python main.py play ingenuo        # humano vs ingenuo

# Competicao entre algoritmos
python main.py compete ingenuo fera 100 json   # 100 partidas, salva JSON
python main.py compete fera ingenuo 50 txt     # 50 partidas, salva TXT

# Navegador interativo de resultados
python main.py view results_ingenuo_fera.json
# n(ext) | p(rev) | g(o) | <num> | q(uit)

# Auto-teste: fera nao deve perder
python main.py test

# Torneios rapidos (100k rodadas)
python run_torneio.py
python run_torneio.py fera ingenuo 500000

# Gerar experimentos progressivos (100k → 1M)
python gen_progressivo.py
python gen_progressivo.py ingenuo fera
```

## Experimentos

Resultados progressivos de 100k a 1M rodadas, sem alternancia de ordem.

| combinacao | vence | empata | perde | link |
|------------|-------|--------|-------|------|
| ingenuo vs ingenuo | 43.7% | 12.7% | 43.7% | [detalhes](experimento_ingenuo_vs_ingenuo.md) |
| ingenuo vs fera | **0%** | 19.3% | **80.7%** | [detalhes](experimento_ingenuo_vs_fera.md) |
| fera vs ingenuo | **99.5%** | 0.5% | **0%** | [detalhes](experimento_fera_vs_ingenuo.md) |
| fera vs fera | 0% | 100% | 0% | [detalhes](experimento_fera_vs_fera.md) |

### Algoritmo externo

Qualquer funcao com assinatura `fn(board, player, rng) -> Tab`:

```bash
# Formato: label:arquivo.py:funcao
python gen_progressivo.py "avarento:outro_aluno.py:avarento" fera
python main.py play "avarento:outro_aluno.py:avarento"
```

Veja `outro_aluno.py` como exemplo.

## Arquivos

| arquivo | descricao |
|---------|-----------|
| `main.py` | implementacao principal |
| `run_torneio.py` | torneios rapidos em massa |
| `gen_progressivo.py` | gerador de experimentos progressivos |
| `test_main.py` | testes unitarios (21 testes) |
| `outro_aluno.py` | estrategia externa de exemplo |
| `experimento_*.md` | resultados dos experimentos |
| `.gitignore` | arquivos ignorados pelo git |

## Testes

```bash
python -m unittest test_main -v
```

## Licença

Projeto academico — use livremente.
