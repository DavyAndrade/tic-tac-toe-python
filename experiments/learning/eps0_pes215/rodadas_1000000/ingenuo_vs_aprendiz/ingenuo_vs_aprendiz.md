# Experimento: ingenuo vs aprendiz (1,000,000 rodadas)

**Configuracao:**
- X (J1): `ingenuo`
- O (J2): `aprendiz`
- Semente: 42
- Rodadas: 1,000,000
- Recompensa: vitoria +2, empate +1, derrota -5
- **epsilon: 0.0** — padrao congelado para todos os experimentos a partir
  desta rodada (exploracao so pelo desempate aleatorio de estados zerados,
  EC-003)

Dados: `experiments/learning/eps0_pes215/rodadas_1000000/ingenuo_vs_aprendiz/`

## Resultado acumulado

| Partida | J1 (ingenuo) | V | J2 (aprendiz) |
|---------|--------------|---|---------------|
| 1,000 | 370 | 197 | 433 |
| 100,000 | 10,160 | 29,871 | 59,969 |
| 500,000 | 47,985 | 151,132 | 300,883 |
| 1,000,000 | 95,783 | 302,203 | 602,014 |

## Evolucao por janela de 100,000 partidas (aprendiz = J2)

| Janela | V | E | D | Aproveitamento |
|--------|---|---|---|----------------|
| 1-100,000 | 59,969 | 29,871 | 10,160 | 89.8% |
| 100,001-200,000 | 60,405 | 30,141 | 9,454 | 90.5% |
| 200,001-300,000 | 59,970 | 30,577 | 9,453 | 90.5% |
| 300,001-400,000 | 60,306 | 30,261 | 9,433 | 90.6% |
| 400,001-500,000 | 60,233 | 30,282 | 9,485 | 90.5% |
| 500,001-600,000 | 60,352 | 30,156 | 9,492 | 90.5% |
| 600,001-700,000 | 60,320 | 30,043 | 9,637 | 90.4% |
| 700,001-800,000 | 60,044 | 30,397 | 9,559 | 90.4% |
| 800,001-900,000 | 60,379 | 30,061 | 9,560 | 90.4% |
| 900,001-1,000,000 | 60,036 | 30,414 | 9,550 | 90.5% |

Leitura: **platol** — 89.8% na primeira janela e ~90.5% em todas as
seguintes; o ganho real ja tinha acontecido antes da partida 200,000 e 10x de
rodadas depois nao movem a agulha. O primeiro bloco de 100,000 e prefixo
identico ao de `experiments/learning/eps0_pes215/rodadas_100000/` (mesma cadeia de
seeds), confirmando determinismo.

A tabela Q termina com **1,070 estados** — os mesmos 1,070 do experimento de
100,000. Com epsilon 0 o agente em O nao sai das linhas que ja conhece.
Baseline epsilon 0.1 (100k, historico do Git): 2,076 estados e 92.5% de
aproveitamento, contra 90.5% aqui — mais exploracao rendeu mais neste lado.

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 1,070 | 3,499,511 |

## Grafico

`progress.svg` — series `J1 (Ingenuo)` / `V` / `J2 (Aprendiz)` por partida.
Gerado por `matplotlib` a partir de `progress.jsonl`.

## Arquivos

```
experiments/learning/eps0_pes215/rodadas_1000000/ingenuo_vs_aprendiz/
├── episodes.jsonl    # ~300M — LOCAL, fora do Git (limite 100MB do GitHub)
├── progress.jsonl    # ~185M — LOCAL, fora do Git
├── q_table.json      # versionado
├── progress.svg      # versionado
└── ingenuo_vs_aprendiz.md    # este relatorio (versionado)
```

Os JSONLs grandes ficam locais e sao regeneraveis identicos (seed 42).

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --rounds 1000000 --scenario ingenuo_vs_aprendiz
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps0_pes215/rodadas_1000000/ingenuo_vs_aprendiz/progress.jsonl \
  --partida 1000000
```

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Estabilizado: 89.8% na primeira janela de 100 mil, ~90.5% em todas as seguintes. Derrotas estaveis ~9,500 por janela (9.5%), vitorias ~60,200, empates
~30,200. Total 1,000,000: 602,014V / 302,203E / 95,783D (90.5%).

**Em que trecho do grafico ocorreu a mudanca mais importante?**
Nenhuma mudanca relevante: +0.7pp entre a 1a e a 2a janela e depois reta.
Prefixo identico ao experimento de 100,000 (mesma cadeia de seeds); Q final
de 1,070 estados, os mesmos do experimento de 100k.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Nao. Ultima derrota na partida 999,974, ~9,500 derrotas por janela ate o
fim. O lado J2 sobe ~1pp em 900 mil partidas — exploracao (epsilon 0), nao
volume, e o gargalo.

**Depois de observar este resultado, o que voces decidiram testar ou alterar na proxima execucao?**
Mudar os pesos para +3/+1/-1 (feito: `eps0_pes311/rodadas_1000000`) para
ver se menos penalidade de derrota aumenta vitorias — executado; ver
relatorios da variante para o resultado.
