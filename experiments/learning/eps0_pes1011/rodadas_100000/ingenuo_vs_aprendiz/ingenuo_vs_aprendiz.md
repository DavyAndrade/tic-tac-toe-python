# Experimento: ingenuo vs aprendiz (100.000 rodadas)

**Configuracao:**
- X (J1): `ingenuo`
- O (J2): `aprendiz`
- Semente: 42
- Rodadas: 100.000
- Recompensa: vitoria +10, empate +1, derrota -1
- epsilon: 0.0 (exploracao apenas pelo desempate aleatorio de estados zerados)

Dados: `experiments/learning/eps0_pes1011/rodadas_100000/ingenuo_vs_aprendiz/`

## Resultado acumulado

| Partida | J1 | V | J2 |
|---------|----|---|----|
| 1.000 | 392 | 196 | 412 |
| 10.000 | 3.167 | 2.259 | 4.574 |
| 50.000 | 14.843 | 11.674 | 23.483 |
| 100.000 | 29.557 | 23.431 | 47.012 |

## Evolucao por janela de 10,000 partidas (aprendiz = J2)

| Janela | V | E | D | Aproveitamento (V+E) |
|--------|---|---|---|----------------------|
| 1-10.000 | 4.574 | 2.259 | 3.167 | 68.3% |
| 10.001-20.000 | 4.696 | 2.357 | 2.947 | 70.5% |
| 20.001-30.000 | 4.751 | 2.419 | 2.830 | 71.7% |
| 30.001-40.000 | 4.752 | 2.292 | 2.956 | 70.4% |
| 40.001-50.000 | 4.710 | 2.347 | 2.943 | 70.6% |
| 50.001-60.000 | 4.668 | 2.310 | 3.022 | 69.8% |
| 60.001-70.000 | 4.694 | 2.346 | 2.960 | 70.4% |
| 70.001-80.000 | 4.657 | 2.389 | 2.954 | 70.5% |
| 80.001-90.000 | 4.758 | 2.318 | 2.924 | 70.8% |
| 90.001-100.000 | 4.752 | 2.394 | 2.854 | 71.5% |

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 701 | 348.209 |

## Grafico

`progress.svg` — series `J1 (Ingenuo)` / `V` / `J2 (Aprendiz)` por partida.

## Arquivos

```
experiments/learning/eps0_pes1011/rodadas_100000/ingenuo_vs_aprendiz/
├── episodes.jsonl    # cada decisao (estado, acao), resultado, recompensa
├── progress.jsonl    # linha 0 + 1 linha por partida (100.001 linhas)
├── q_table.json      # snapshot da tabela Q (schema_version 1)
├── progress.svg      # grafico acumulado
└── ingenuo_vs_aprendiz.md    # este relatorio
```

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --rounds 100000 --root experiments/learning/eps0_pes1011
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps0_pes1011/rodadas_100000/ingenuo_vs_aprendiz/progress.jsonl \
  --partida 100000
```

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Plano: aproveitamento (V+E) de 68.3% na primeira janela de 10 mil para 71.5% na ultima. Total 47.012V / 23.431E / 29.557D (47.0% de vitorias; 70.4% sem derrota).

**Em que trecho do grafico ocorreu a mudanca mais importante?**
Nenhuma relevante: variacao total entre janelas de apenas 3.4pp (68.3%-71.7%). Com epsilon 0 a politica converge antes da partida 10,000 e o restante e repeticao deterministica.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Nao. Ultima derrota na partida 99.999, com ~2956 derrotas por janela de 10 mil ate o fim.
