# Experimento: treino aprendiz vs ingenuo (1,000,000 rodadas, 2 fases)

**Configuracao:**
- X (J1): `aprendiz`
- O (J2): `ingenuo`
- Semente: 42
- Rodadas: 1,000,000 = **Fase 1 exploracao 500,000 (epsilon 0.25)** +
  **Fase 2 neutralizacao 500,000 (epsilon 0.0)**
- Recompensa: vitoria +2, empate +1, derrota -5
- Objetivo declarado: **zerar as derrotas contra o ingenuo**

Dados: `experiments/learning/eps025_0_pes215/rodadas_500000/treino_aprendiz_vs_ingenuo/`

## Resultado acumulado

| Partida | Fase | epsilon | J1 (aprendiz) | V | J2 (ingenuo) |
|---------|------|---------|---------------|---|--------------|
| 100,000 | exploracao | 0.25 | 90,987 | 5,116 | 3,897 |
| 500,000 | exploracao | 0.25 | 464,920 | 21,383 | 13,697 |
| 600,000 | neutralizacao | 0.0 | 563,906 | 22,397 | 13,697 |
| 1,000,000 | neutralizacao | 0.0 | 959,628 | 26,675 | 13,697 |

## Evolucao por janela de 100,000 partidas (aprendiz = J1)

| Janela | Fase | epsilon | V | E | D | Aproveitamento |
|--------|------|---------|---|---|---|----------------|
| 1-100,000 | exploracao | 0.25 | 90,987 | 5,116 | 3,897 | 96.1% |
| 100,001-200,000 | exploracao | 0.25 | 93,178 | 4,177 | 2,645 | 97.4% |
| 200,001-300,000 | exploracao | 0.25 | 93,546 | 4,017 | 2,437 | 97.6% |
| 300,001-400,000 | exploracao | 0.25 | 93,594 | 4,044 | 2,362 | 97.6% |
| 400,001-500,000 | exploracao | 0.25 | 93,615 | 4,029 | 2,356 | 97.6% |
| 500,001-600,000 | neutralizacao | 0.0 | 98,986 | 1,014 | **0** | **100.0%** |
| 600,001-700,000 | neutralizacao | 0.0 | 98,990 | 1,010 | **0** | **100.0%** |
| 700,001-800,000 | neutralizacao | 0.0 | 98,854 | 1,146 | **0** | **100.0%** |
| 800,001-900,000 | neutralizacao | 0.0 | 98,934 | 1,066 | **0** | **100.0%** |
| 900,001-1,000,000 | neutralizacao | 0.0 | 98,944 | 1,056 | **0** | **100.0%** |

A transicao de epsilon aparece na linha de partida 500,000 (0.25) para
500,001 (0.0) no `progress.jsonl`, com marcador no `progress.svg`.

## Tabela Q final

| Estados | Teto teorico (lado X) | Cobertura | Visitas |
|---------|----------------------|-----------|---------|
| **2,423** | 2,423 | **100%** | 3,401,473 |

O teto e a enumeracao exata de posicoes nao-terminais com X a jogar
(BFS do tabuleiro vazio; 5,478 posicoes alcancaveis no total, 4,520
nao-terminais).

## Grafico

`progress.svg` — series `J1 (Aprendiz)` / `V` / `J2 (Ingenuo)`; a linha
tracejada marca a troca exploracao -> neutralizacao.

## Arquivos

```
experiments/learning/eps025_0_pes215/rodadas_500000/treino_aprendiz_vs_ingenuo/
├── episodes.jsonl    # ~300M — LOCAL, fora do Git (limite 100MB do GitHub)
├── progress.jsonl    # ~185M — LOCAL, fora do Git
├── q_table.json      # versionado
├── progress.svg      # versionado
└── treino_aprendiz_vs_ingenuo.md    # este relatorio (versionado)
```

JSONLs grandes ficam locais e regeneraveis identicos (seed 42).

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --root experiments/learning/eps025_0_pes215 \
  --rounds 500000 --scenario treino_aprendiz_vs_ingenuo
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps025_0_pes215/rodadas_500000/treino_aprendiz_vs_ingenuo/progress.jsonl \
  --partida 1000000
```

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Duas curvas distintas. Na fase de exploracao (epsilon 0.25) as derrotas por
janela caíram de 3,897 para 2,356 e o aproveitamento subiu de 96.1% para
97.6% — ja com o espaco sendo coberto. Na fase de neutralizacao (epsilon 0)
o aproveitamento foi **100.0% em todas as 5 janelas**: 494,708 vitorias,
5,292 empates e **ZERO derrotas em 500,000 partidas**. Total 1M:
959,628V / 26,675E / 13,697D, sendo que as 13,697 derrotas existem
exclusivamente dentro da fase de exploracao.

**Em que trecho do grafico ocorreu a mudanca mais importante?**
Exatamente na particao das fases — partida 500,000 (marcador tracejado no
grafico). Antes dele a linha vermelha (derrotas acumuladas) sobe; depois
ela fica **plana para sempre**, porque nenhuma derrota mais acontece. O
crossing decisivo ocorre na primeira janela apos a troca de epsilon.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Sim — **zerou as derrotas a partir da partida 500,001**, no primeiro lance
da fase com epsilon 0. Nao e apenas "as ultimas 100,000": foram 500,000
partidas sem uma unica derrota (a ultima derrota global foi na partida
499,989, ja no fim da exploracao; nenhuma depois dela). O ingestao de
exploracao com epsilon 0.25 cobriu **100% dos 2,423 estados possiveis do
lado X** — apos isso a politica greedy ja tinha resposta para todo estado e
nao perde mais.

**Depois de observar este resultado, o que voces decidiram testar ou alterar na proxima execucao?**
O protocolo (500k explorando com epsilon 0.25 + 500k neutralizando com
epsilon 0, pesos +2/+1/-5, so contra ingenuo) resolveu o objetivo — manter
como receita. Proximo passo natural: avaliar a mesma politica contra
`fera_basica` (o unico oponente nao coberto pelo treino) para confirmar que
a neutralizacao generaliza alem do ingenuo.
