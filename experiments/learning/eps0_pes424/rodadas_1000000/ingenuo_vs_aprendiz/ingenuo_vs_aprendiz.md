# Experimento: ingenuo vs aprendiz (1,000,000 rodadas)

**Configuracao:**
- X (J1): `ingenuo`
- O (J2): `aprendiz`
- Semente: 42
- Rodadas: 1,000,000
- Recompensa: **vitoria +4, empate +2, derrota -4** (variante `pesos424`)
- epsilon: 0.0 (sem epsilon; exploracao so pelo desempate aleatorio de estados zerados)

Dados: `experiments/learning/eps0_pes424/rodadas_1000000/ingenuo_vs_aprendiz/`

## Resultado acumulado

| Partida | J1 (ingenuo) | V | J2 (aprendiz) |
|---------|--------------|---|---------------|
| 100,000 | 12,190 | 32,954 | 54,856 |
| 500,000 | 57,659 | 166,471 | 275,870 |
| 1,000,000 | 114,175 | 333,260 | 552,565 |

## Evolucao por janela de 100,000 partidas (aprendiz = J2)

| Janela | V | E | D | Aproveitamento |
|--------|---|---|---|----------------|
| 1-100,000 | 54,856 | 32,954 | 12,190 | 87.8% |
| 100,001-200,000 | 55,460 | 33,154 | 11,384 | 88.6% |
| 200,001-300,000 | 55,548 | 33,071 | 11,380 | 88.6% |
| 300,001-400,000 | 55,478 | 33,165 | 11,356 | 88.6% |
| 400,001-500,000 | 55,649 | 33,001 | 11,349 | 88.7% |
| 500,001-600,000 | 55,773 | 32,879 | 11,347 | 88.7% |
| 600,001-700,000 | 55,105 | 33,317 | 11,577 | 88.4% |
| 700,001-800,000 | 55,706 | 33,087 | 11,206 | 88.8% |
| 800,001-900,000 | 55,797 | 33,021 | 11,181 | 88.8% |
| 900,001-1,000,000 | 55,193 | 33,610 | 11,205 | 88.8% |

## Comparacao das variantes de pesos (1M, epsilon 0, mesmo seed)

| Variante | Vitorias (J2) | Empates | Derrotas | Aproveit. | Estados Q |
|----------|---------------|---------|----------|-----------|-----------|
| +2/+1/-5 (`eps0_pes215`) | 602,014 | 302,203 | 95,783 | 90.5% | 1,070 |
| **+4/+2/-4 (`eps0_pes424`)** | **552,565** | **333,260** | **114,175** | **88.6%** | **1,064** |
| +3/+1/-1 (`eps0_pes311`) | 536,669 | 247,032 | 216,299 | 78.3% | 807 |

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 1,064 | 3,524,761 |

## Grafico

`progress.svg` — series `J1 (Ingenuo)` / `V` / `J2 (Aprendiz)`; gerado por
`matplotlib` a partir de `progress.jsonl`.

## Arquivos

```
experiments/learning/eps0_pes424/rodadas_1000000/ingenuo_vs_aprendiz/
├── episodes.jsonl    # ~300M — LOCAL, fora do Git (limite 100MB do GitHub)
├── progress.jsonl    # ~185M — LOCAL, fora do Git
├── q_table.json      # versionado
├── progress.svg      # versionado
└── ingenuo_vs_aprendiz.md    # este relatorio (versionado)
```

JSONLs grandes ficam locais e regeneraveis identicos (seed 42).

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --root experiments/learning/eps0_pes424 \
  --rounds 1000000 --scenario ingenuo_vs_aprendiz
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps0_pes424/rodadas_1000000/ingenuo_vs_aprendiz/progress.jsonl \
  --partida 1000000
```

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Quase nada: aproveitamento de 87.8% na primeira janela de 100 mil para 88.8%
nas ultimas, estavel desde a segunda. Derrotas por janela caíram de 12,190
para ~11,200 (11.2% constantes); vitorias ~55,500 e empates ~33,100 por
janela. Total 1M: 552,565V / 333,260E / 114,175D (88.6%) — melhor que
+3/+1/-1 (78.3%) mas pior que o baseline +2/+1/-5 (90.5%). Note que os
empates sao os maiores de todas as variantes (333k vs 302k e 247k): o peso
+2 no empate (metade da vitoria) exatamente valoriza linha segura.

**Em que trecho do grafico ocorreu a mudanca mais importante?**
Entre a 1a e a 2a janela (+0.8pp, de 87.8% para 88.6%) — depois plano
88.4-88.8% por 900 mil partidas. Prefixo de 100 mil ja nasce treinado; nao ha
inflexao visivel no resto do grafico.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Nao. ~11,200-12,200 derrotas por janela de 100 mil ate o fim; ultima derrota
na partida 999,998. A taxa estabilizou ja na segunda janela (apos ~200 mil)
mas nao zera nem diminui depois disso.

**Depois de observar este resultado, o que voces decidiram testar ou alterar na proxima execucao?**
Mesmo veredicto do lado J1: entre as tres variantes de pesos o baseline
+2/+1/-5 continua vencendo, entao os pesos saem da agenda. Proximo teste:
epsilon pequeno (ex. 0.01) para visitar estados fora dos ~1,064 estados
conhecidos — todas as variantes de peso presam a tabela no mesmo teto, o que
confirma que exploracao e o gargalo, nao recompensa.
