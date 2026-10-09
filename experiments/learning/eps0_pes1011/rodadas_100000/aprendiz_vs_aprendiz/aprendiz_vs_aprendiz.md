# Experimento: aprendiz vs aprendiz (self-play, 100.000 rodadas)

**Configuracao:**
- X (J1): `aprendiz`
- O (J2): `aprendiz`
- Semente: 42
- Rodadas: 100.000
- Recompensa: vitoria +10, empate +1, derrota -1
- epsilon: 0.0 (exploracao apenas pelo desempate aleatorio de estados zerados)

Dados: `experiments/learning/eps0_pes1011/rodadas_100000/aprendiz_vs_aprendiz/`

## Resultado acumulado

| Partida | J1 (aprendiz X) | V | J2 (aprendiz O) |
|---------|-----------------|---|-----------------|
| 100.000 | 10 | 99.986 | 4 |

Leitura: identico byte a byte ao self-play do baseline eps0_pes215
(10 / 99.986 / 4): com epsilon 0 os dois pesos levam a politica greedy aos
mesmos empates dominantes; a diferenca de recompensa so aparece contra
oponente externo.

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 75 | 899.982 |

## Grafico

`progress.svg` — series `J1 (Aprendiz)` / `V` / `J2 (Aprendiz)` por partida.

## Arquivos

```
experiments/learning/eps0_pes1011/rodadas_100000/aprendiz_vs_aprendiz/
├── episodes.jsonl    # cada decisao (estado, acao), resultado, recompensa
├── progress.jsonl    # linha 0 + 1 linha por partida (100.001 linhas)
├── q_table.json      # snapshot da tabela Q (schema_version 1)
├── progress.svg      # grafico acumulado
└── aprendiz_vs_aprendiz.md    # este relatorio
```

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --rounds 100000 --root experiments/learning/eps0_pes1011
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps0_pes1011/rodadas_100000/aprendiz_vs_aprendiz/progress.jsonl \
  --partida 100000
```
