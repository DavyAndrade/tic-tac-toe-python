# TicTacToe - Paradigma Funcional/Data-Driven

Implementacao em estilo funcional: funcoes puras recebem um **tabuleiro imutavel** e
retornam um **novo tabuleiro**. Tab e tupla imutavel de 9 posicoes (indices `0..8`):

```
 0 | 1 | 2
 3 | 4 | 5
 6 | 7 | 8
```

Valores: `'X'`, `'O'` ou `' '`.

## Algoritmos

| nome     | funcao     | estrategia                                    |
|----------|------------|-----------------------------------------------|
| `ingenuo`  | `ingenuo()`  | escolhe jogada aleatoria entre celulas vazias |
| `fera`     | `fera()`     | algoritmo **minimax** puro — nunca perde      |
| `humano`   | `humano()`   | le coordenada `0-8` do input                  |

### Fera (minimax)

Busca exaustiva do espaco de jogadas. Avalia terminal:

- vitoria de **X** → score `10 - depth` (ganha mais cedo vale mais)
- vitoria de **O** → score `depth - 10`
- empate → `0`

X (maximo) e O (minimo) alternam. Resultado garantido: **fera nunca perde**.

## API (funcoes puras)

```python
tab_vazio() -> Tab                           # nova tupla vazia
get_winner(board) -> 'X' | 'O' | None        # vencedor ou None
is_full(board) -> bool
get_empty_cells(board) -> tuple[int,..]
minimax(board, player, depth=0) -> (score, cell)
ingenuo(board, player, rng) -> Tab           # jogada aleatoria
fera(board, player, _rng) -> Tab             # minimax
humano(board, player, _rng) -> Tab           # input
play_game(p1_fn, p2_fn, seed=0) -> dict      # partida unica
compete(name1, name2, rounds, start_player=0) -> list[dict]
```

## Formato de resultado (JSON)

Cada partida produz:

```json
{
  "id": 1,
  "j1": "ingenuo",
  "v": 0,
  "j2": "fera",
  "n": 6,
  "winner": "fera",
  "t0": -1, "t1": 0, "t2": 1, "t3": 1, "t4": -1,
  "t5": 0, "t6": 0, "t7": 1, "t8": -1
}
```

| campo     | descricao                                          |
|-----------|----------------------------------------------------|
| `id`      | ID sequencial da partida                           |
| `j1`      | nome do algoritmo Jogador 1 (joga X)               |
| `v`       | `0` = empate ou J2 venceu, `1` = J1 venceu        |
| `j2`      | nome do algoritmo Jogador 2 (joga O)               |
| `n`       | numero de jogadas ate fim                          |
| `winner`  | nome do vencedor ou `"draw"`                       |
| `t0`-`t8` | `1` = marca J1, `0` = vazio, `-1` = marca J2     |

## Uso

```bash
# Demo: ingenuo vs fera, 100 partidas
python main.py demo

# Visualiza partida jogada por jogada
python main.py show ingenuo fera
python main.py show fera ingenuo

# Humano vs algoritmo
python main.py play fera --first    # humano joga X (primeiro)
python main.py play ingenuo         # humano joga O (segundo)

# Competicao: N1 vs N2, R rounds, formato txt|json
python main.py compete ingenuo fera 100 json

# Navegador interativo de resultados
python main.py view results_ingenuo_fera.json

# Auto-teste: fera nao deve perder
python main.py test

# Torneios rapidos (4 combinacoes, 100k rodadas)
python run_torneio.py

# Torneio especifico
python run_torneio.py fera ingenuo 500000
```

## Experimentos

Progressivos de 100k a 1M rodadas (100k passo). Ordem alternada, semente 42.

| experimento | resultado |
|-------------|-----------|
| [ingenuo vs ingenuo](experimento_ingenuo_vs_ingenuo.md) | aleatorio vs aleatorio |
| [ingenuo vs fera](experimento_ingenuo_vs_fera.md) | ingenuo nunca ganha |
| [fera vs ingenuo](experimento_fera_vs_ingenuo.md) | fera domina |
| [fera vs fera](experimento_fera_vs_fera.md) | sempre empate |
| [guloso vs fera](experimento_guloso_vs_fera.md) | guloso (externo) vs fera |

### Adicionando algoritmo externo

```bash
# Formato: label:arquivo.py:funcao
python gen_progressivo.py "guloso:outro_aluno.py:guloso" fera

# Ou qualquer arquivo com assinatura fn(board, player, rng) -> Tab
python gen_progressivo.py "meu_algo:meu.py:minha_funcao" fera
```

## Arquivos

| arquivo | descricao |
|---------|-----------|
| `main.py` | implementacao (funcional, imutavel) |
| `run_torneio.py` | torneios rapidos em massa |
| `gen_progressivo.py` | gerador de experimentos progressivos |
| `test_main.py` | testes unitarios |
| `outro_aluno.py` | estrategia externa (guloso) |
| `experimento_*.md` | resultados dos experimentos |
| `results_*_100k.json` - `results_*_1M.json` | dados brutos |
| `README.md` | este documento |

## Testes

```bash
python -m unittest test_main -v
```
