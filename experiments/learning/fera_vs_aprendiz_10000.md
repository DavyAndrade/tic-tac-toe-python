# Experimento: fera vs aprendiz (10,000 rodadas)

**Configuracao:**
- X (J1): `fera` (minimax — nunca perde)
- O (J2): `aprendiz`
- Semente: 42
- Rodadas: 10,000
- Recompensa: vitoria +2, empate +1, derrota -5
- epsilon: 0.0 (exploracao apenas pelo desempate aleatorio de estados zerados)

Dados: `experiments/learning/rodadas_10000/fera_vs_aprendiz/`

## Resultado acumulado

| Partida | J1 (fera) | V | J2 (aprendiz) |
|---------|-----------|---|---------------|
| 1,000 | 115 | 885 | 0 |
| 5,000 | 115 | 4,885 | 0 |
| 10,000 | 115 | 9,885 | 0 |

## Evolucao por janela de 1,000 partidas (aprendiz = J2)

| Janela | V | E | D | Aproveitamento |
|--------|---|---|---|---------------|
| 1-1,000 | 0 | 885 | 115 | 88% |
| 1,001-2,000 | 0 | 1,000 | 0 | 100% |
| 2,001-3,000 | 0 | 1,000 | 0 | 100% |
| 3,001-4,000 | 0 | 1,000 | 0 | 100% |
| 4,001-5,000 | 0 | 1,000 | 0 | 100% |
| 5,001-6,000 | 0 | 1,000 | 0 | 100% |
| 6,001-7,000 | 0 | 1,000 | 0 | 100% |
| 7,001-8,000 | 0 | 1,000 | 0 | 100% |
| 8,001-9,000 | 0 | 1,000 | 0 | 100% |
| 9,001-10,000 | 0 | 1,000 | 0 | 100% |

Leitura: com o aprendiz em O ele erra mais no comeco — 115 derrotas todas na
primeira janela (11,5% daquelas partidas). Depois da partida 1,000 nao perde
mais nenhuma: as 9 janelas seguintes sao 100% empates. Contra minimax
perfeito o empate e o teto, e ele e atingido desde a janela 2.

Comparado com `aprendiz_vs_fera` (1 derrota total), o aprendiz como segundo
jogador precisa de ~115 partidas de castigo antes de estabilizar.

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 18 | 39,787 |

Com epsilon 0 a politica converge para poucas linhas (18 estados) repetidas
em todas as partidas — exploracao adicional so ocorreria em estados nunca
visitados.

## Grafico

`rodadas_10000/fera_vs_aprendiz/progress.svg` — series `J1 (Fera)` / `V` /
`J2 (Aprendiz)` por partida. Gerado por `matplotlib` a partir de
`progress.jsonl`.

## Arquivos

```
experiments/learning/rodadas_10000/fera_vs_aprendiz/
├── episodes.jsonl    # cada decisao (estado, acao), resultado, recompensa
├── progress.jsonl    # linha 0 + 1 linha por partida (10,001 linhas)
├── q_table.json      # snapshot da tabela Q (schema_version 1)
└── progress.svg      # grafico acumulado
```

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --rounds 10000 --scenario fera_vs_aprendiz
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/rodadas_10000/fera_vs_aprendiz/progress.jsonl \
  --partida 10000
```

Execucao deterministica (seed 42): regenera identico.
