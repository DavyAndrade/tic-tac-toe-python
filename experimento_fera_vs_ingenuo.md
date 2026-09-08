# Experimento: fera vs ingenuo

**Algoritmos:**
- `fera` — Jogador 1 (X)
- `ingenuo` — Jogador 2 (O)

**Configuracao:**
- Ordem alternada (J1 e J2 trocam posicao)
- Semente: 42

## Resultados progressivos

| Rodadas | V (vitorias) | D (derrotas) | E (empates) | Tempo |
|---------|-------------|-------------|-------------|-------|
| 100,000 | 90,020 | 0 | 9,980 | 1.41s |
| 200,000 | 180,135 | 0 | 19,865 | 2.82s |
| 300,000 | 270,188 | 0 | 29,812 | 4.29s |
| 400,000 | 360,206 | 0 | 39,794 | 5.81s |
| 500,000 | 450,336 | 0 | 49,664 | 7.24s |
| 600,000 | 540,530 | 0 | 59,470 | 8.83s |
| 700,000 | 630,668 | 0 | 69,332 | 10.34s |
| 800,000 | 720,701 | 0 | 79,299 | 11.70s |
| 900,000 | 810,727 | 0 | 89,273 | 13.36s |
| 1,000,000 | 900,958 | 0 | 99,042 | 14.76s |

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
{"id": 1, "j1": "fera", "v": 1, "j2": "ingenuo", "n": 5, "winner": "fera", "t0": 1, "t1": 1, "t2": 1, "t3": -1, "t4": 0, "t5": 0, "t6": 0, "t7": 0, "t8": -1}
{"id": 2, "j1": "ingenuo", "v": 0, "j2": "fera", "n": 6, "winner": "fera", "t0": -1, "t1": -1, "t2": -1, "t3": 1, "t4": 0, "t5": 0, "t6": 0, "t7": 1, "t8": 1}
{"id": 3, "j1": "fera", "v": 1, "j2": "ingenuo", "n": 5, "winner": "fera", "t0": 1, "t1": 1, "t2": 1, "t3": 0, "t4": 0, "t5": -1, "t6": -1, "t7": 0, "t8": 0}
{"id": 4, "j1": "ingenuo", "v": 0, "j2": "fera", "n": 6, "winner": "fera", "t0": -1, "t1": 0, "t2": 1, "t3": 1, "t4": -1, "t5": 0, "t6": 0, "t7": 1, "t8": -1}
{"id": 5, "j1": "fera", "v": 1, "j2": "ingenuo", "n": 5, "winner": "fera", "t0": 1, "t1": 1, "t2": 1, "t3": 0, "t4": -1, "t5": -1, "t6": 0, "t7": 0, "t8": 0}
```
