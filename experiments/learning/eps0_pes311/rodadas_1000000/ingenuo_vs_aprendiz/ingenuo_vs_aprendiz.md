# Experimento: ingenuo vs aprendiz (1,000,000 rodadas)

**Configuracao:**
- X (J1): `ingenuo`
- O (J2): `aprendiz`
- Semente: 42
- Rodadas: 1,000,000
- Recompensa: **vitoria +3, empate +1, derrota -1** (variante `pesos311`)
- epsilon: 0.0 (padrao; exploracao so pelo desempate aleatorio de estados zerados)

Dados: `experiments/learning/eps0_pes311/rodadas_1000000/ingenuo_vs_aprendiz/`

## Resultado acumulado

| Partida | J1 (ingenuo) | V | J2 (aprendiz) |
|---------|--------------|---|---------------|
| 200,000 | 43,756 | 49,513 | 106,731 |
| 600,000 | 129,894 | 147,971 | 322,135 |
| 1,000,000 | 216,299 | 247,032 | 536,669 |

## Evolucao por janela de 200,000 partidas (aprendiz = J2)

| Janela | V | E | D | Aproveitamento |
|--------|---|---|---|----------------|
| 1-200,000 | 106,731 | 49,513 | 43,756 | 78.1% |
| 200,001-400,000 | 107,275 | 49,451 | 43,274 | 78.4% |
| 400,001-600,000 | 108,129 | 49,007 | 42,864 | 78.6% |
| 600,001-800,000 | 107,328 | 49,644 | 43,028 | 78.5% |
| 800,001-1,000,000 | 107,206 | 49,417 | 43,377 | 78.3% |

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 807 | 3,468,999 |

## Grafico

`progress.svg` — series `J1 (Ingenuo)` / `V` / `J2 (Aprendiz)`; gerado por
`matplotlib` a partir de `progress.jsonl`.

## Arquivos

```
experiments/learning/eps0_pes311/rodadas_1000000/ingenuo_vs_aprendiz/
├── episodes.jsonl    # ~300M — LOCAL, fora do Git (limite 100MB do GitHub)
├── progress.jsonl    # ~185M — LOCAL, fora do Git
├── q_table.json      # versionado
├── progress.svg      # versionado
└── ingenuo_vs_aprendiz.md    # este relatorio (versionado)
```

JSONLs grandes ficam locais e regeneraveis identicos (seed 42).

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --root experiments/learning/eps0_pes311 \
  --rounds 1000000 --scenario ingenuo_vs_aprendiz
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps0_pes311/rodadas_1000000/ingenuo_vs_aprendiz/progress.jsonl \
  --partida 1000000
```

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Plano e abaixo do baseline: aproveitamento entre 77.9% e 78.7% em todos os
blocos de 200 mil. Vitorias ~107 mil/bloco, empates ~49 mil/bloco, derrotas
~21,5 mil/bloco — nenhuma tendencia de melhora. Baseline +2/+1/-5 na mesma
rodada: 90.5% de aproveitamento e 602,014 vitorias contra 536,669 aqui; o
agente com pesos novos sofreu ~65,000 derrotas a mais (216,299 vs 95,783).

**Em que trecho do gráfico ocorreu a mudanca mais importante?**
Nenhuma mudanca real: maior variacao +0.5pp entre o 1o e 2o bloco. O grafico
e uma reta horizontal — o modelo aprendeu (ou fixou) tudo antes da partida
200,000.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Nao. ~21,400-22,100 derrotas por bloco de 200 mil (21.6% das partidas) do
inicio ao fim; ultima derrota na partida 999,996. Com os pesos antigos as
derrotas ja eram ~9,500/bloco (9.5%) — o tolerancia a risco do +3/-1 quase
dobrou a taxa de derrota e ela nao cai com treino.

**O que voces decidiram testar ou alterar na proxima execucao?**
Reverter para +2/+1/-5 (melhor em todas as metricas) e testar epsilon
pequeno (ex. 0.01): com epsilon 0 a tabela ficou presa em 807 estados
(1,070 no baseline) e nenhum volume de partidas novou conhecimento —
exploracao, nao quantidade de rodadas, e o gargalo.
