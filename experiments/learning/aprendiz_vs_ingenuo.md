# Experimento: aprendiz vs ingenuo

**Configuracao:**
- X (J1): `aprendiz`
- O (J2): `ingenuo`
- Semente: 42
- Rodadas: 1,000
- Recompensa: vitoria +2, empate +1, derrota -5
- epsilon: 0.1 (10% das jogadas sempre aleatorias)

## Resultado acumulado

| Partida | J1 (aprendiz) | V | J2 (ingenuo) |
|---------|---------------|---|--------------|
| 100 | 67 | 10 | 23 |
| 500 | 367 | 57 | 76 |
| 1,000 | 765 | 109 | 126 |

## Evolucao por janela de 100 partidas (aprendiz = J1)

| Janela | V | E | D | Aproveitamento |
|--------|---|---|---|----------------|
| 1-100 | 67 | 10 | 23 | 77% |
| 101-200 | 65 | 17 | 18 | 82% |
| 201-300 | 80 | 8 | 12 | 88% |
| 301-400 | 72 | 11 | 17 | 83% |
| 401-500 | 83 | 11 | 6 | 94% |
| 501-600 | 81 | 7 | 12 | 88% |
| 601-700 | 77 | 10 | 13 | 87% |
| 701-800 | 81 | 11 | 8 | 92% |
| 801-900 | 78 | 12 | 10 | 90% |
| 901-1000 | 81 | 12 | 7 | 93% |

Leitura: aproveitamento sobe de 77% para ~93% e estabiliza por volta da
partida 400. O teto parcial vem do epsilon: 10% das jogadas sao aleatorias
para sempre, entao o agente nunca chega a 100%.

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 809 | 3,991 |

## Grafico

`progress.svg` — series J1/V/J2 por partida, eixo X numerado de 100 em 100.
Gerado por `matplotlib` a partir de `progress.jsonl`.

## Arquivos

```
experiments/learning/rodadas_1000/aprendiz_vs_ingenuo/
├── episodes.jsonl    # cada decisao (estado, acao), resultado, recompensa
├── progress.jsonl    # linha 0 + 1 linha por partida
├── q_table.json      # snapshot da tabela Q (schema_version 1)
└── progress.svg      # grafico acumulado
```

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --rounds 1000 --scenario aprendiz_vs_ingenuo
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/rodadas_1000/aprendiz_vs_ingenuo/progress.jsonl \
  --partida 1000
```

Execucao deterministica (seed 42): regenera identico.
