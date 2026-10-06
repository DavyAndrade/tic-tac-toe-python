# Experimento: aprendiz vs fera_basica (10,000 rodadas)

**Configuracao:**
- X (J1): `aprendiz`
- O (J2): `fera_basica` (regras heuristicas)
- Semente: 42
- Rodadas: 10,000
- Recompensa: vitoria +2, empate +1, derrota -5
- epsilon: 0.0 (exploracao apenas pelo desempate aleatorio de estados zerados)

Dados: `experiments/learning/rodadas_10000/aprendiz_vs_fera_basica/`

## Resultado acumulado

| Partida | J1 (aprendiz) | V | J2 (fera_basica) |
|---------|---------------|---|------------------|
| 1,000 | 0 | 994 | 6 |
| 5,000 | 0 | 4,994 | 6 |
| 10,000 | 0 | 9,994 | 6 |

## Evolucao por janela de 1,000 partidas (aprendiz = J1)

| Janela | V | E | D | Aproveitamento |
|--------|---|---|---|---------------|
| 1-1,000 | 0 | 994 | 6 | 99.4% |
| 1,001-2,000 | 0 | 1,000 | 0 | 100% |
| 2,001-3,000 | 0 | 1,000 | 0 | 100% |
| 3,001-4,000 | 0 | 1,000 | 0 | 100% |
| 4,001-5,000 | 0 | 1,000 | 0 | 100% |
| 5,001-6,000 | 0 | 1,000 | 0 | 100% |
| 6,001-7,000 | 0 | 1,000 | 0 | 100% |
| 7,001-8,000 | 0 | 1,000 | 0 | 100% |
| 8,001-9,000 | 0 | 1,000 | 0 | 100% |
| 9,001-10,000 | 0 | 1,000 | 0 | 100% |

Leitura: as 6 derrotas acontecem todas na primeira janela (0,6% das partidas
daquela fase) e nunca mais se repetem. Contra `fera_basica` o aprendiz nao
consegue vitorias (0 em 10,000) — a heuristica basica nao cede linha aberta
na politica convergida do agente, entao o resultado estabiliza em 100%
empates a partir da partida 1,001.

Comparar com `aprendiz_vs_ingenuo`, onde o mesmo agente vencia ~94% das
partidas: o oponente determina o teto.

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 18 | 49,989 |

Com epsilon 0 e dois jogadores deterministicos, a politica converge para
poucas linhas repetidas — exploracao nova so ocorre em estados nunca
visitados.

## Grafico

`rodadas_10000/aprendiz_vs_fera_basica/progress.svg` — series
`J1 (Aprendiz)` / `V` / `J2 (Fera basica)` por partida. Gerado por
`matplotlib` a partir de `progress.jsonl`.

## Arquivos

```
experiments/learning/rodadas_10000/aprendiz_vs_fera_basica/
├── episodes.jsonl    # cada decisao (estado, acao), resultado, recompensa
├── progress.jsonl    # linha 0 + 1 linha por partida (10,001 linhas)
├── q_table.json      # snapshot da tabela Q (schema_version 1)
└── progress.svg      # grafico acumulado
```

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --rounds 10000 --scenario aprendiz_vs_fera_basica
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/rodadas_10000/aprendiz_vs_fera_basica/progress.jsonl \
  --partida 10000
```

Execucao deterministica (seed 42): regenera identico.
