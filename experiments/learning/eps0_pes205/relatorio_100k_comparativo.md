# Relatorio comparativo 100k — pesos 2/0/−5 vs serie completa (epsilon 0)

**Experimento:** `eps0_pes205` — recompensa vitoria +2, empate +0, derrota −5
(baseline sem o premio de empate), epsilon 0.0, 100.000 rodadas, seed 42,
apenas `aprendiz_vs_ingenuo`.

**Comparacao (aprendiz = J1, mesmas 100.000 rodadas, seed 42):**

| Pesos V/E/D | V / E / D | Vitorias | Sem derrota | Estados Q |
|-------------|-----------|----------|-------------|-----------|
| 2/1/−5 (baseline, `eps0_pes215`) | 82.513 / 16.018 / 1.469 | 82,5% | **98,5%** | 300 |
| 3/1/−1 (`eps0_pes311`, 1M) | 743.939 / 137.833 / 118.228 | 74,4% | 88,2% | — |
| 4/2/−4 (`eps0_pes424`, 1M) | 806.610 / 137.613 / 55.777 | 80,7% | 94,4% | — |
| 10/1/−1 (`eps0_pes1011`) | 73.234 / 14.078 / 12.688 | 73,2% | 87,3% | 220 |
| 10/1/−3 (`eps0_pes1013`) | 75.348 / 13.545 / 11.107 | 75,3% | 88,9% | 224 |
| 10/0/−1 (`eps0_pes1001`) | 78.769 / 8.643 / 12.588 | 78,8% | 87,4% | 230 |
| 10/0/−3 (`eps0_pes1003`) | 79.809 / 8.135 / 12.056 | 79,8% | 87,9% | 235 |
| **2/0/−5** (`eps0_pes205`) | **88.066 / 10.150 / 1.784** | **88,1%** | 98,2% | **347** |

## Masterizacao da arvore

| Metrica | baseline 2/1/−5 | 2/0/−5 |
|---------|-----------------|--------|
| Abertura | canto0 100% | canto0 100% |
| Migracoes | 0 | 0 |
| Estados novos por janela | 300 na 0, +0 depois | 347 na 0, +0 depois |
| 2a jogada do X | 8 celulas | 5 principais {2:25k, 4:25k, 6:25k, 7:12k, 8:12k} |
| Ultima derrota | p99.952 (janela 100k) | p99.975 |

Leitura:

1. **Maior salto de vitorias de toda a serie: +5,6pp (82,5% → 88,1%)** ao tirar
   o premio do empate mantendo +2/−5. Empates caem de16.018 para10.150 (−36%)
   e viram vitorias. Aproveitamento praticamente empatado (98,2% vs 98,5%):
   as ~315 derrotas a mais sao o custo.
2. **Nao chega a 100%** — ultima derrota na partida99.975, ~170 derrotas por
   janela. Confirmado: nenhum arranjo de pesos puros zerou derrotas em100k;
   so o curriculo epsilon (0,25→0, fase2, `eps025_0_pes215`) atingiu 0D.
3. **Tabela Q maior que qualquer outro peso** (347 vs 300 do baseline): sem
   prêmio de empate o agente testa mais ramos (2a jogada em5 celulas
   principais) — recompensa de empate era o que encurtava a exploracao.
4. Persistencia em arvore segue identica e estrutural em todos: abertura
   canto0 100%, 0 migracoes, exploracao fechada na janela 0.

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Melhor curva da serie: 97,3% de aproveitamento ja na primeira janela, 98,1–98,5%
estavel depois. Total 88.066V / 10.150E / 1.784D.

**Em que trecho do grafico ocorreu a mudanca mais importante?**
A primeira janela (272 derrotas, ~2x o ritmo das demais ~170): greedy ainda
fechando contas; depois constante.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Nao. Ultima derrota na partida 99.975.

**Depois de observar este resultado, o que voces decidiram testar ou alterar na proxima execucao?**
Empate 0 confirmou utilidade (+5,6pp vitorias empatando aproveitamento);
vit forte (+10) confirmou inutilidade. Se houver um ultimo teste de pesos:
**2/0/−3** (empate 0 + derrota suavizada no baseline) fecharia a matriz
{±empate} x {−5,−3}. Aproveitamento maximo observado em pesos puros: 98,5%
(2/1/−5) / 98,2% (2/0/−5); o teto de "sem derrota" real so veio do curriculo.

## Comandos

```bash
# regenerar (identico, seed 42)
.venv/bin/python run_aprendizado.py --rounds 100000 \
  --scenario aprendiz_vs_ingenuo --root experiments/learning/eps0_pes205
# consulta pontual
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps0_pes205/rodadas_100000/aprendiz_vs_ingenuo/progress.jsonl \
  --partida 100000
```
