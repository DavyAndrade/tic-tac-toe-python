# Experimento: aprendiz vs ingenuo (100.000 rodadas)

**Configuracao:**
- X (J1): `aprendiz`
- O (J2): `ingenuo`
- Semente: 42
- Rodadas: 100.000
- Recompensa: vitoria +10, empate +1, derrota -3
- epsilon: 0.0 (exploracao apenas pelo desempate aleatorio de estados zerados)

Dados: `experiments/learning/eps0_pes1013/rodadas_100000/aprendiz_vs_ingenuo/`

## Resultado acumulado

| Partida | J1 | V | J2 |
|---------|----|---|----|
| 1.000 | 728 | 136 | 136 |
| 10.000 | 7.499 | 1.324 | 1.177 |
| 50.000 | 37.736 | 6.755 | 5.509 |
| 100.000 | 75.348 | 13.545 | 11.107 |

## Evolucao por janela de 10,000 partidas (aprendiz = J1)

| Janela | V | E | D | Aproveitamento (V+E) |
|--------|---|---|---|----------------------|
| 1-10.000 | 7.499 | 1.324 | 1.177 | 88.2% |
| 10.001-20.000 | 7.578 | 1.345 | 1.077 | 89.2% |
| 20.001-30.000 | 7.549 | 1.356 | 1.095 | 89.0% |
| 30.001-40.000 | 7.520 | 1.366 | 1.114 | 88.9% |
| 40.001-50.000 | 7.590 | 1.364 | 1.046 | 89.5% |
| 50.001-60.000 | 7.549 | 1.351 | 1.100 | 89.0% |
| 60.001-70.000 | 7.540 | 1.318 | 1.142 | 88.6% |
| 70.001-80.000 | 7.524 | 1.346 | 1.130 | 88.7% |
| 80.001-90.000 | 7.485 | 1.394 | 1.121 | 88.8% |
| 90.001-100.000 | 7.514 | 1.381 | 1.105 | 89.0% |

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 224 | 403.180 |

## Grafico

`progress.svg` — series `J1 (Aprendiz)` / `V` / `J2 (Ingenuo)` por partida.

## Arquivos

```
experiments/learning/eps0_pes1013/rodadas_100000/aprendiz_vs_ingenuo/
├── episodes.jsonl    # cada decisao (estado, acao), resultado, recompensa
├── progress.jsonl    # linha 0 + 1 linha por partida (100.001 linhas)
├── q_table.json      # snapshot da tabela Q (schema_version 1)
├── progress.svg      # grafico acumulado
└── aprendiz_vs_ingenuo.md    # este relatorio
```

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --rounds 100000 --root experiments/learning/eps0_pes1013
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps0_pes1013/rodadas_100000/aprendiz_vs_ingenuo/progress.jsonl \
  --partida 100000
```

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Plano: aproveitamento (V+E) de 88.2% na primeira janela de 10 mil para 89.0% na ultima. Total 75.348V / 13.545E / 11.107D (75.3% de vitorias; 88.9% sem derrota).

**Em que trecho do grafico ocorreu a mudanca mais importante?**
Nenhuma relevante: variacao total entre janelas de apenas 1.3pp (88.2%-89.5%). Com epsilon 0 a politica converge antes da partida 10,000 e o restante e repeticao deterministica.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Nao. Ultima derrota na partida 99.997, com ~1111 derrotas por janela de 10 mil ate o fim.
