# Experimento: aprendiz vs ingenuo (100.000 rodadas)

**Configuracao:**
- X (J1): `aprendiz`
- O (J2): `ingenuo`
- Semente: 42
- Rodadas: 100.000
- Recompensa: vitoria +10, empate +1, derrota -1
- epsilon: 0.0 (exploracao apenas pelo desempate aleatorio de estados zerados)

Dados: `experiments/learning/eps0_pes1011/rodadas_100000/aprendiz_vs_ingenuo/`

## Resultado acumulado

| Partida | J1 | V | J2 |
|---------|----|---|----|
| 1.000 | 710 | 140 | 150 |
| 10.000 | 7.277 | 1.385 | 1.338 |
| 50.000 | 36.660 | 7.044 | 6.296 |
| 100.000 | 73.234 | 14.078 | 12.688 |

## Evolucao por janela de 10,000 partidas (aprendiz = J1)

| Janela | V | E | D | Aproveitamento (V+E) |
|--------|---|---|---|----------------------|
| 1-10.000 | 7.277 | 1.385 | 1.338 | 86.6% |
| 10.001-20.000 | 7.370 | 1.405 | 1.225 | 87.8% |
| 20.001-30.000 | 7.329 | 1.417 | 1.254 | 87.5% |
| 30.001-40.000 | 7.286 | 1.426 | 1.288 | 87.1% |
| 40.001-50.000 | 7.398 | 1.411 | 1.191 | 88.1% |
| 50.001-60.000 | 7.338 | 1.407 | 1.255 | 87.5% |
| 60.001-70.000 | 7.365 | 1.348 | 1.287 | 87.1% |
| 70.001-80.000 | 7.304 | 1.393 | 1.303 | 87.0% |
| 80.001-90.000 | 7.264 | 1.459 | 1.277 | 87.2% |
| 90.001-100.000 | 7.303 | 1.427 | 1.270 | 87.3% |

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 220 | 405.218 |

## Grafico

`progress.svg` — series `J1 (Aprendiz)` / `V` / `J2 (Ingenuo)` por partida.

## Arquivos

```
experiments/learning/eps0_pes1011/rodadas_100000/aprendiz_vs_ingenuo/
├── episodes.jsonl    # cada decisao (estado, acao), resultado, recompensa
├── progress.jsonl    # linha 0 + 1 linha por partida (100.001 linhas)
├── q_table.json      # snapshot da tabela Q (schema_version 1)
├── progress.svg      # grafico acumulado
└── aprendiz_vs_ingenuo.md    # este relatorio
```

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --rounds 100000 --root experiments/learning/eps0_pes1011
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps0_pes1011/rodadas_100000/aprendiz_vs_ingenuo/progress.jsonl \
  --partida 100000
```

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Plano: aproveitamento (V+E) de 86.6% na primeira janela de 10 mil para 87.3% na ultima. Total 73.234V / 14.078E / 12.688D (73.2% de vitorias; 87.3% sem derrota).

**Em que trecho do grafico ocorreu a mudanca mais importante?**
Nenhuma relevante: variacao total entre janelas de apenas 1.5pp (86.6%-88.1%). Com epsilon 0 a politica converge antes da partida 10,000 e o restante e repeticao deterministica.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Nao. Ultima derrota na partida 99.997, com ~1269 derrotas por janela de 10 mil ate o fim.
