# Experimento: treino ingenuo vs aprendiz (1,000,000 rodadas, 2 fases)

**Configuracao:**
- X (J1): `ingenuo`
- O (J2): `aprendiz`
- Semente: 42
- Rodadas: 1,000,000 = **Fase 1 exploracao 500,000 (epsilon 0.25)** +
  **Fase 2 neutralizacao 500,000 (epsilon 0.0)**
- Recompensa: vitoria +2, empate +1, derrota -5
- Objetivo declarado: **zerar as derrotas contra o ingenuo**

Dados: `experiments/learning/eps025_0_pes215/rodadas_500000/treino_ingenuo_vs_aprendiz/`

## Resultado acumulado

| Partida | Fase | epsilon | J1 (ingenuo) | V | J2 (aprendiz) |
|---------|------|---------|--------------|---|---------------|
| 100,000 | exploracao | 0.25 | 13,510 | 13,731 | 72,759 |
| 500,000 | exploracao | 0.25 | 57,334 | 68,070 | 374,596 |
| 600,000 | neutralizacao | 0.0 | 57,334 | 78,245 | 464,421 |
| 1,000,000 | neutralizacao | 0.0 | 57,334 | 118,874 | 823,792 |

Repare: os totais de J1 (derrotas do aprendiz) **travam em 57,334 a partir
da partida 500,000** — nenhuma derrota nova e somada na fase 2.

## Evolucao por janela de 100,000 partidas (aprendiz = J2)

| Janela | Fase | epsilon | V | E | D | Aproveitamento |
|--------|------|---------|---|---|---|----------------|
| 1-100,000 | exploracao | 0.25 | 72,759 | 13,731 | 13,510 | 86.5% |
| 100,001-200,000 | exploracao | 0.25 | 75,290 | 13,604 | 11,106 | 88.9% |
| 200,001-300,000 | exploracao | 0.25 | 75,299 | 13,532 | 11,169 | 88.8% |
| 300,001-400,000 | exploracao | 0.25 | 75,546 | 13,614 | 10,840 | 89.2% |
| 400,001-500,000 | exploracao | 0.25 | 75,702 | 13,589 | 10,709 | 89.3% |
| 500,001-600,000 | neutralizacao | 0.0 | 89,825 | 10,175 | **0** | **100.0%** |
| 600,001-700,000 | neutralizacao | 0.0 | 89,834 | 10,166 | **0** | **100.0%** |
| 700,001-800,000 | neutralizacao | 0.0 | 89,838 | 10,162 | **0** | **100.0%** |
| 800,001-900,000 | neutralizacao | 0.0 | 89,869 | 10,131 | **0** | **100.0%** |
| 900,001-1,000,000 | neutralizacao | 0.0 | 89,830 | 10,170 | **0** | **100.0%** |

A transicao de epsilon aparece da partida 500,000 (0.25) para 500,001
(0.0) no `progress.jsonl`, com marcador no `progress.svg`.

## Tabela Q final

| Estados | Teto teorico (lado O) | Cobertura | Visitas |
|---------|----------------------|-----------|---------|
| **2,097** | 2,097 | **100%** | 3,323,852 |

Teto = enumeracao exata de posicoes nao-terminais com O a jogar (BFS do
tabuleiro vazio; 5,478 posicoes alcancaveis no total, 4,520 nao-terminais).

## Grafico

`progress.svg` — series `J1 (Ingenuo)` / `V` / `J2 (Aprendiz)`; a linha
tracejada marca a troca exploracao -> neutralizacao.

## Arquivos

```
experiments/learning/eps025_0_pes215/rodadas_500000/treino_ingenuo_vs_aprendiz/
├── episodes.jsonl    # ~300M — LOCAL, fora do Git (limite 100MB do GitHub)
├── progress.jsonl    # ~185M — LOCAL, fora do Git
├── q_table.json      # versionado
├── progress.svg      # versionado
└── treino_ingenuo_vs_aprendiz.md    # este relatorio (versionado)
```

JSONLs grandes ficam locais e regeneraveis identicos (seed 42).

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --root experiments/learning/eps025_0_pes215 \
  --rounds 500000 --scenario treino_ingenuo_vs_aprendiz
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps025_0_pes215/rodadas_500000/treino_ingenuo_vs_aprendiz/progress.jsonl \
  --partida 1000000
```

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Na exploracao (epsilon 0.25) o aproveitamento subiu de 86.5% para 89.3%,
com derrotas por janela caindo de 13,510 para 10,709 — o lado J2, sempre o
mais dificil, ja melhorava com o espaco sendo coberto. Na neutralizacao
(epsilon 0) o resultado virou **100.0% em todas as 5 janelas**: 449,196
vitorias, 50,804 empates e **ZERO derrotas em 500,000 partidas**. Total 1M:
823,792V / 118,874E / 57,334D — e a contagem de derrotas congela em 57,334
exatamente na partida 500,000.

**Em que trecho do grafico ocorreu a mudanca mais importante?**
Na particao das fases, partida 500,000 (marcador tracejado). A linha de
derrotas acumuladas sobe durante toda a exploracao e **para de subir
bruscamente ali** — depois do marcador ela e uma reta horizontal ate o fim.
Segundo momento: entre as janelas 1 e 2 da exploracao (+2.4pp), quando a
cobertura comeca a valer.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Sim — **zerou as derrotas a partir da partida 500,001**. A ultima derrota
foi na partida **499,992**, ultimo lote da fase de exploracao; nas 500,000
partidas seguintes o ingenuo nao venceu uma unica vez. Como J2 isso e
particularmente forte: era o lado que perdia 9.5% das partidas nos
experimentos antigos. A cobertura terminou em **100% dos 2,097 estados
possiveis do lado O**.

**Depois de observar este resultado, o que voces decidiram testar ou alterar na proxima execucao?**
Receita confirmada nos dois lados: 500k explorando (epsilon 0.25) + 500k
neutralizando (epsilon 0), pesos +2/+1/-5, so contra ingenuo. Proximo passo:
avaliar a mesma politica contra `fera_basica` para ver se a neutralizacao
generaliza — hoje ela so foi provada contra o ingenuo.
