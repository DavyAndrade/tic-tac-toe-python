# Experimento: aprendiz vs ingenuo (1,000,000 rodadas)

**Configuracao:**
- X (J1): `aprendiz`
- O (J2): `ingenuo`
- Semente: 42
- Rodadas: 1,000,000
- Recompensa: **vitoria +4, empate +2, derrota -4** (variante `pesos424`)
- epsilon: 0.0 (sem epsilon; exploracao so pelo desempate aleatorio de estados zerados)

Dados: `experiments/learning/eps0_pes424/rodadas_1000000/aprendiz_vs_ingenuo/`

## Resultado acumulado

| Partida | J1 (aprendiz) | V | J2 (ingenuo) |
|---------|---------------|---|--------------|
| 100,000 | 80,378 | 13,836 | 5,786 |
| 500,000 | 402,658 | 68,897 | 28,445 |
| 1,000,000 | 806,610 | 137,613 | 55,777 |

## Evolucao por janela de 100,000 partidas (aprendiz = J1)

| Janela | V | E | D | Aproveitamento |
|--------|---|---|---|----------------|
| 1-100,000 | 80,378 | 13,836 | 5,786 | 94.2% |
| 100,001-200,000 | 80,426 | 13,813 | 5,763 | 94.2% |
| 200,001-300,000 | 80,759 | 13,561 | 5,680 | 94.3% |
| 300,001-400,000 | 80,569 | 13,705 | 5,726 | 94.3% |
| 400,001-500,000 | 81,072 | 13,438 | 5,490 | 94.5% |
| 500,001-600,000 | 81,312 | 13,340 | 5,348 | 94.7% |
| 600,001-700,000 | 80,777 | 13,658 | 5,565 | 94.4% |
| 700,001-800,000 | 81,127 | 13,349 | 5,524 | 94.5% |
| 800,001-900,000 | 81,198 | 13,424 | 5,378 | 94.6% |
| 900,001-1,000,000 | 80,992 | 13,491 | 5,517 | 94.5% |

## Comparacao das variantes de pesos (1M, epsilon 0, mesmo seed)

| Variante | Vitorias | Empates | Derrotas | Aproveit. | Estados Q |
|----------|----------|---------|----------|-----------|-----------|
| +2/+1/-5 (`eps0_pes215`) | 825,711 | 161,082 | 13,207 | 98.7% | 300 |
| **+4/+2/-4 (`eps0_pes424`)** | **806,610** | **137,613** | **55,777** | **94.4%** | **233** |
| +3/+1/-1 (`eps0_pes311`) | 743,939 | 137,833 | 118,228 | 88.2% | 221 |

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 233 | 3,966,720 |

## Grafico

`progress.svg` — series `J1 (Aprendiz)` / `V` / `J2 (Ingenuo)`; gerado por
`matplotlib` a partir de `progress.jsonl`.

## Arquivos

```
experiments/learning/eps0_pes424/rodadas_1000000/aprendiz_vs_ingenuo/
├── episodes.jsonl    # ~316M — LOCAL, fora do Git (limite 100MB do GitHub)
├── progress.jsonl    # ~185M — LOCAL, fora do Git
├── q_table.json      # versionado
├── progress.svg      # versionado
└── aprendiz_vs_ingenuo.md    # este relatorio (versionado)
```

JSONLs grandes ficam locais e regeneraveis identicos (seed 42).

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --root experiments/learning/eps0_pes424 \
  --rounds 1000000 --scenario aprendiz_vs_ingenuo
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps0_pes424/rodadas_1000000/aprendiz_vs_ingenuo/progress.jsonl \
  --partida 1000000
```

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Praticamente nada: aproveitamento entre 94.2% e 94.7% em todas as janelas de\n100 mil. Derrotas por janela oscilaram 5,348-5,786 (5.5% constantes),\nvitorias ~81,000 e empates ~13,500 por janela. Melhor que a variante
+3/+1/-1 (88.2%) mas pior que o baseline +2/+1/-5 (98.7%) — 42,570 derrotas
a mais que o baseline em 1M.

**Em que trecho do grafico ocorreu a mudanca mais importante?**
Nenhuma: o grafico e plano do comeco ao fim (maior variacao -0.3pp entre os\nblocos 6 e 7, ou seja, dentro do ruido). Prefixo de 100 mil ja nasce em
94.2% — com epsilon 0 tudo e decidido antes da partida 100,000.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Nao. ~5,500 derrotas por janela de 100 mil (5.5%) ate o fim; ultima derrota
na partida 999,965. A taxa caiu contra a variante +3/+1/-1 (11.8%) mas nao
zera e nao diminui com treino.

**Depois de observar este resultado, o que voces decidiram testar ou alterar na proxima execucao?**
Os tres pesos testados deixam o baseline +2/+1/-5 como campeao em vitorias e
derrotas — entao manter ele como padrao de resultados. O proximo alvo nao e
peso: e exploracao. Testar epsilon pequeno (ex. 0.01) para furar o platou de
estados (233 aqui, 300 no baseline — nenhuma variante de peso visitou linhas
novas), mantendo +2/+1/-5.
