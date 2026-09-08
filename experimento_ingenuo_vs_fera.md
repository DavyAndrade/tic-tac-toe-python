# Experimento: ingenuo vs fera

**Algoritmos:**
- `ingenuo` — Jogador 1 (X)
- `fera` — Jogador 2 (O)

**Configuracao:**
- Ordem alternada (J1 e J2 trocam posicao)
- Semente: 42

## Resultados progressivos

| Rodadas | V (vitorias) | D (derrotas) | E (empates) | Tempo |
|---------|-------------|-------------|-------------|-------|
| 100,000 | 0 | 90,013 | 9,987 | 1.46s |
| 200,000 | 0 | 180,080 | 19,920 | 2.86s |
| 300,000 | 0 | 270,083 | 29,917 | 4.36s |
| 400,000 | 0 | 360,305 | 39,695 | 5.85s |
| 500,000 | 0 | 450,530 | 49,470 | 7.37s |
| 600,000 | 0 | 540,548 | 59,452 | 8.79s |
| 700,000 | 0 | 630,703 | 69,297 | 10.14s |
| 800,000 | 0 | 720,778 | 79,222 | 11.86s |
| 900,000 | 0 | 810,930 | 89,070 | 13.01s |
| 1,000,000 | 0 | 900,981 | 99,019 | 14.96s |

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
{"id": 1, "j1": "ingenuo", "v": 0, "j2": "fera", "n": 9, "winner": "draw", "t0": 1, "t1": -1, "t2": 1, "t3": -1, "t4": 1, "t5": 1, "t6": -1, "t7": 1, "t8": -1}
{"id": 2, "j1": "fera", "v": 1, "j2": "ingenuo", "n": 5, "winner": "fera", "t0": 1, "t1": 1, "t2": 1, "t3": 0, "t4": -1, "t5": 0, "t6": 0, "t7": 0, "t8": -1}
{"id": 3, "j1": "ingenuo", "v": 0, "j2": "fera", "n": 9, "winner": "draw", "t0": 1, "t1": 1, "t2": -1, "t3": -1, "t4": 1, "t5": 1, "t6": 1, "t7": -1, "t8": -1}
{"id": 4, "j1": "fera", "v": 1, "j2": "ingenuo", "n": 5, "winner": "fera", "t0": 1, "t1": 1, "t2": 1, "t3": -1, "t4": -1, "t5": 0, "t6": 0, "t7": 0, "t8": 0}
{"id": 5, "j1": "ingenuo", "v": 0, "j2": "fera", "n": 9, "winner": "draw", "t0": -1, "t1": -1, "t2": 1, "t3": 1, "t4": 1, "t5": -1, "t6": -1, "t7": 1, "t8": 1}
```
