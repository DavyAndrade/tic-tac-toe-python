# Experimento: treino_aprendiz vs ingenuo (200.000 rodadas)

**Configuracao:**
- X (J1): `aprendiz`
- O (J2): `ingenuo`
- Semente: 42
- Rodadas: 200.000
- Recompensa: vitoria +10, empate +1, derrota -1
- epsilon: 0.25 na fase `exploracao`, 0.0 na fase `neutralizacao` (curriculo `treino_*` — nao faz parte do comparativo epsilon 0)

Dados: `experiments/learning/eps0_pes1011/rodadas_100000/treino_aprendiz_vs_ingenuo/`

## Resultado acumulado

| Partida | J1 | V | J2 |
|---------|----|---|----|
| 1.000 | 679 | 132 | 189 |
| 10.000 | 8.043 | 727 | 1.230 |
| 50.000 | 43.630 | 2.573 | 3.797 |
| 100.000 | 89.059 | 4.734 | 6.207 |

## Evolucao por janela de 10,000 partidas (aprendiz = J1)

| Janela | V | E | D | Aproveitamento (V+E) |
|--------|---|---|---|----------------------|
| 1-10.000 | 8.043 | 727 | 1.230 | 87.7% |
| 10.001-20.000 | 8.730 | 507 | 763 | 92.4% |
| 20.001-30.000 | 8.875 | 440 | 685 | 93.2% |
| 30.001-40.000 | 8.948 | 466 | 586 | 94.1% |
| 40.001-50.000 | 9.034 | 433 | 533 | 94.7% |
| 50.001-60.000 | 9.065 | 410 | 525 | 94.8% |
| 60.001-70.000 | 9.071 | 431 | 498 | 95.0% |
| 70.001-80.000 | 9.083 | 435 | 482 | 95.2% |
| 80.001-90.000 | 9.080 | 436 | 484 | 95.2% |
| 90.001-100.000 | 9.130 | 449 | 421 | 95.8% |
| 100.001-110.000 | 9.915 | 85 | 0 | 100.0% |
| 110.001-120.000 | 9.914 | 86 | 0 | 100.0% |
| 120.001-130.000 | 9.894 | 106 | 0 | 100.0% |
| 130.001-140.000 | 9.891 | 109 | 0 | 100.0% |
| 140.001-150.000 | 9.897 | 103 | 0 | 100.0% |
| 150.001-160.000 | 9.895 | 105 | 0 | 100.0% |
| 160.001-170.000 | 9.895 | 105 | 0 | 100.0% |
| 170.001-180.000 | 9.891 | 109 | 0 | 100.0% |
| 180.001-190.000 | 9.902 | 98 | 0 | 100.0% |
| 190.001-200.000 | 9.895 | 105 | 0 | 100.0% |

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 2.414 | 684.835 |

## Grafico

`progress.svg` — series `J1 (Aprendiz)` / `V` / `J2 (Ingenuo)` por partida.

## Arquivos

```
experiments/learning/eps0_pes1011/rodadas_100000/treino_aprendiz_vs_ingenuo/
├── episodes.jsonl    # cada decisao (estado, acao), resultado, recompensa
├── progress.jsonl    # linha 0 + 1 linha por partida (200.001 linhas)
├── q_table.json      # snapshot da tabela Q (schema_version 1)
├── progress.svg      # grafico acumulado
└── treino_aprendiz_vs_ingenuo.md    # este relatorio
```

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --rounds 100000 --root experiments/learning/eps0_pes1011
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps0_pes1011/rodadas_100000/treino_aprendiz_vs_ingenuo/progress.jsonl \
  --partida 200000
```

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Plano: aproveitamento (V+E) de 87.7% na primeira janela de 10 mil para 100.0% na ultima. Total 188.048V / 5.745E / 6.207D (94.0% de vitorias; 96.9% sem derrota).

**Em que trecho do grafico ocorreu a mudanca mais importante?**
Nenhuma relevante: variacao total entre janelas de apenas 12.3pp (87.7%-100.0%). Com epsilon 0 a politica converge antes da partida 10,000 e o restante e repeticao deterministica.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Nao. Ultima derrota na partida 99.983, com ~310 derrotas por janela de 10 mil ate o fim.
