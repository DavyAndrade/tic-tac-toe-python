# Relatorio comparativo 100k — pesos 10/0/−1 vs série de pesos (epsilon 0)

**Experimento:** `eps0_pes1001` — recompensa vitoria +10, empate +0, derrota −1,
epsilon 0.0, 100.000 rodadas, seed 42, apenas `aprendiz_vs_ingenuo`. Ideia:
empate sem recompensa — só vitórias pagam; combina vitória forte com derrota
suavizada para o guloso masterizar uma árvore.

**Comparação (aprendiz = J1, mesmas 100.000 rodadas, seed 42):**

| Pesos V/E/D | V / E / D | Vitórias | Sem derrota | Estados Q | 2ª jogada do X |
|-------------|-----------|----------|-------------|-----------|----------------|
| **2/1/−5** (baseline, `eps0_pes215`) | 82.513 / 16.018 / 1.469 | 82,5% | **98,5%** | 300 | 8 células |
| 10/1/−1 (`eps0_pes1011`) | 73.234 / 14.078 / 12.688 | 73,2% | 87,3% | 220 | {2:37,6k, 4:24,8k, 6:25,2k, 8:12,4k} |
| 10/1/−3 (`eps0_pes1013`) | 75.348 / 13.545 / 11.107 | 75,3% | 88,9% | 224 | idêntica ao 10/1/−1 |
| **10/0/−1** (`eps0_pes1001`) | 78.769 / 8.643 / 12.588 | **78,8%** | 87,4% | 230 | {2:25,2k, 4:24,8k, 6:25,2k, 8:24,8k} |

## Masterização da árvore

| Métrica | 2/1/−5 | 10/1/−1 | 10/1/−3 | 10/0/−1 |
|---------|--------|---------|---------|---------|
| Abertura | canto0 100% | canto0 100% | canto0 100% | canto0 100% |
| Migrações | 0 | 0 | 0 | 0 |
| Estados novos por janela | 300 na 0, +0 depois | 220 na 0, +0 | 224 na 0, +0 | 230 na 0, +0 |
| Saturados | 80/300 | 55/220 | 56/224 | 62/230 |

Leitura:

1. **Remover a recompensa de empate surtiu efeito real:** empates caem de
   ~13,5k para 8,6k (−36%) e a 2ª jogada do X se **equilibra** (4 células ~25k
   cada, contra o viés 37k/12k dos pesos com empate +1) — sem prêmio para a
   linha que empata, o agente redistribui os ramos que tenta.
2. **Melhor vitória da série 10x (78,8%), mas mais derrotas que 10/1/−3**
   (12.588 vs 11.107): o empate 0 empurra para ladas mais arriscados. Ainda
   4,7pp abaixo do baseline em vitórias e 11pp em "sem derrota".
3. **Persistência em árvore segue idêntica e estrutural:** 0 migrações,
   exploração fechada na janela 0 em todas as configurações.

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Plano: 78,7% de vitórias na 1ª quarta parte, 78,4% na última; ~3.100 derrotas
por fatia de 25 mil o tempo todo. Total 78.769V / 8.643E / 12.588D (87,4% sem
derrota).

**Em que trecho do grafico ocorreu a mudanca mais importante?**
Nenhuma — variação entre fatias < 1pp; epsilon 0 converge antes da partida
10.000.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Não. Derrotas em ritmo constante ate a partida 100.000.

**Depois de observar este resultado, o que voces decidiram testar ou alterar na proxima execucao?**
Série 10x esgotou variantes úteis (−1, −3, empate 0): nenhuma alcança o
baseline 2/1/−5 (98,5% sem derrota). O empate 0 é o melhor ajuste interno dos
10x (mais vitórias, mesmos ramos equilibrados) e confirma que o prêmio de
empate +1 é o que cria a linha "segura". Próximo passo candidato: **2/1/−3**
ou **2/0/−5** para isolar se o empate 0 também melhora o baseline — ou encerrar
a série de pesos com 2/1/−5 como campeão.

## Comandos

```bash
# regenerar (identico, seed 42)
.venv/bin/python run_aprendizado.py --rounds 100000 \
  --scenario aprendiz_vs_ingenuo --root experiments/learning/eps0_pes1001
# consulta pontual
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps0_pes1001/rodadas_100000/aprendiz_vs_ingenuo/progress.jsonl \
  --partida 100000
```
