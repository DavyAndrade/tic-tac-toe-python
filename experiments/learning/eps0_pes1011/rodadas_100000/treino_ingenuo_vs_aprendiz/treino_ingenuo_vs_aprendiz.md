# Experimento: treino_ingenuo vs aprendiz (200.000 rodadas)

**Configuracao:**
- X (J1): `ingenuo`
- O (J2): `aprendiz`
- Semente: 42
- Rodadas: 200.000
- Recompensa: vitoria +10, empate +1, derrota -1
- epsilon: 0.25 na fase `exploracao`, 0.0 na fase `neutralizacao` (curriculo `treino_*` — nao faz parte do comparativo epsilon 0)

Dados: `experiments/learning/eps0_pes1011/rodadas_100000/treino_ingenuo_vs_aprendiz/`

## Resultado acumulado

| Partida | J1 | V | J2 |
|---------|----|---|----|
| 1.000 | 403 | 132 | 465 |
| 10.000 | 2.891 | 1.036 | 6.073 |
| 50.000 | 10.888 | 4.001 | 35.111 |
| 100.000 | 19.320 | 7.757 | 72.923 |

## Evolucao por janela de 10,000 partidas (aprendiz = J2)

| Janela | V | E | D | Aproveitamento (V+E) |
|--------|---|---|---|----------------------|
| 1-10.000 | 6.073 | 1.036 | 2.891 | 71.1% |
| 10.001-20.000 | 6.993 | 809 | 2.198 | 78.0% |
| 20.001-30.000 | 7.244 | 701 | 2.055 | 79.5% |
| 30.001-40.000 | 7.444 | 686 | 1.870 | 81.3% |
| 40.001-50.000 | 7.357 | 769 | 1.874 | 81.3% |
| 50.001-60.000 | 7.398 | 756 | 1.846 | 81.5% |
| 60.001-70.000 | 7.528 | 781 | 1.691 | 83.1% |
| 70.001-80.000 | 7.577 | 715 | 1.708 | 82.9% |
| 80.001-90.000 | 7.642 | 742 | 1.616 | 83.8% |
| 90.001-100.000 | 7.667 | 762 | 1.571 | 84.3% |
| 100.001-110.000 | 9.139 | 411 | 450 | 95.5% |
| 110.001-120.000 | 9.143 | 425 | 432 | 95.7% |
| 120.001-130.000 | 9.155 | 461 | 384 | 96.2% |
| 130.001-140.000 | 9.209 | 398 | 393 | 96.1% |
| 140.001-150.000 | 9.167 | 445 | 388 | 96.1% |
| 150.001-160.000 | 9.110 | 451 | 439 | 95.6% |
| 160.001-170.000 | 9.173 | 421 | 406 | 95.9% |
| 170.001-180.000 | 9.172 | 411 | 417 | 95.8% |
| 180.001-190.000 | 9.092 | 455 | 453 | 95.5% |
| 190.001-200.000 | 9.163 | 420 | 417 | 95.8% |

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 2.096 | 655.448 |

## Grafico

`progress.svg` — series `J1 (Ingenuo)` / `V` / `J2 (Aprendiz)` por partida.

## Arquivos

```
experiments/learning/eps0_pes1011/rodadas_100000/treino_ingenuo_vs_aprendiz/
├── episodes.jsonl    # cada decisao (estado, acao), resultado, recompensa
├── progress.jsonl    # linha 0 + 1 linha por partida (200.001 linhas)
├── q_table.json      # snapshot da tabela Q (schema_version 1)
├── progress.svg      # grafico acumulado
└── treino_ingenuo_vs_aprendiz.md    # este relatorio
```

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --rounds 100000 --root experiments/learning/eps0_pes1011
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps0_pes1011/rodadas_100000/treino_ingenuo_vs_aprendiz/progress.jsonl \
  --partida 200000
```

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Plano: aproveitamento (V+E) de 71.1% na primeira janela de 10 mil para 95.8% na ultima. Total 164.446V / 12.055E / 23.499D (82.2% de vitorias; 88.3% sem derrota).

**Em que trecho do grafico ocorreu a mudanca mais importante?**
Nenhuma relevante: variacao total entre janelas de apenas 25.1pp (71.1%-96.2%). Com epsilon 0 a politica converge antes da partida 10,000 e o restante e repeticao deterministica.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Nao. Ultima derrota na partida 199.984, com ~1175 derrotas por janela de 10 mil ate o fim.
