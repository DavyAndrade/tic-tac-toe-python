# Relatório consolidado — campanha de 1M de rodadas: do primeiro milhão até zerar as derrotas

Data: 2026-10-06 · Semente: 42 em todos · Agente: `aprendiz` vs `ingenuo`, nos dois lados
(J1 = aprendiz joga X · J2 = aprendiz joga O)

Este relatório agrega **todos** os experimentos de 1M feitos nesta campanha,
do baseline inicial até o resultado final atual (0 derrotas).

## 1. Resposta final primeiro

> **O aprendiz neutralizou o ingênuo: 0 derrotas em 500.000 partidas de cada
> lado (Fase 2 do treino em duas fases), com 100% de cobertura do espaço de
> estados possível.**

Protocolo vencedor: **500k explorando (ε=0,25) + 500k neutralizando (ε=0)**,
pesos **+2/+1/−5**, oponente apenas `ingenuo`, tudo num único run por lado.

| | Fase 1 (ε=0,25) | Fase 2 (ε=0) |
|---|---|---|
| Aprendiz J1 | derrotas 3.897 → 2.356 por janela de 100k | **494.708V / 5.292E / 0D = 100,00%** |
| Aprendiz J2 | derrotas 13.510 → 10.709 por janela de 100k | **449.196V / 50.804E / 0D = 100,00%** |
| Última derrota | p499.989 (J1) · p499.992 (J2) | nenhuma |

## 2. Cronologia — todos os experimentos de 1M

| # | Experimento | Config | J1: aproveit. (derrotas) | J2: aproveit. (derrotas) | Estados Q (J1 / J2) |
|---|---|---|---|---|---|
| 1 | `eps0_pes215/rodadas_1000000` | ε=0, pesos +2/+1/−5 | 98,7% (13.207) | 90,5% (95.783) | 300 / 1.070 |
| 2 | `eps0_pes311/rodadas_1000000` | ε=0, pesos +3/+1/−1 | 88,2% (118.228) | 78,3% (216.299) | 221 / 807 |
| 3 | `eps0_pes424/rodadas_1000000` | ε=0, pesos +4/+2/−4 | 94,4% (55.777) | 88,6% (114.175) | 233 / 1.064 |
| 4 | **`eps025_0_pes215/rodadas_500000`** | **ε=0,25→0, pesos +2/+1/−5** | **100% (0) na fase 2** | **100% (0) na fase 2** | **2.423 / 2.097 = 100% do teto** |

Contexto imediatamente anterior (não-1M, mesma campanha): baseline ε=0,1 em
100k já tinha mostrado J1 98,1% (94,5% de vitórias) com **2.282 estados**,
enquanto ε=0 em 100k/1M travava a Q em 300/1.070 — foi essa contradição que
abriu toda a investigação.

## 3. A grande descoberta: o gargalo era exploração, não volume

O experimento 1 provou: **10x mais partidas com ε=0 não movem nada** — as
10 janelas de 100k ficam planas em 98,7% (J1) e 90,5% (J2), e a tabela Q
termina com **os mesmos 300 / 1.070 estados** dos 100k. O prefixo de 100k do
1M é byte-idêntico ao experimento de 100k (mesma cadeia de seeds).

Especificação numérica do espaço (enumeração exata, BFS do tabuleiro vazio):

| Espaço | Estados |
|---|---|
| `3^9` brutos | 19.683 |
| Alcançáveis em jogo legal | 5.478 |
| Terminais (942 vitórias + 16 cheios sem vencedor) | 958 |
| Não-terminais = teto total da Q | 4.520 |
| **Teto lado X (aprendiz como J1)** | **2.423** |
| **Teto lado O (aprendiz como J2)** | **2.097** |

Com ε=0, o agente ocupava **12%** do teto X e **51%** do teto O. Com ε=0,1
(histórico) tinha chegado a 94% do teto X — sinal de que o espaço era
alcançável, só faltava visitingá-lo.

## 4. Teste de pesos: quanto cada recompensa rendeu (1M, ε=0)

Hipótese: o −5 da derrota tornava o agente conservador demais (linha de
empate valia quase tanto quanto vencer; risco só valia a pena com p>85,7%).

| Pesos (V/E/D) | Limite p/ preferir risco | J1 | J2 | Veredito |
|---|---|---|---|---|
| **+2 / +1 / −5** | p > 85,7% | **98,7%** | **90,5%** | **campeão — mantido** |
| +4 / +2 / −4 | p > 75% | 94,4% | 88,6% | meio-termo, descartado |
| +3 / +1 / −1 | p > 50% | 88,2% | 78,3% | pior nos dois lados, descartado |

Resultado contra a intuição: **mais tolerância a risco piorou tudo** — menos
estados visitados e derrotas 4x maiores. O −5 não era um bug, era a proteção
que mantinha o agente em linhas seguras. Pesos voltaram pra +2/+1/−5
(histórico completo em `AGENTS.md`; cada variante preservada no seu diretório).

## 5. A receita final: exploração pesada e depois neutração

Fase 1 com ε=0,25 por 500k gera cobertura total; a recompensa −5 punindo os
blunders aleatórios, somada a 500k amostras, deixa a Q com média confiável
em **todos** os estados. Fase 2 com ε=0 transforma isso em política greed
que não erra mais contra o ingênuo:

```
experiments/learning/eps025_0_pes215/rodadas_500000/
├── treino_aprendiz_vs_ingenuo/   J1: 2.423/2.423 estados (100%)
└── treino_ingenuo_vs_aprendiz/   J2: 2.097/2.097 estados (100%)
```

