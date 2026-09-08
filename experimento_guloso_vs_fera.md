# Experimento: guloso vs fera

**Algoritmos:**
- `guloso` — Jogador 1 (X)
- `fera` — Jogador 2 (O)

**Configuracao:**
- Ordem alternada (J1 e J2 trocam posicao)
- Semente: 42

## Resultados progressivos

| Rodadas | V (vitorias) | D (derrotas) | E (empates) | Tempo |
|---------|-------------|-------------|-------------|-------|
| 100,000 | 0 | 50,000 | 50,000 | 3.57s |
| 200,000 | 0 | 100,000 | 100,000 | 7.20s |
| 300,000 | 0 | 150,000 | 150,000 | 10.65s |
| 400,000 | 0 | 200,000 | 200,000 | 14.37s |
| 500,000 | 0 | 250,000 | 250,000 | 18.26s |
| 600,000 | 0 | 300,000 | 300,000 | 21.28s |
| 700,000 | 0 | 350,000 | 350,000 | 25.09s |
| 800,000 | 0 | 400,000 | 400,000 | 28.35s |
| 900,000 | 0 | 450,000 | 450,000 | 32.22s |
| 1,000,000 | 0 | 500,000 | 500,000 | 35.88s |

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
{"id": 1, "j1": "guloso", "v": 0, "j2": "fera", "n": 9, "winner": "draw", "t0": 1, "t1": 1, "t2": -1, "t3": -1, "t4": -1, "t5": 1, "t6": 1, "t7": -1, "t8": 1}
{"id": 2, "j1": "fera", "v": 1, "j2": "guloso", "n": 7, "winner": "fera", "t0": 1, "t1": -1, "t2": 0, "t3": 1, "t4": 1, "t5": -1, "t6": -1, "t7": 0, "t8": 1}
{"id": 3, "j1": "guloso", "v": 0, "j2": "fera", "n": 9, "winner": "draw", "t0": 1, "t1": 1, "t2": -1, "t3": -1, "t4": -1, "t5": 1, "t6": 1, "t7": -1, "t8": 1}
{"id": 4, "j1": "fera", "v": 1, "j2": "guloso", "n": 7, "winner": "fera", "t0": 1, "t1": -1, "t2": 0, "t3": 1, "t4": 1, "t5": -1, "t6": -1, "t7": 0, "t8": 1}
{"id": 5, "j1": "guloso", "v": 0, "j2": "fera", "n": 9, "winner": "draw", "t0": 1, "t1": 1, "t2": -1, "t3": -1, "t4": -1, "t5": 1, "t6": 1, "t7": -1, "t8": 1}
```
