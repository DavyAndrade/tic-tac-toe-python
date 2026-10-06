# Experimento: ingenuo vs aprendiz

**Configuracao:**
- X (J1): `ingenuo`
- O (J2): `aprendiz`
- Semente: 42
- Rodadas: 1,000
- Recompensa: vitoria +2, empate +1, derrota -5
- epsilon: 0.1 (10% das jogadas sempre aleatorias)

## Resultado acumulado

| Partida | J1 (ingenuo) | V | J2 (aprendiz) |
|---------|--------------|---|---------------|
| 100 | 50 | 14 | 36 |
| 500 | 240 | 87 | 173 |
| 1,000 | 441 | 192 | 367 |

## Evolucao por janela de 100 partidas (aprendiz = J2)

| Janela | V | E | D | Aproveitamento |
|--------|---|---|---|----------------|
| 1-100 | 36 | 14 | 50 | 50% |
| 101-200 | 32 | 15 | 53 | 47% |
| 201-300 | 33 | 20 | 47 | 53% |
| 301-400 | 33 | 18 | 49 | 51% |
| 401-500 | 39 | 20 | 41 | 59% |
| 501-600 | 35 | 21 | 44 | 56% |
| 601-700 | 37 | 18 | 45 | 55% |
| 701-800 | 43 | 18 | 39 | 61% |
| 801-900 | 37 | 28 | 35 | 65% |
| 901-1000 | 42 | 20 | 38 | 62% |

Leitura: como segundo jogador o ganho e menor (50% para ~62%). Com o
oponente aleatorio e epsilon em 10%, o agente em O tem menos margem para
explorar sem custo. A partir da partida 700 a janela fica consistentemente
acima de 60%.

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 1,102 | 3,495 |

## Grafico

`progress.svg` — series J1/V/J2 por partida, eixo X numerado de 100 em 100.
Gerado por `matplotlib` a partir de `progress.jsonl`.

## Arquivos

```
experiments/learning/rodadas_1000/ingenuo_vs_aprendiz/
├── episodes.jsonl    # cada decisao (estado, acao), resultado, recompensa
├── progress.jsonl    # linha 0 + 1 linha por partida
├── q_table.json      # snapshot da tabela Q (schema_version 1)
├── progress.svg      # grafico acumulado
└── ingenuo_vs_aprendiz.md    # este relatorio
```

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --rounds 1000 --scenario ingenuo_vs_aprendiz
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/rodadas_1000/ingenuo_vs_aprendiz/progress.jsonl \
  --partida 1000
```

Execucao deterministica (seed 42): regenera identico.
