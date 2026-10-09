# Experimento: aprendiz vs ingenuo (100.000 rodadas)

**Configuracao:**
- X (J1): `aprendiz`
- O (J2): `ingenuo`
- Semente: 42
- Rodadas: 100.000
- Recompensa: vitoria +10, empate +0, derrota -1
- epsilon: 0.0 (exploracao apenas pelo desempate aleatorio de estados zerados)

Dados: `experiments/learning/eps0_pes1001/rodadas_100000/aprendiz_vs_ingenuo/`

## Resultado acumulado

| Partida | J1 | V | J2 |
|---------|----|---|----|
| 1.000 | 762 | 93 | 145 |
| 10.000 | 7.863 | 857 | 1.280 |
| 50.000 | 39.435 | 4.303 | 6.262 |
| 100.000 | 78.769 | 8.643 | 12.588 |

## Evolucao por janela de 10,000 partidas (aprendiz = J1)

| Janela | V | E | D | Aproveitamento (V+E) |
|--------|---|---|---|----------------------|
| 1-10.000 | 7.863 | 857 | 1.280 | 87.2% |
| 10.001-20.000 | 7.883 | 850 | 1.267 | 87.3% |
| 20.001-30.000 | 7.881 | 887 | 1.232 | 87.7% |
| 30.001-40.000 | 7.884 | 841 | 1.275 | 87.2% |
| 40.001-50.000 | 7.924 | 868 | 1.208 | 87.9% |
| 50.001-60.000 | 7.923 | 836 | 1.241 | 87.6% |
| 60.001-70.000 | 7.879 | 864 | 1.257 | 87.4% |
| 70.001-80.000 | 7.844 | 870 | 1.286 | 87.1% |
| 80.001-90.000 | 7.851 | 881 | 1.268 | 87.3% |
| 90.001-100.000 | 7.837 | 889 | 1.274 | 87.3% |

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 230 | 399.294 |

## Grafico

`progress.svg` — series `J1 (Aprendiz)` / `V` / `J2 (Ingenuo)` por partida.

## Arquivos

```
experiments/learning/eps0_pes1001/rodadas_100000/aprendiz_vs_ingenuo/
├── episodes.jsonl    # cada decisao (estado, acao), resultado, recompensa
├── progress.jsonl    # linha 0 + 1 linha por partida (100.001 linhas)
├── q_table.json      # snapshot da tabela Q (schema_version 1)
├── progress.svg      # grafico acumulado
└── aprendiz_vs_ingenuo.md    # este relatorio
```

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --rounds 100000 --root experiments/learning/eps0_pes1001
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps0_pes1001/rodadas_100000/aprendiz_vs_ingenuo/progress.jsonl \
  --partida 100000
```

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Plano: aproveitamento (V+E) de 87.2% na primeira janela de 10 mil para 87.3% na ultima. Total 78.769V / 8.643E / 12.588D (78.8% de vitorias; 87.4% sem derrota).

**Em que trecho do grafico ocorreu a mudanca mais importante?**
Nenhuma relevante: variacao total entre janelas de apenas 0.8pp (87.1%-87.9%). Com epsilon 0 a politica converge antes da partida 10,000 e o restante e repeticao deterministica.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Nao. Ultima derrota na partida 99.997, com ~1259 derrotas por janela de 10 mil ate o fim.
