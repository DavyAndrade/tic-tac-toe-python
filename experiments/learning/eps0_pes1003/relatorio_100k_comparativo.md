# Relatorio comparativo 100k — pesos 10/0/−3 vs serie de pesos (epsilon 0)

**Experimento:** `eps0_pes1003` — recompensa vitoria +10, empate +0, derrota −3,
epsilon 0.0, 100.000 rodadas, seed 42, apenas `aprendiz_vs_ingenuo`. Combina
sem recompensa de empate com derrota suavizada.

**Comparacao (aprendiz = J1, mesmas 100.000 rodadas, seed 42):**

| Pesos V/E/D | V / E / D | Vitorias | Sem derrota | Estados Q |
|-------------|-----------|----------|-------------|-----------|
| **2/1/−5** (baseline, `eps0_pes215`) | 82.513 / 16.018 / 1.469 | 82,5% | **98,5%** | 300 |
| 10/1/−1 (`eps0_pes1011`) | 73.234 / 14.078 / 12.688 | 73,2% | 87,3% | 220 |
| 10/1/−3 (`eps0_pes1013`) | 75.348 / 13.545 / 11.107 | 75,3% | 88,9% | 224 |
| 10/0/−1 (`eps0_pes1001`) | 78.769 / 8.643 / 12.588 | 78,8% | 87,4% | 230 |
| **10/0/−3** (`eps0_pes1003`) | 79.809 / 8.135 / 12.056 | **79,8%** | 87,9% | 235 |

## Masterizacao da arvore

| Metrica | baseline | 10/0/−1 | 10/0/−3 |
|---------|----------|---------|---------|
| Abertura | canto0 100% | canto0 100% | canto0 100% |
| Migracoes | 0 | 0 | 0 |
| Estados novos por janela | 300 na 0, +0 depois | 230 na 0, +0 | 235 na 0, +0 |
| 2a jogada do X | 8 celulas | {2:25,2k, 4:24,8k, 6:25,2k, 8:24,8k} | **identica** ao 10/0/−1 |

Leitura:

1. **Empate 0 + derrota −3 e o melhor dos 10x** (79,8% vitorias, 12.056D):
   ganha +1pp e −532 derrotas sobre 10/0/−1, +4,5pp sobre 10/1/−3. Os quatro
   10x seguem a ordem logica: empate 0 > empate 1, e dentro de cada empate a
   derrota −3 > −1 em vitorias.
2. **Mesmo assim, 2,7pp abaixo do baseline em vitorias e 10,6pp em "sem
   derrota"** (87,9% vs 98,5%). A serie 10x esgotou as combinacoes utis.
3. **A politica dos dois empate-0 e identica** (mesma distribuicao de 2a
   jogada byte a byte): remover o premio de empate reequilibra os ramos; o
   valor da derrota so desloca medias. Persistencia em arvore segue
   estrutural (0 migracoes, exploracao fechada na janela 0).

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Plano: aproveitamento 87,8% na primeira janela de 10 mil, 87,9% na ultima.
Total 79.809V / 8.135E / 12.056D. ~1.200 derrotas por janela o tempo todo.

**Em que trecho do grafico ocorreu a mudanca mais importante?**
Nenhuma — variacao entre janelas abaixo de 0,5pp; epsilon 0 converge antes da
partida 10.000.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Nao. Ultima derrota na partida 99.997.

**Depois de observar este resultado, o que voces decidiram testar ou alterar na proxima execucao?**
Serie 10x fechada: {10/1/−1, 10/1/−3, 10/0/−1, 10/0/−3} todas perdem para
2/1/−5. Se a questao for "vale a pena tirar o premio de empate?", testar
**2/0/−5** (empate 0 no baseline) isola isso sem o bônus de +10. Caso contrario
encerra-se a serie de pesos com 2/1/−5 campeao entre {2/1/−5, 3/1/−1, 4/2/−4,
10/1/−1, 10/1/−3, 10/0/−1, 10/0/−3}.

## Comandos

```bash
# regenerar (identico, seed 42)
.venv/bin/python run_aprendizado.py --rounds 100000 \
  --scenario aprendiz_vs_ingenuo --root experiments/learning/eps0_pes1003
# consulta pontual
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps0_pes1003/rodadas_100000/aprendiz_vs_ingenuo/progress.jsonl \
  --partida 100000
```
