# Relatorio comparativo 100k — pesos 20/1/−1 (epsilon 0)

**Experimento:** `eps0_pes2011` — vitoria +20, empate +1, derrota −1,
epsilon 0.0, 100.000 rodadas, seed 42, apenas `aprendiz_vs_ingenuo`.

## Resultado

| Pesos V/E/D | V / E / D | Vitorias | Sem derrota |
|-------------|---------|----------|-------------|
| 10/1/−1 (`eps0_pes1011`) | 73.234 / 14.078 / 12.688 | 73,2% | 87,3% |
| **20/1/−1** (`eps0_pes2011`) | **73.234 / 14.078 / 12.688** | **73,2%** | **87,3%** |

Identidade total: mesmos resultados, mesmos 220 estados, mesma distribuicao de
2a jogada, mesmas acoes na tabela Q. Dobrar a vitoria sem tocar em empate ou
derrota preserva a ordem do argmax — a politica gulosa nao muda.

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Igual ao 10/1/−1: plano, 73,2% de vitorias.

**Em que trecho do grafico ocorreu a mudanca mais importante?**
Nenhuma — e o proprio achado: grafico identico ao do 10/1/−1.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Nao — 12.688 derrotas.

**Depois de observar este resultado, o que voces decidiram testar ou alterar na proxima execucao?**
Escala de vitoria (10, 20) e parametro invariante; os unicos pesos com efeito
real observado ate agora: empate 0 (+5,6pp no baseline, `eps0_pes205`) e a
derrota −5 (aversao a risco do baseline). Proximos candidatos se a serie
continuar: `2/0/−3` (fecha a matriz {±empate}×{−5,−3}) ou encerrar com
baseline 2/1/−5.

## Comandos

```bash
.venv/bin/python run_aprendizado.py --rounds 100000 \
  --scenario aprendiz_vs_ingenuo --root experiments/learning/eps0_pes2011
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps0_pes2011/rodadas_100000/aprendiz_vs_ingenuo/progress.jsonl \
  --partida 100000
```
