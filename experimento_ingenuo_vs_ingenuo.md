# Experimento: ingenuo vs ingenuo

**Algoritmos:**
- `ingenuo` — Jogador 1 (X)
- `ingenuo` — Jogador 2 (O)

**Configuracao:**
- Ordem alternada (J1 e J2 trocam posicao)
- Semente: 42

## Resultados progressivos

| Rodadas | V (vitorias) | D (derrotas) | E (empates) | Tempo |
|---------|-------------|-------------|-------------|-------|
| 100,000 | 87,146 | 87,146 | 25,708 | 1.74s |
| 200,000 | 174,565 | 174,565 | 50,870 | 3.58s |
| 300,000 | 261,953 | 261,953 | 76,094 | 5.31s |
| 400,000 | 349,500 | 349,500 | 101,000 | 7.09s |
| 500,000 | 436,892 | 436,892 | 126,216 | 8.92s |
| 600,000 | 524,113 | 524,113 | 151,774 | 10.77s |
| 700,000 | 611,558 | 611,558 | 176,884 | 12.63s |
| 800,000 | 698,843 | 698,843 | 202,314 | 14.36s |
| 900,000 | 786,136 | 786,136 | 227,728 | 16.31s |
| 1,000,000 | 873,413 | 873,413 | 253,174 | 18.05s |

## Formato de cada partida

```json
{
  "id": "inteiro sequencial",
  "j1": "nome do algoritmo J1",
  "v": "0 = draw/empate, 1 = J1 venceu",
  "j2": "nome do algoritmo J2",
  "n": "numero de jogadas",
  "winner": "nome do vencedor ou draw",
  "t0".."t8": "1 = marca J1, 0 = vazio, -1 = marca J2"
}
```

## Amostra (ultima rodada - 5 partidas)

```json
{"id": 1, "j1": "ingenuo", "v": 1, "j2": "ingenuo", "n": 7, "winner": "ingenuo", "t0": -1, "t1": 0, "t2": -1, "t3": 1, "t4": 1, "t5": 1, "t6": 0, "t7": 1, "t8": -1}
{"id": 2, "j1": "ingenuo", "v": 1, "j2": "ingenuo", "n": 9, "winner": "ingenuo", "t0": 1, "t1": 1, "t2": 1, "t3": 1, "t4": -1, "t5": -1, "t6": -1, "t7": -1, "t8": 1}
{"id": 3, "j1": "ingenuo", "v": 0, "j2": "ingenuo", "n": 9, "winner": "draw", "t0": 1, "t1": 1, "t2": -1, "t3": -1, "t4": 1, "t5": 1, "t6": 1, "t7": -1, "t8": -1}
{"id": 4, "j1": "ingenuo", "v": 1, "j2": "ingenuo", "n": 9, "winner": "ingenuo", "t0": 1, "t1": -1, "t2": -1, "t3": 1, "t4": 1, "t5": 1, "t6": -1, "t7": 1, "t8": -1}
{"id": 5, "j1": "ingenuo", "v": 1, "j2": "ingenuo", "n": 9, "winner": "ingenuo", "t0": -1, "t1": -1, "t2": 1, "t3": 1, "t4": -1, "t5": 1, "t6": -1, "t7": 1, "t8": 1}
```
