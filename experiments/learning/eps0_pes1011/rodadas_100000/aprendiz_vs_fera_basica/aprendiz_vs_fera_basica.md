# Experimento: aprendiz vs fera_basica (100.000 rodadas)

**Configuracao:**
- X (J1): `aprendiz`
- O (J2): `fera_basica`
- Semente: 42
- Rodadas: 100.000
- Recompensa: vitoria +10, empate +1, derrota -1
- epsilon: 0.0 (exploracao apenas pelo desempate aleatorio de estados zerados)

Dados: `experiments/learning/eps0_pes1011/rodadas_100000/aprendiz_vs_fera_basica/`

## Resultado acumulado

| Partida | J1 | V | J2 |
|---------|----|---|----|
| 1.000 | 0 | 994 | 6 |
| 10.000 | 0 | 9.994 | 6 |
| 50.000 | 0 | 49.994 | 6 |
| 100.000 | 0 | 99.994 | 6 |

## Evolucao por janela de 10,000 partidas (aprendiz = J1)

| Janela | V | E | D | Aproveitamento (V+E) |
|--------|---|---|---|----------------------|
| 1-10.000 | 0 | 9.994 | 6 | 99.9% |
| 10.001-20.000 | 0 | 10.000 | 0 | 100.0% |
| 20.001-30.000 | 0 | 10.000 | 0 | 100.0% |
| 30.001-40.000 | 0 | 10.000 | 0 | 100.0% |
| 40.001-50.000 | 0 | 10.000 | 0 | 100.0% |
| 50.001-60.000 | 0 | 10.000 | 0 | 100.0% |
| 60.001-70.000 | 0 | 10.000 | 0 | 100.0% |
| 70.001-80.000 | 0 | 10.000 | 0 | 100.0% |
| 80.001-90.000 | 0 | 10.000 | 0 | 100.0% |
| 90.001-100.000 | 0 | 10.000 | 0 | 100.0% |

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 18 | 499.989 |

## Grafico

`progress.svg` — series `J1 (Aprendiz)` / `V` / `J2 (Fera_basica)` por partida.

## Arquivos

```
experiments/learning/eps0_pes1011/rodadas_100000/aprendiz_vs_fera_basica/
├── episodes.jsonl    # cada decisao (estado, acao), resultado, recompensa
├── progress.jsonl    # linha 0 + 1 linha por partida (100.001 linhas)
├── q_table.json      # snapshot da tabela Q (schema_version 1)
├── progress.svg      # grafico acumulado
└── aprendiz_vs_fera_basica.md    # este relatorio
```

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --rounds 100000 --root experiments/learning/eps0_pes1011
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps0_pes1011/rodadas_100000/aprendiz_vs_fera_basica/progress.jsonl \
  --partida 100000
```

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Plano: aproveitamento (V+E) de 99.9% na primeira janela de 10 mil para 100.0% na ultima. Total 0V / 99.994E / 6D (0.0% de vitorias; 100.0% sem derrota).

**Em que trecho do grafico ocorreu a mudanca mais importante?**
Nenhuma relevante: variacao total entre janelas de apenas 0.1pp (99.9%-100.0%). Com epsilon 0 a politica converge antes da partida 10,000 e o restante e repeticao deterministica.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Nao. Ultima derrota na partida 6, com ~1 derrotas por janela de 10 mil ate o fim.
