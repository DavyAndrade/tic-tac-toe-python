# Relatorio comparativo 100k — pesos 10/1/−1 vs baseline 2/1/−5 (epsilon 0)

**Experimento:** `eps0_pes1011` — recompensa vitoria +10, empate +1, derrota −1,
epsilon 0.0, 100.000 rodadas, seed 42. Ideia testada: bônus de vitória alto faz o
guloso "explorar um ramo por mais tempo" (Q das linhas vencedoras inflado).

**Baseline:** `eps0_pes215/rodadas_100000` — vitoria +2, empate +1, derrota −5,
epsilon 0.0, mesmas 100.000 rodadas, seed 42.

Dados: `experiments/learning/eps0_pes1011/rodadas_100000/`

## Resultado direto (100k, aprendiz em negrito)

| Confronto | baseline 2/1/−5 | experimento 10/1/−1 |
|-----------|-----------------|---------------------|
| `aprendiz_vs_ingenuo` (J1) | **82.513V** / 16.018E / 1.469D (82,5% — sem derrota 98,5%) | **73.234V** / 14.078E / 12.688D (73,2% — sem derrota 87,3%) |
| `ingenuo_vs_aprendiz` (J2) | **59.969V** / 29.871E / 10.160D (60,0%) | **47.012V** / 23.431E / 29.557D (47,0%) |
| `aprendiz_vs_aprendiz` (self-play) | 10 / 99.986 / 4 | 10 / 99.986 / 4 — **identico** |
| `aprendiz_vs_fera_basica` (J1) | 9.994V / 6D @10k (99,94%) | **99.994V** / 6D @100k (99,99%) |
| `fera_basica_vs_aprendiz` (J2) | 9.998V / 2D @10k (100%) | **99.998V** / 2D @100k (100%) |
| `treino_*` fase2 (`neutralizacao`) | 0 derrotas nos dois lados (500k/fase) | J1: 0D, mas **J2: 4.179D** (100k/fase) |

Estados na tabela Q: 220 (10/1/−1) vs 300 (baseline) em `aprendiz_vs_ingenuo`.

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Plano do inicio ao fim nas duas configs (epsilon 0 converge antes da partida
10.000): baseline 82,0%→82,5% de vitorias, experimento 72,8%→73,2%. O deficit
do 10/1/−1 nasce cedo e nunca fecha — ~1.250 derrotas por janela de 10 mil ate
a partida 100.000, contra ~140 do baseline.

**Em que trecho do grafico ocorreu a mudanca mais importante?**
Nenhuma — variacao entre janelas < 1pp nas duas configs. A diferenca entre os
pesos e um deslocamento de nivel (~9pp de vitoria, ~8,6x derrotas), formado
nas primeiras 10 mil partidas, não um evento tardio.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Nao. Ultima derrota na partida 99.997 com 12.688D no total. O baseline tambem
nao zerou em 100k (1.469D), mas perdeu 8,6x menos. Os unicos rodelos que zeraram
derrotas foram os de curriculo `treino_*` com a fase2 — e so o lado J1 zerou
com 10/1/−1 (J2 ficou com 4.179D, contra 0D do baseline 2/1/−5 em 500k/fase).

**Depois de observar este resultado, o que voces decidiram testar ou alterar na proxima execucao?**
Hipotese "bônus alto = persiste no ramo" nao se confirmou: inflar a vitoria para
+10 e desinflar a derrota para −1 removeu a aversao a risco do baseline — quase
toda linha vencedora termina com Q ~7-9 (discriminação diluida, empate aleatorio
em empates tecnicos) e linhas com derrota ocasional custam so −1, entao o agente
as aceita. Manter 2/1/−5 como pesos campeoes. Se o objetivo continuar "persistir
mais tempo em um ramo", a alavanca que funcionou foi o curriculo epsilon
(0.25→0, `eps025_0_pes215`, 0 derrotas na fase2) — nao o peso da recompensa.

## Proximo experimento sugerido

1. Nenhum em pesos puros: 3/1/−1, 4/2/−4, 10/1/−1 perderam todos para 2/1/−5.
2. Se insistir em recompensa: variar só a fase de exploracao do curriculo
   (ex.: pesos 10/1/−1 só na fase exploracao, trocar para 2/1/−5 na neutralizacao)
   para medir se o bônus alto ajuda a descoberta sem poluir a politica final.

## Comandos

```bash
# regenerar (identico, seed 42)
.venv/bin/python run_aprendizado.py --rounds 100000 --root experiments/learning/eps0_pes1011
# consulta pontual
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps0_pes1011/rodadas_100000/aprendiz_vs_ingenuo/progress.jsonl \
  --partida 100000
```
