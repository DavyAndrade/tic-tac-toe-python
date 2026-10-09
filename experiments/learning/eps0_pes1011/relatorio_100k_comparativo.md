# Relatorio comparativo 100k — pesos 10/1/−1 vs baseline 2/1/−5 (epsilon 0)

**Experimento:** `eps0_pes1011` — recompensa vitoria +10, empate +1, derrota −1,
epsilon 0.0, 100.000 rodadas, seed 42. Ideia testada: bônus de vitória alto faz o
guloso "explorar um ramo por mais tempo" (Q das linhas vencedoras inflado).

**Baseline:** `eps0_pes215/rodadas_100000` — vitoria +2, empate +1, derrota −5,
epsilon 0.0, mesmas 100.000 rodadas, seed 42.

Escopo: apenas `aprendiz_vs_ingenuo` e `ingenuo_vs_aprendiz`.

Dados: `experiments/learning/eps0_pes1011/rodadas_100000/`

## Resultado direto (100k, aprendiz em negrito)

| Confronto | baseline 2/1/−5 | experimento 10/1/−1 |
|-----------|-----------------|---------------------|
| `aprendiz_vs_ingenuo` (J1) | **82.513V** / 16.018E / 1.469D (82,5% — sem derrota 98,5%) | **73.234V** / 14.078E / 12.688D (73,2% — sem derrota 87,3%) |
| `ingenuo_vs_aprendiz` (J2) | **59.969V** / 29.871E / 10.160D (60,0%) | **47.012V** / 23.431E / 29.557D (47,0%) |

Estados na tabela Q: 220 (10/1/−1) vs 300 (baseline) em `aprendiz_vs_ingenuo`.

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Plano do inicio ao fim nas duas configs (epsilon 0 converge antes da partida
10.000): baseline 82,0%→82,5% de vitorias, experimento 72,8%→73,2%. O deficit
do 10/1/−1 nasce cedo e nunca fecha — ~1.250 derrotas por janela de 10 mil ate
a partida 100.000, contra ~140 do baseline.

**Em que trecho do grafico ocorreu a mudanca mais importante?**
Nenhuma — variacao entre janelas < 1,5pp nas duas configs. A diferenca entre os
pesos e um deslocamento de nivel (~9pp de vitoria, ~8,6x derrotas), formado
nas primeiras 10 mil partidas, não um evento tardio.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Nao. Ultima derrota na partida 99.997 com 12.688D no total. O baseline tambem
nao zerou em 100k (1.469D), mas perdeu 8,6x menos.

**Depois de observar este resultado, o que voces decidiram testar ou alterar na proxima execucao?**
Hipotese "bônus alto = persiste no ramo" nao se confirmou: inflar a vitoria para
+10 e desinflar a derrota para −1 removeu a aversao a risco do baseline — quase
toda linha vencedora termina com Q ~7-9 (discriminação diluida, empate aleatorio
em empates tecnicos) e linhas com derrota ocasional custam so −1, entao o agente
as aceita. Manter 2/1/−5 como pesos campeoes. Se o objetivo continuar "persistir
mais tempo em um ramo", a alavanca que funcionou foi o curriculo epsilon
(`eps025_0_pes215`, 0 derrotas na fase2) — nao o peso da recompensa.

## Proximo experimento sugerido

1. Nenhum em pesos puros: 3/1/−1, 4/2/−4, 10/1/−1 perderam todos para 2/1/−5.
2. Se insistir em recompensa: variar só a fase de exploracao do curriculo
   (ex.: pesos 10/1/−1 só na fase exploracao, trocar para 2/1/−5 na neutralizacao)
   para medir se o bônus alto ajuda a descoberta sem poluir a politica final.

## Masterização da árvore — validação da ideia

Ideia: os pesos de recompensa devem fazer o guloso permanecer numa árvore e
masterizá-la, em vez de ir para outra e recomeçar a exploração. Medido nos
`episodes.jsonl` / `q_table.json` dos dois lados (aprendiz_vs_ingenuo, 100k):

| Métrica | 2/1/−5 (baseline) | 10/1/−1 |
|---------|-------------------|---------|
| Abertura usada | canto0 em 100% dos jogos | canto0 em 100% dos jogos |
| Migrações de abertura (jogada 1 muda) | 0 em 99.999 | 0 em 99.999 |
| Estados distintos explorados | 300 | 220 |
| Distribuição por ply (0/2/4/6/8 marcas) | 1 / 8 / 64 / 158 / 69 | 1 / 8 / 43 / 115 / 53 |
| 2ª jogada do X (células distintas) | 8 (1,2,3,4,5,6,7,8) | 4 (2,4,6,8) |
| Estados com todas as ações testadas | 80/300 (27%) | 55/220 (25%) |
| Primeiros-aparecimentos por janela | 300 na janela 0, **+0 nas 9 seguintes** | 220 na janela 0, **+0 nas 9 seguintes** |
| Aproveitamento (V+E) | 98,5% | 87,3% |

Leitura:

1. **A pegada na árvore já é estrutural, não vem da recompensa.** Com epsilon 0
   e política gulosa, as duas configurações ficam 100% na mesma abertura, com
   0 migrações, e fecham toda a exploração na primeira janela de 10 mil jogos —
   depois disso nenhum estado novo aparece em nenhuma das duas. O cenário temido
   ("ir para outra árvore e começar a explorar tudo de novo") **nunca ocorre**.
2. **O peso 10/1/−1 estreita a exploração sem ganhar nada:** menos estados
   (220 vs 300), menos ramos na 2ª jogada (4 vs 8 células), mesmo grau de
   saturação (~26%), porém 9pp a menos de vitórias. Masterizou menos, não mais.
3. **Conclusão:** parâmetros de recompensa não são a alavanca de persistência
   em árvore aqui — a persistência já vem do guloso + epsilon 0. Os pesos só
   decidem quão largo é o explorado dentro da árvore, e 2/1/−5 achou os ramos
   que vencem mais. Ideia validada como *não necessária* neste arranjo; se o
   objetivo for variar a largura da exploração dentro da árvore, 10/1/−1 é o
   knob (mais estreito), mas até agora sempre com desempenho pior.

## Execucao de 500k (mesmo config)

`rodadas_500000/aprendiz_vs_ingenuo/`: **368.694V / 69.192E / 62.114D**
(73,7% de vitorias, 87,6% sem derrota) — identico em taxa ao 100k (73,2% /
87,3%), planissimo janela a janela (87,2–87,9%), **mesmos 220 estados na
tabela Q** (zero crescimento em 400k partidas extras), 0 migracoes, ultima
derrota p499.998. Confirma em escala: o gap para o baseline e estrutural na
recompensa, nao de amostragem.

## Comandos

```bash
# regenerar apenas o confronto (identico, seed 42)
.venv/bin/python run_aprendizado.py --rounds 100000 \
  --scenario aprendiz_vs_ingenuo --root experiments/learning/eps0_pes1011
# consulta pontual
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps0_pes1011/rodadas_100000/aprendiz_vs_ingenuo/progress.jsonl \
  --partida 100000
```
