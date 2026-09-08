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

## Formato de resultado (JSON)

Cada partida produz:

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
  "t0": 1, "t1": 1, "t2": 1, "t3": 0, "t4": 0,
  "t5": 0, "t6": 0, "t7": 0, "t8": 0
}
```

| campo      | descricao                                             |
|------------|-------------------------------------------------------|
| `id`       | ID sequencial da partida                              |
| `j1`       | `1` = J1 venceu, `0` = nao venceu                    |
| `v`        | `1` = empate/velha, `0` = sem empate                  |
| `j2`       | `1` = J2 venceu, `0` = nao venceu                    |
| `winner`   | `1` = J1, `-1` = J2, `0` = empate                    |
| `n`        | numero de jogadas ate fim                             |
| `j1_name`  | nome da estrategia do Jogador 1                       |
| `j2_name`  | nome da estrategia do Jogador 2                       |
| `t0`-`t8`  | `1` = marca J1, `0` = vazio, `-1` = marca J2        |

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

# Competicao: N1 vs N2, R rounds
python main.py compete ingenuo fera 100 json

# Navegador interativo de resultados
python main.py view results_ingenuo_fera.json

# Auto-teste: fera nao deve perder
python main.py test

# Torneios rapidos
python run_torneio.py

# Torneio especifico
python run_torneio.py fera ingenuo 500000
```

## Experimentos

Progressivos de 100k a 1M rodadas (100k passo). Sem alternancia de ordem.

| experimento | resultado |
|-------------|-----------|
| [ingenuo vs ingenuo](experimento_ingenuo_vs_ingenuo.md) | aleatorio vs aleatorio |
| [ingenuo vs fera](experimento_ingenuo_vs_fera.md) | ingenuo nunca ganha |
| [fera vs ingenuo](experimento_fera_vs_ingenuo.md) | fera domina (~99.5%) |
| [fera vs fera](experimento_fera_vs_fera.md) | sempre empate |

### Adicionando algoritmo externo

```bash
# Formato: label:arquivo.py:funcao
python gen_progressivo.py "avarento:outro_aluno.py:avarento" fera

# Ou qualquer arquivo com assinatura fn(board, player, rng) -> Tab
python gen_progressivo.py "meu_algo:meu.py:minha_funcao" fera
```

## Post LinkedIn

[linkedin_post.md](linkedin_post.md) — post pronto para copiar e colar.

## Arquivos

| arquivo | descricao |
|---------|-----------|
| `main.py` | implementacao (funcional, imutavel) |
| `run_torneio.py` | torneios rapidos em massa |
| `gen_progressivo.py` | gerador de experimentos progressivos |
| `test_main.py` | testes unitarios |
| `outro_aluno.py` | estrategia externa (avarento) |
| `experimento_*.md` | resultados dos experimentos |
| `linkedin_post.md` | post para LinkedIn |
| `README.md` | este documento |

## Testes

```bash
python -m unittest test_main -v
```
