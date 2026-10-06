# Experimento: aprendiz vs fera (10,000 rodadas)

**Configuracao:**
- X (J1): `aprendiz`
- O (J2): `fera` (minimax — nunca perde)
- Semente: 42
- Rodadas: 10,000
- Recompensa: vitoria +2, empate +1, derrota -5
- epsilon: 0.0 (exploracao apenas pelo desempate aleatorio de estados zerados)

Dados: `experiments/learning/rodadas_10000/aprendiz_vs_fera/`

## Resultado acumulado

| Partida | J1 (aprendiz) | V | J2 (fera) |
|---------|---------------|---|-----------|
| 1,000 | 0 | 999 | 1 |
| 5,000 | 0 | 4,999 | 1 |
| 10,000 | 0 | 9,999 | 1 |

## Evolucao por janela de 1,000 partidas (aprendiz = J1)

| Janela | V | E | D | Aproveitamento |
|--------|---|---|---|---------------|
| 1-1,000 | 0 | 999 | 1 | 100% |
| 1,001-2,000 | 0 | 1,000 | 0 | 100% |
| 2,001-3,000 | 0 | 1,000 | 0 | 100% |
| 3,001-4,000 | 0 | 1,000 | 0 | 100% |
| 4,001-5,000 | 0 | 1,000 | 0 | 100% |
| 5,001-6,000 | 0 | 1,000 | 0 | 100% |
| 6,001-7,000 | 0 | 1,000 | 0 | 100% |
| 7,001-8,000 | 0 | 1,000 | 0 | 100% |
| 8,001-9,000 | 0 | 1,000 | 0 | 100% |
| 9,001-10,000 | 0 | 1,000 | 0 | 100% |

Leitura: `fera` e invencivel — o teto do aprendiz aqui e o empate, e ele bate
nesse teto em 9,999 de 10,000 partidas. A unica derrota acontece na primeira
janela (aprendizado inicial) e nao se repete. Vitorias zero: esperado contra
minimax perfeito.

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 7 | 49,998 |

Com epsilon 0 e dois jogadores deterministicos, a politica convergiu para uma
unica linha de jogo (7 estados visitados) repetida em todas as partidas —
exploracao adicional so ocorreria em estados nunca visitados.

## Grafico

`rodadas_10000/aprendiz_vs_fera/progress.svg` — series `J1 (Aprendiz)` /
`V` / `J2 (Fera)` por partida. Gerado por `matplotlib` a partir de
`progress.jsonl`.

## Arquivos

```
experiments/learning/rodadas_10000/aprendiz_vs_fera/
├── episodes.jsonl    # cada decisao (estado, acao), resultado, recompensa
├── progress.jsonl    # linha 0 + 1 linha por partida (10,001 linhas)
├── q_table.json      # snapshot da tabela Q (schema_version 1)
└── progress.svg      # grafico acumulado
```

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --rounds 10000 --scenario aprendiz_vs_fera
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/rodadas_10000/aprendiz_vs_fera/progress.jsonl \
  --partida 10000
```

Execucao deterministica (seed 42): regenera identico.
