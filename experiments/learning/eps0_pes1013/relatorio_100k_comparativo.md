# Relatorio comparativo 100k — pesos 10/1/−3 vs 10/1/−1 vs baseline 2/1/−5 (epsilon 0)

**Experimento:** `eps0_pes1013` — recompensa vitoria +10, empate +1, derrota −3,
epsilon 0.0, 100.000 rodadas, seed 42, apenas `aprendiz_vs_ingenuo`. Ideia:
vitória forte + derrota suavizada para o guloso permanecer e masterizar uma
árvore (evitar ir para outra árvore e recomeçar a exploração).

**Configs comparadas (aprendiz = J1, mesmas 100.000 rodadas, seed 42):**

| Pesos V/E/D | V / E / D | Vitórias | Sem derrota | Estados Q | 2ª jogada (células) |
|-------------|-----------|----------|-------------|-----------|---------------------|
| **2/1/−5** (baseline, `eps0_pes215`) | 82.513 / 16.018 / 1.469 | 82,5% | **98,5%** | 300 | 8 |
| 10/1/−1 (`eps0_pes1011`) | 73.234 / 14.078 / 12.688 | 73,2% | 87,3% | 220 | 4 |
| **10/1/−3** (`eps0_pes1013`) | 75.348 / 13.545 / 11.107 | 75,3% | 88,9% | 224 | 4 |

## Masterização da árvore

| Métrica | 2/1/−5 | 10/1/−1 | 10/1/−3 |
|---------|--------|---------|---------|
| Abertura | canto0 100% | canto0 100% | canto0 100% |
| Migrações de abertura | 0 | 0 | 0 |
| Estados novos por janela | 300 na janela 0, +0 depois | 220 na janela 0, +0 depois | 224 na janela 0, +0 depois |
| Saturados (todas as ações testadas) | 80/300 | 55/220 | 56/224 |
| Distribuição 2ª jogada do X | 8 células | {2:37.625, 4:24.812, 6:25.182, 8:12.381} | **idêntica ao 10/1/−1** |

Leitura:

1. **Suavizar a derrota (−1 → −3) ajuda, mas não salva:** +2,1pp de vitórias e
   1.581 derrotas a menos que 10/1/−1. Ainda assim 9,6pp abaixo do baseline.
2. **As escolhas gulosas praticamente não mudam:** a distribuição da 2ª jogada
   do X é idêntica byte a byte à do 10/1/−1; só 4 estados de diferença na
   tabela Q. O peso da derrota desloca médias, não a política — o problema de
   desempenho vem do bônus +10, que dilui a discriminação entre linhas
   vencedoras (quase todas com Q ~7-9).
3. **Persistência em árvore continua estrutural:** 0 migrações, exploração
   fechada na janela 0 — igual em todos os pesos, sem ajuda da recompensa.

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Plano: aproveitamento (V+E) de 88,2% na primeira janela para 89,0% na última.
Total 75.348V / 13.545E / 11.107D (88,9% sem derrota). ~1.111 derrotas por
janela o tempo todo.

**Em que trecho do grafico ocorreu a mudanca mais importante?**
Nenhuma — variação entre janelas abaixo de 1pp; epsilon 0 converge antes da
partida 10.000 e o restante é repetição.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Não. Última derrota na partida 99.997.

**Depois de observar este resultado, o que voces decidiram testar ou alterar na proxima execucao?**
Mantém-se a conclusão anterior com mais um ponto de dado: o casal
(vitória forte, derrota suavizada) não vence o baseline 2/1/−5 — a versão
−3 melhora a −1, mas os dois ficam ~10pp abaixo. Próximo isolamento natural:
**2/1/−3** (mantém a derrota suavizada sem o bônus de +10) para confirmar se a
perda vem do +10 ou da derrota −5. Se não houver mais interesse em pesos,
fecha-se a série: 2/1/−5 é o campeão entre 2/1/−5, 3/1/−1, 4/2/−4, 10/1/−1,
10/1/−3.

## Comandos

```bash
# regenerar (identico, seed 42)
.venv/bin/python run_aprendizado.py --rounds 100000 \
  --scenario aprendiz_vs_ingenuo --root experiments/learning/eps0_pes1013
# consulta pontual
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps0_pes1013/rodadas_100000/aprendiz_vs_ingenuo/progress.jsonl \
  --partida 100000
```
