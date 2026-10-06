# Experimento: aprendiz vs ingenuo

**Configuracao:**
- X (J1): `aprendiz`
- O (J2): `ingenuo`
- Semente: 42
- Rodadas: 1,000
- Recompensa: vitoria +2, empate +1, derrota -5
- epsilon: 0.0 (exploracao apenas pelo desempate aleatorio de estados zerados)

Dados: `experiments/learning/rodadas_1000/aprendiz_vs_ingenuo/`

## Resultado acumulado

| Partida | J1 (aprendiz) | V | J2 (ingenuo) |
|---------|---------------|---|--------------|
| 100 | 72 | 11 | 17 |
| 500 | 366 | 65 | 69 |
| 1,000 | 764 | 156 | 80 |

## Evolucao por janela de 100 partidas (aprendiz = J1)

| Janela | V | E | D | Aproveitamento |
|--------|---|---|---|----------------|
| 1-100 | 72 | 11 | 17 | 83% |
| 101-200 | 74 | 10 | 16 | 84% |
| 201-300 | 71 | 18 | 11 | 89% |
| 301-400 | 75 | 12 | 13 | 87% |
| 401-500 | 74 | 14 | 12 | 88% |
| 501-600 | 76 | 21 | 3 | 97% |
| 601-700 | 79 | 21 | 0 | 100% |
| 701-800 | 80 | 18 | 2 | 98% |
| 801-900 | 82 | 16 | 2 | 98% |
| 901-1000 | 81 | 15 | 4 | 96% |

Leitura: aproveitamento sobe de 83% para ~97% a partir da partida 500 e
zero derrotas na janela 601-700. Nesta amostra curta o agente com epsilon 0
supera a versao anterior com epsilon 0.1 (87% no total).

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 290 | 4,064 |

Politica menor que a versao com epsilon 0.1 (290 vs 809 estados): sem
exploracao aleatoria fixa, o agente concentra as jogadas em menos linhas.

## Grafico

`rodadas_1000/aprendiz_vs_ingenuo/progress.svg` — series `J1 (Aprendiz)` /
`V` / `J2 (Ingenuo)` por partida. Gerado por `matplotlib` a partir de
`progress.jsonl`.

## Arquivos

```
experiments/learning/rodadas_1000/aprendiz_vs_ingenuo/
├── episodes.jsonl    # cada decisao (estado, acao), resultado, recompensa
├── progress.jsonl    # linha 0 + 1 linha por partida (1,001 linhas)
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

Execucao deterministica (seed 42): regenera identico. A versao anterior com
epsilon 0.1 esta no historico do Git (commit `bd4ffa3` e anteriores).
