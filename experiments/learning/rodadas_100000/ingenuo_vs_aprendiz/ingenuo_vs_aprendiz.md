# Experimento: ingenuo vs aprendiz (100,000 rodadas)

**Configuracao:**
- X (J1): `ingenuo`
- O (J2): `aprendiz`
- Semente: 42
- Rodadas: 100,000
- Recompensa: vitoria +2, empate +1, derrota -5
- epsilon: 0.1 (10% das jogadas sempre aleatorias)

Dados: `experiments/learning/rodadas_100000/ingenuo_vs_aprendiz/`

## Resultado acumulado

| Partida | J1 (ingenuo) | V | J2 (aprendiz) |
|---------|--------------|---|---------------|
| 1,000 | 441 | 192 | 367 |
| 10,000 | 1,980 | 2,205 | 5,815 |
| 50,000 | 5,116 | 7,779 | 37,105 |
| 100,000 | 7,487 | 13,708 | 78,805 |

## Evolucao por janela de 10,000 partidas (aprendiz = J2)

| Janela | V | E | D | Aproveitamento |
|--------|---|---|---|----------------|
| 1-10,000 | 5,815 | 2,205 | 1,980 | 80% |
| 10,001-20,000 | 7,268 | 1,658 | 1,074 | 89% |
| 20,001-30,000 | 7,830 | 1,380 | 790 | 92% |
| 30,001-40,000 | 8,035 | 1,297 | 668 | 93% |
| 40,001-50,000 | 8,157 | 1,239 | 604 | 94% |
| 50,001-60,000 | 8,301 | 1,199 | 500 | 95% |
| 60,001-70,000 | 8,310 | 1,183 | 507 | 95% |
| 70,001-80,000 | 8,357 | 1,168 | 475 | 95% |
| 80,001-90,000 | 8,407 | 1,158 | 435 | 96% |
| 90,001-100,000 | 8,325 | 1,221 | 454 | 95% |

Leitura: em O o aprendizado e mais lento que em X — comeca em 80% e sobe
gradualmente ate 95-96% por volta da partida 60,000. A curva em
`progress.svg` mostra a virada: J1 lidera
no inicio, mas J2 ultrapassa o acumulado na partida 1,679 e nunca mais perde.

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 2,076 | 336,389 |

## Grafico

`progress.svg` — series J1/V/J2 por
partida, eixo X numerado. Gerado por `matplotlib` a partir de `progress.jsonl`.

## Arquivos

```
experiments/learning/rodadas_100000/ingenuo_vs_aprendiz/
├── episodes.jsonl    # 29M — cada decisao (estado, acao), resultado, recompensa
├── progress.jsonl    # 18M — linha 0 + 1 linha por partida (100,001 linhas)
├── q_table.json      # snapshot da tabela Q (schema_version 1)
├── progress.svg      # grafico acumulado
└── ingenuo_vs_aprendiz.md    # este relatorio
```

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --rounds 100000 --scenario ingenuo_vs_aprendiz
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/rodadas_100000/ingenuo_vs_aprendiz/progress.jsonl \
  --partida 100000
```

Execucao deterministica (seed 42): regenera identico. Versao de 1,000
rodadas preservada em `rodadas_1000/` e documentada em
`rodadas_1000/ingenuo_vs_aprendiz/ingenuo_vs_aprendiz.md`.
