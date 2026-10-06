# Experimento: ingenuo vs aprendiz

**Configuracao:**
- X (J1): `ingenuo`
- O (J2): `aprendiz`
- Semente: 42
- Rodadas: 1,000
- Recompensa: vitoria +2, empate +1, derrota -5
- epsilon: 0.0 (exploracao apenas pelo desempate aleatorio de estados zerados)

Dados: `experiments/learning/rodadas_1000_eps0/ingenuo_vs_aprendiz/`

## Resultado acumulado

| Partida | J1 (ingenuo) | V | J2 (aprendiz) |
|---------|--------------|---|---------------|
| 100 | 55 | 19 | 26 |
| 500 | 223 | 87 | 190 |
| 1,000 | 370 | 197 | 433 |

## Evolucao por janela de 100 partidas (aprendiz = J2)

| Janela | V | E | D | Aproveitamento |
|--------|---|---|---|----------------|
| 1-100 | 26 | 19 | 55 | 45% |
| 101-200 | 34 | 16 | 50 | 50% |
| 201-300 | 42 | 16 | 42 | 58% |
| 301-400 | 44 | 20 | 36 | 64% |
| 401-500 | 44 | 16 | 40 | 60% |
| 501-600 | 46 | 19 | 35 | 65% |
| 601-700 | 46 | 23 | 31 | 69% |
| 701-800 | 56 | 21 | 23 | 77% |
| 801-900 | 51 | 22 | 27 | 73% |
| 901-1000 | 44 | 25 | 31 | 69% |

Leitura: como segundo jogador o aprendizado e mais lento — comeca em 45%
(inferior ao ingenuo puro) e chega a ~70% ate a partida 1,000. Nesta amostra
curta, epsilon 0 fica atras da versao epsilon 0.1 (56% no total daquela
versao); a amostra de 100k e a referencia confiavel.

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 905 | 3,507 |

## Grafico

`progress.svg` — series `J1 (Ingenuo)` /
`V` / `J2 (Aprendiz)` por partida. Gerado por `matplotlib` a partir de
`progress.jsonl`.

## Arquivos

```
experiments/learning/rodadas_1000_eps0/ingenuo_vs_aprendiz/
├── episodes.jsonl    # cada decisao (estado, acao), resultado, recompensa
├── progress.jsonl    # linha 0 + 1 linha por partida (1,001 linhas)
├── q_table.json      # snapshot da tabela Q (schema_version 1)
├── progress.svg      # grafico acumulado
└── ingenuo_vs_aprendiz.md    # este relatorio
```

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --rounds 1000 --scenario ingenuo_vs_aprendiz --variant eps0
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/rodadas_1000_eps0/ingenuo_vs_aprendiz/progress.jsonl \
  --partida 1000
```

Execucao deterministica (seed 42): regenera identico com `--variant eps0`;
a versao epsilon 0.1 esta preservada no diretorio sem sufixo (`rodadas_<N>/`).
