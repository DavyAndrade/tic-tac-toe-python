# Experimento: aprendiz vs ingenuo (100,000 rodadas)

**Configuracao:**
- X (J1): `aprendiz`
- O (J2): `ingenuo`
- Semente: 42
- Rodadas: 100,000
- Recompensa: vitoria +2, empate +1, derrota -5
- epsilon: 0.0 (exploracao apenas pelo desempate aleatorio de estados zerados)

Dados: `experiments/learning/rodadas_100000_eps0/aprendiz_vs_ingenuo/`

## Resultado acumulado

| Partida | J1 (aprendiz) | V | J2 (ingenuo) |
|---------|---------------|---|--------------|
| 1,000 | 764 | 156 | 80 |
| 10,000 | 8,198 | 1,606 | 196 |
| 50,000 | 41,288 | 7,949 | 763 |
| 100,000 | 82,513 | 16,018 | 1,469 |

## Evolucao por janela de 10,000 partidas (aprendiz = J1)

| Janela | V | E | D | Aproveitamento |
|--------|---|---|---|----------------|
| 1-10,000 | 8,198 | 1,606 | 196 | 98.0% |
| 10,001-20,000 | 8,274 | 1,584 | 142 | 98.6% |
| 20,001-30,000 | 8,271 | 1,583 | 146 | 98.5% |
| 30,001-40,000 | 8,265 | 1,605 | 130 | 98.7% |
| 40,001-50,000 | 8,280 | 1,571 | 149 | 98.5% |
| 50,001-60,000 | 8,278 | 1,598 | 124 | 98.8% |
| 60,001-70,000 | 8,237 | 1,595 | 168 | 98.3% |
| 70,001-80,000 | 8,250 | 1,626 | 124 | 98.8% |
| 80,001-90,000 | 8,248 | 1,602 | 150 | 98.5% |
| 90,001-100,000 | 8,212 | 1,648 | 140 | 98.6% |

Leitura: aproveitamento estavel em ~98.5% desde a primeira janela. Contra a
versao epsilon 0.1 (historico do Git: 94,517V / 3,603E / 1,880D, 98.1% de
aproveitamento): epsilon 0 vence menos (82.5% vs 94.5% das partidas) mas
perde menos (1,469 vs 1,880) — a politica greedy converge para linhas seguras
que empatam mais; a exploracao aleatoria da versao antiga encontrava
vitorias com mais frequencia contra o oponente fraco.

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 300 | 403,012 |

Muito menor que a versao epsilon 0.1 (300 vs 2,282 estados): sem exploracao
aleatoria fixa, o agente concentra as jogadas em poucas linhas.

## Grafico

`rodadas_100000_eps0/aprendiz_vs_ingenuo/progress.svg` — series `J1 (Aprendiz)` /
`V` / `J2 (Ingenuo)` por partida. Gerado por `matplotlib` a partir de
`progress.jsonl`.

## Arquivos

```
experiments/learning/rodadas_100000_eps0/aprendiz_vs_ingenuo/
├── episodes.jsonl    # 30M — cada decisao (estado, acao), resultado, recompensa
├── progress.jsonl    # 18M — linha 0 + 1 linha por partida (100,001 linhas)
├── q_table.json      # snapshot da tabela Q (schema_version 1)
└── progress.svg      # grafico acumulado
```

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --rounds 100000 --scenario aprendiz_vs_ingenuo --variant eps0
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/rodadas_100000_eps0/aprendiz_vs_ingenuo/progress.jsonl \
  --partida 100000
```

Execucao deterministica (seed 42): regenera identico com `--variant eps0`;
a versao epsilon 0.1 esta preservada no diretorio sem sufixo (`rodadas_<N>/`).
