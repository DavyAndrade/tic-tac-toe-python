# Relatório — Experimento do Aprendiz vs Ingênuo

Data: 2026-09-30 · Runner: `run_aprendizado.py` · Partidas: 1000 por experimento · Seed: 42

## Escopo

Somente confrontos diretos (fase futura: Fera e currículos):

| Experimento | J1 (X) | J2 (O) |
|---|---|---|
| `aprendiz_vs_ingenuo` | aprendiz | ingenuo |
| `ingenuo_vs_aprendiz` | ingenuo | aprendiz |

## Método

- Agente `aprendiz`: Monte Carlo episódico, tabela começa vazia, aprende ao fim de cada partida.
- Recompensa terminal: vitória `+2`, empate `+1`, derrota `-5`, aplicada a todos os pares `(estado, célula)` da partida.
- Atualização por média incremental: `Q ← Q + (recompensa − Q) / N`.
- ε-greedy com `ε = 0.1` (10% das jogadas sempre aleatórias — limita o teto de aproveitamento).
- `ingenuo` é jogada aleatória em célula vazia. Cada experimento começa com Q zerada.

## Resultado acumulado

### aprendiz_vs_ingenuo (aprendiz = J1)

| Partida | J1 | V | J2 |
|---|---|---|---|
| 100 | 67 | 10 | 23 |
| 500 | 367 | 57 | 76 |
| 1000 | 765 | 109 | 126 |

### ingenuo_vs_aprendiz (aprendiz = J2)

| Partida | J1 | V | J2 |
|---|---|---|---|
| 100 | 50 | 14 | 36 |
| 500 | 240 | 87 | 173 |
| 1000 | 441 | 192 | 367 |

## Evolução por janela (aproveitamento = vitórias + empates)

| Janela | aprendiz como J1 | aprendiz como J2 |
|---|---|---|
| 1–100 | 77% (67V 10E 23D) | 50% (36V 14E 50D) |
| 401–500 | 94% (83V 11E 6D) | 59% (39V 20E 41D) |
| 901–1000 | 93% (81V 12E 7D) | 62% (42V 20E 38D) |

Leitura: o agente aprende em ambos os lados. Como J1 sobe de 77% → ~93% e
estabiliza por volta da partida 400. Como J2 o ganho é menor (50% → 62%) —
com X aleatório e `ε = 0.1`, o segundo jogador tem menos margem para explorar
sem custo. Parte fixa das derrotas vem do ε: 10% das jogadas são aleatórias
para sempre.

## Tabela Q final

| Experimento | Estados | Visitas |
|---|---|---|
| `aprendiz_vs_ingenuo` | 809 | 3991 |
| `ingenuo_vs_aprendiz` | 1102 | 3495 |

## Arquivos por experimento

```
experiments/learning/<experimento>/
├── episodes.jsonl    # cada decisão (estado, ação), resultado, recompensa
├── progress.jsonl    # linha 0 + 1 linha por partida (contagens cumulativas)
├── q_table.json      # snapshot da tabela Q (schema_version 1)
└── progress.svg      # gráfico J1/V/J2 por partida (matplotlib)
```

## Reproduzir e consultar

```bash
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python run_aprendizado.py --rounds 1000
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/aprendiz_vs_ingenuo/progress.jsonl \
  --partida 1000
```

Execução é determinística (seed 42): regenera idêntico.
