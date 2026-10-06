# Experimento: aprendiz vs aprendiz (100,000 rodadas)

**Configuracao:**
- X (J1): `aprendiz`
- O (J2): `aprendiz`
- Semente: 42
- Rodadas: 100,000
- Recompensa: vitoria +2, empate +1, derrota -5
- epsilon: 0.0 (exploracao apenas pelo desempate aleatorio de estados zerados)

Dados: `experiments/learning/eps0_pes215/rodadas_100000/aprendiz_vs_aprendiz/`

Os dois lados usam a mesma tabela Q, mas os estados de X e de O nao se misturam
(a chave inclui o jogador da vez). Os dois comecam zerados e aprendem ao mesmo
tempo.

## Resultado acumulado

| Partida | J1 (aprendiz) | V | J2 (aprendiz) |
|---------|---------------|---|---------------|
| 1,000 | 10 | 986 | 4 |
| 10,000 | 10 | 9,986 | 4 |
| 50,000 | 10 | 49,986 | 4 |
| 100,000 | 10 | 99,986 | 4 |

## Evolucao por janela de 10,000 partidas

| Janela | J1 | V | J2 |
|--------|----|---|----|
| 1-10,000 | 10 | 9,986 | 4 |
| 10,001-20,000 | 0 | 10,000 | 0 |
| 20,001-30,000 | 0 | 10,000 | 0 |
| 30,001-40,000 | 0 | 10,000 | 0 |
| 40,001-50,000 | 0 | 10,000 | 0 |
| 50,001-60,000 | 0 | 10,000 | 0 |
| 60,001-70,000 | 0 | 10,000 | 0 |
| 70,001-80,000 | 0 | 10,000 | 0 |
| 80,001-90,000 | 0 | 10,000 | 0 |
| 90,001-100,000 | 0 | 10,000 | 0 |

Leitura: as 14 partidas com vencedor sao as 14 primeiras (J1 venceu 10, J2
venceu 4). Da partida 15 ate a 100,000 os dois jogam exatamente a mesma partida
(X nas posicoes 6, 3, 1, 4, 8) e empatam todas. Com epsilon 0, depois que os
dois acham um empate nenhum lado tem motivo para trocar de jogada.

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 82 | 899,982 |

Obs.: `episodes` no `q_table.json` e 200,000 porque o aprendiz registra um
episodio para cada lado em cada partida.

## Grafico

`progress.svg`: series `J1 (Aprendiz)` / `V` / `J2 (Aprendiz)` por partida.
Gerado por `matplotlib` a partir de `progress.jsonl`.

## Arquivos

```
experiments/learning/eps0_pes215/rodadas_100000/aprendiz_vs_aprendiz/
├── episodes.jsonl    # 2 linhas por partida (X e O), decisoes, resultado, recompensa
├── progress.jsonl    # linha 0 + 1 linha por partida (100,001 linhas)
├── q_table.json      # snapshot da tabela Q (schema_version 1)
├── progress.svg      # grafico acumulado
└── aprendiz_vs_aprendiz.md    # este relatorio
```

## Reproduzir e consultar

Rodado antes da troca de pesos para +3/+1/-1. Para reproduzir, voltar
`_RECOMPENSAS_APRENDIZ` para vitoria 2, empate 1, derrota -5.

```bash
.venv/bin/python run_aprendizado.py --rounds 100000 --scenario aprendiz_vs_aprendiz \
  --root experiments/learning/eps0_pes215
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps0_pes215/rodadas_100000/aprendiz_vs_aprendiz/progress.jsonl \
  --partida 100000
```

Execucao deterministica (seed 42): regenera identico.