Cada um com 1.000.001 linhas de progresso (coluna `epsilon` registra a
transição na partida 500.000/500.001, marcada no SVG), `q_table.json`,
`progress.svg` e relatório próprio com as 4 perguntas.

## 6. Gráfico da caminhada (aproveitamento por lado, 1M)

```
J1 (aprendiz como X)
  98,7  ██ baseline ε=0 (platô, 13k derrotas)
  94,4  ███ pesos 4/2/−4
  88,2  ████ pesos 3/1/−1
 100,0  ██ fase 2 do treino ε 0,25→0  ← 0 derrotas

J2 (aprendiz como O)
  90,5  ███ baseline ε=0 (platô, 96k derrotas)
  88,6  ███ pesos 4/2/−4
  78,3  █████ pesos 3/1/−1
 100,0  ██ fase 2 do treino ε 0,25→0  ← 0 derrotas
```

## 7. Conclusao e proximo passo

- Quantidade de rodadas sozinha não resolve: ε=0 platou; **exploração +**
  volume resolveu (ε=0,25 → 100% de cobertura → ε=0 → 0 derrotas).
- Pesos conservadores (+2/+1/−5) ganharam dos "otimistas" — mantidos como
  padrão.
- A receita está codificada: cenários `treino_*` (ε por fase via
  `configurar_epsilon`), replicável a qualquer rodada.
- **Pendência:** a neutralização só foi provada contra `ingenuo`. Avaliar a
  mesma política (os `q_table.json` já treinados) contra `fera_basica` é o
  próximo passo — sem retreino, só avaliação com ε=0.

## 8. Onde vive cada coisa

```
experiments/learning/
├── eps0-1_pes215/   baseline histórico ε=0,1 (1k e 100k)
├── eps0_pes215/     ε=0 pesos 2/1/−5: 1k, 10k, 100k, 1M (experimentos 1)
├── eps0_pes311/     ε=0 pesos 3/1/−1: 1M (experimento 2)
├── eps0_pes424/     ε=0 pesos 4/2/−4: 1M (experimento 3)
├── eps025_0_pes215/ treino 2 fases: 1M por lado (experimento 4 — final)
└── relatorio_1M_consolidado.md  (este arquivo)
```

JSONLs de 500k+ rodadas ficam locais (limite de 100MB do GitHub) e são
regeneráveis identicos por seed 42; relatórios, `q_table.json` e SVGs estão
versionados. Todos os relatórios por experimento vivem dentro da pasta do
respectivo experimento e respondem as mesmas 4 perguntas.

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Dependeu do epsilon, nao do volume. Nas variantes epsilon 0 puras (1M cada)
o desempenho foi plano do primeiro ao ultimo bloco: J1 em 98,7% (13,207
derrotas distribuidas em ~1,300 por janela de 100k, de 1,469 na primeira
para 1,280 na ultima) e J2 em 90,5% (95,783 derrotas, ~9,500 por janela sem
tendencia de queda) — 10x de partidas nao mudaram vitorias, empates nem
derrotas. Com pesos testados (+3/+1/−1 e +4/+2/−4) piorou: 118,228 e 55,777
derrotas no lado J1, 216,299 e 114,175 no J2. A inversao so veio com o
treino em duas fases: na exploracao (epsilon 0.25, 500k) as derrotas por
janela caíram de 3,897 para 2,356 (J1) e de 13,510 para 10,709 (J2), com
aproveitamento subindo de 96.1% para 97.6% e de 86.5% para 89.3%; na
neutralizacao (epsilon 0, 500k) virou **100.0% dos dois lados — 494,708V /
5,292E / 0D em J1 e 449,196V / 50,804E / 0D em J2**.

**Em que trecho do grafico ocorreu a mudanca mais importante?**
Na partida 500,000 do treino — o marcador de troca epsilon 0.25 -> 0. Ate
la a linha de derrotas acumuladas sobe em todas as variantes; depois dela
ela fica **plana ate a partida 1,000,000** (e fica plana nas duas series, J1
e J2). Nos graficos das variantes epsilon 0 puras nao ha mudanca nenhuma:
retas do comeco ao fim, o maior delta entre janelas foi +0.2pp (ruido). O
crossing decisivo acontece na primeira janela apos o marcador.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Sim — em todos os experimentos anteriores ele **nunca** parou (13,207 a
95,783 derrotas por milhao, ultima derrota sempre na casa dos 999 mil). No
treino final ele zerou **a partir da partida 500,001**, ou seja, depois de
**500,000 partidas de exploracao** (epsilon 0.25): a ultima derrota de J1
foi na partida **499,989** e a de J2 na **499,992**; nas 500,000 partidas
seguintes, nenhuma derrota de nenhum lado. O ponto de virada foi atingir
100% da cobertura (2,423/2,423 estados X e 2,097/2,097 estados O) ainda na
fase de exploracao — depois disso a politica greed ja tinha resposta para
qualquer estado que o ingenuo apresentasse.

**Depois de observar este resultado, o que voces decidiram testar ou alterar na proxima execucao?**
A receita (500k epsilon 0.25 + 500k epsilon 0, pesos +2/+1/−5, so contra
ingenuo) resolveu a meta e fica congelada como padrao — pesos e volume saem
da agenda, os comparativos de variantes ja mostraram que nao ajudam. Proximo
passo: **avaliar sem retreino** a politica ja treinada (os `q_table.json`
existentes) contra `fera_basica`, com epsilon 0, para descobrir se a
neutralizacao generaliza alem do oponente de treino. Se falhar la, o
candidato seguinte e incluir fera_basica dentro da fase de exploracao.
