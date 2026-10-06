# Experimento: fera_basica vs aprendiz (10,000 rodadas)

**Configuracao:**
- X (J1): `fera_basica` (regras heuristicas)
- O (J2): `aprendiz`
- Semente: 42
- Rodadas: 10,000
- Recompensa: vitoria +2, empate +1, derrota -5
- epsilon: 0.0 (exploracao apenas pelo desempate aleatorio de estados zerados)

Dados: `experiments/learning/rodadas_10000/fera_basica_vs_aprendiz/`

## Resultado acumulado

| Partida | J1 (fera_basica) | V | J2 (aprendiz) |
|---------|------------------|---|---------------|
| 1,000 | 2 | 998 | 0 |
| 5,000 | 2 | 4,998 | 0 |
| 10,000 | 2 | 9,998 | 0 |

## Evolucao por janela de 1,000 partidas (aprendiz = J2)

| Janela | V | E | D | Aproveitamento |
|--------|---|---|---|---------------|
| 1-1,000 | 0 | 998 | 2 | 99.8% |
| 1,001-2,000 | 0 | 1,000 | 0 | 100% |
| 2,001-3,000 | 0 | 1,000 | 0 | 100% |
| 3,001-4,000 | 0 | 1,000 | 0 | 100% |
| 4,001-5,000 | 0 | 1,000 | 0 | 100% |
| 5,001-6,000 | 0 | 1,000 | 0 | 100% |
| 6,001-7,000 | 0 | 1,000 | 0 | 100% |
| 7,001-8,000 | 0 | 1,000 | 0 | 100% |
| 8,001-9,000 | 0 | 1,000 | 0 | 100% |
| 9,001-10,000 | 0 | 1,000 | 0 | 100% |

Leitura: com o aprendiz em O as perdas sao ainda menores — 2 derrotas, ambas
na primeira janela, e 9,998 empates no total. A partir da partida 1,001 o
resultado e 100% empate em todas as janelas. Nenhuma vitoria: mesmo com
`fera_basica` imperfeito, a politica convergida do agente nao encontra linha
vencedora.

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 7 | 39,997 |

Com epsilon 0 a politica converge para poucas linhas repetidas; exploracao
nova so ocorre em estados nunca visitados.

## Grafico

`progress.svg` — series
`J1 (Fera basica)` / `V` / `J2 (Aprendiz)` por partida. Gerado por
`matplotlib` a partir de `progress.jsonl`.

## Arquivos

```
experiments/learning/rodadas_10000/fera_basica_vs_aprendiz/
├── episodes.jsonl    # cada decisao (estado, acao), resultado, recompensa
├── progress.jsonl    # linha 0 + 1 linha por partida (10,001 linhas)
├── q_table.json      # snapshot da tabela Q (schema_version 1)
├── progress.svg      # grafico acumulado
└── fera_basica_vs_aprendiz.md    # este relatorio
```

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --rounds 10000 --scenario fera_basica_vs_aprendiz
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/rodadas_10000/fera_basica_vs_aprendiz/progress.jsonl \
  --partida 10000
```

Execucao deterministica (seed 42): regenera identico.
