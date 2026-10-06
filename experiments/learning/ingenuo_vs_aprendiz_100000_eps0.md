# Experimento: ingenuo vs aprendiz (100,000 rodadas)

**Configuracao:**
- X (J1): `ingenuo`
- O (J2): `aprendiz`
- Semente: 42
- Rodadas: 100,000
- Recompensa: vitoria +2, empate +1, derrota -5
- epsilon: 0.0 (exploracao apenas pelo desempate aleatorio de estados zerados)

Dados: `experiments/learning/rodadas_100000_eps0/ingenuo_vs_aprendiz/`

## Resultado acumulado

| Partida | J1 (ingenuo) | V | J2 (aprendiz) |
|---------|--------------|---|---------------|
| 1,000 | 370 | 197 | 433 |
| 10,000 | 1,492 | 2,748 | 5,760 |
| 50,000 | 5,396 | 14,862 | 29,742 |
| 100,000 | 10,160 | 29,871 | 59,969 |

## Evolucao por janela de 10,000 partidas (aprendiz = J2)

| Janela | V | E | D | Aproveitamento |
|--------|---|---|---|----------------|
| 1-10,000 | 5,760 | 2,748 | 1,492 | 85.1% |
| 10,001-20,000 | 6,096 | 2,978 | 926 | 90.7% |
| 20,001-30,000 | 6,023 | 3,043 | 934 | 90.7% |
| 30,001-40,000 | 5,991 | 2,954 | 1,055 | 89.5% |
| 40,001-50,000 | 5,872 | 3,139 | 989 | 90.1% |
| 50,001-60,000 | 6,157 | 2,887 | 956 | 90.4% |
| 60,001-70,000 | 5,896 | 3,100 | 1,004 | 90.0% |
| 70,001-80,000 | 6,074 | 2,969 | 957 | 90.4% |
| 80,001-90,000 | 6,001 | 3,084 | 915 | 90.8% |
| 90,001-100,000 | 6,099 | 2,969 | 932 | 90.7% |

Leitura: em O o aprendizado sobe de 85% para ~90% e estabiliza ja na
segunda janela. Contra a versao epsilon 0.1 (historico do Git: 7,487 derrotas
/ 13,708 empates / 78,805 vitorias, 92.5% de aproveitamento): epsilon 0
rendeu menos aqui — menos vitorias (59,969 vs 78,805), mais derrotas
(10,160 vs 7,487) e aproveitamento 90.0% vs 92.5%. Sem exploracao aleatoria
o agente em O explora menos as linhas do ingenuo e converge rapido para
poucas respostas.

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 1,070 | 350,088 |

Contra 2,076 estados da versao epsilon 0.1: politica concentrada pela falta
de exploracao fixa.

## Grafico

`rodadas_100000_eps0/ingenuo_vs_aprendiz/progress.svg` — series `J1 (Ingenuo)` /
`V` / `J2 (Aprendiz)` por partida. Gerado por `matplotlib` a partir de
`progress.jsonl`.

## Arquivos

```
experiments/learning/rodadas_100000_eps0/ingenuo_vs_aprendiz/
├── episodes.jsonl    # 30M — cada decisao (estado, acao), resultado, recompensa
├── progress.jsonl    # 18M — linha 0 + 1 linha por partida (100,001 linhas)
├── q_table.json      # snapshot da tabela Q (schema_version 1)
└── progress.svg      # grafico acumulado
```

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --rounds 100000 --scenario ingenuo_vs_aprendiz --variant eps0
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/rodadas_100000_eps0/ingenuo_vs_aprendiz/progress.jsonl \
  --partida 100000
```

Execucao deterministica (seed 42): regenera identico com `--variant eps0`;
a versao epsilon 0.1 esta preservada no diretorio sem sufixo (`rodadas_<N>/`).
