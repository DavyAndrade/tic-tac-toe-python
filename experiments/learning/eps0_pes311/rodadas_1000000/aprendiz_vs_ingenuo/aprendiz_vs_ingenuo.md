# Experimento: aprendiz vs ingenuo (1,000,000 rodadas)

**Configuracao:**
- X (J1): `aprendiz`
- O (J2): `ingenuo`
- Semente: 42
- Rodadas: 1,000,000
- Recompensa: **vitoria +3, empate +1, derrota -1** (variante `pesos311`)
- epsilon: 0.0 (padrao; exploracao so pelo desempate aleatorio de estados zerados)

Dados: `experiments/learning/eps0_pes311/rodadas_1000000/aprendiz_vs_ingenuo/`

## Resultado acumulado

| Partida | J1 (aprendiz) | V | J2 (ingenuo) |
|---------|---------------|---|--------------|
| 200,000 | 147,859 | 27,925 | 24,216 |
| 600,000 | 446,047 | 82,926 | 71,027 |
| 1,000,000 | 743,939 | 137,833 | 118,228 |

## Evolucao por janela de 200,000 partidas (aprendiz = J1)

| Janela | V | E | D | Aproveitamento |
|--------|---|---|---|----------------|
| 1-200,000 | 147,859 | 27,925 | 24,216 | 87.9% |
| 200,001-400,000 | 149,034 | 27,427 | 23,539 | 88.2% |
| 400,001-600,000 | 149,154 | 27,574 | 23,272 | 88.4% |
| 600,001-800,000 | 148,790 | 27,482 | 23,728 | 88.1% |
| 800,001-1,000,000 | 149,102 | 27,425 | 23,473 | 88.3% |

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 221 | 4,047,736 |

## Grafico

`progress.svg` — series `J1 (Aprendiz)` / `V` / `J2 (Ingenuo)`; gerado por
`matplotlib` a partir de `progress.jsonl`.

## Arquivos

```
experiments/learning/eps0_pes311/rodadas_1000000/aprendiz_vs_ingenuo/
├── episodes.jsonl    # ~316M — LOCAL, fora do Git (limite 100MB do GitHub)
├── progress.jsonl    # ~185M — LOCAL, fora do Git
├── q_table.json      # versionado
├── progress.svg      # versionado
└── aprendiz_vs_ingenuo.md    # este relatorio (versionado)
```

JSONLs grandes ficam locais e regeneraveis identicos (seed 42).

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --root experiments/learning/eps0_pes311 \
  --rounds 1000000 --scenario aprendiz_vs_ingenuo
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps0_pes311/rodadas_1000000/aprendiz_vs_ingenuo/progress.jsonl \
  --partida 1000000
```

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Nao melhorou: aproveitamento ficou em 87.9-88.4% do primeiro ao ultimo bloco
de 200 mil. Vitacoes por bloco ficaram em ~149 mil, empates ~27.5 mil e
derrotas ~23.5 mil — todas as metricas estaveis. Contra o baseline com pesos
+2/+1/-5 (mesma rodada, 1M): 98.7% de aproveitamento, 825,711 vitorias e
apenas 13,207 derrotas. Com pesos +3/+1/-1 o agente **perdeu 104,991 partidas
a mais** e venceu 81,772 a menos.

**Em que trecho do gráfico ocorreu a mudanca mais importante?**
Em nenhum: o grafico e reto do comeco ao fim (maior variacao entre blocos:
+0.4pp, entre o 2o e o 3o bloco). A curva ja nasce estavel — a mudanca
importante aconteceu antes da partida 200,000 e nao ha inflexao visivel
depois disso.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Nunca. As derrotas se mantiveram em ~11,700-12,200 por bloco de 200 mil
(11.8% das partidas) do comeco ao fim; a ultima derrota foi na partida
999,995. Ao contrario dos pesos antigos, aqui as derrotas **nao diminuem com
treino** — a politica tolera risco e o ingenuo pune.

**O que voces decidiram testar ou alterar na proxima execucao?**
Reverter para os pesos +2/+1/-5 (resultado estritamente melhor em vitorias,
empates e derrotas neste teste) e atacar o problema de exploracao: testar um
epsilon pequeno (ex. 0.01) para visitar estados fora das 221 linhas ja
conhecidas — o verdadeiro teto identificado nos experimentos anteriores.
