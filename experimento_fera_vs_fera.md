# Experimento: fera vs fera

**Algoritmos:**
- `fera` — Jogador 1 (X)
- `fera` — Jogador 2 (O)

**Configuracao:**
- Ordem alternada (J1 e J2 trocam posicao)
- Semente: 42

## Resultados progressivos

| Rodadas | V (vitorias) | D (derrotas) | E (empates) | Tempo |
|---------|-------------|-------------|-------------|-------|
| 100,000 | 0 | 0 | 200,000 | 1.35s |
| 200,000 | 0 | 0 | 400,000 | 2.75s |
| 300,000 | 0 | 0 | 600,000 | 4.18s |
| 400,000 | 0 | 0 | 800,000 | 5.65s |
| 500,000 | 0 | 0 | 1,000,000 | 7.12s |
| 600,000 | 0 | 0 | 1,200,000 | 8.37s |
| 700,000 | 0 | 0 | 1,400,000 | 10.17s |
| 800,000 | 0 | 0 | 1,600,000 | 11.44s |
| 900,000 | 0 | 0 | 1,800,000 | 12.75s |
| 1,000,000 | 0 | 0 | 2,000,000 | 14.37s |

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
{"id": 1, "j1": "fera", "v": 0, "j2": "fera", "n": 9, "winner": "draw", "t0": 1, "t1": 1, "t2": -1, "t3": -1, "t4": -1, "t5": 1, "t6": 1, "t7": -1, "t8": 1}
{"id": 2, "j1": "fera", "v": 0, "j2": "fera", "n": 9, "winner": "draw", "t0": 1, "t1": 1, "t2": -1, "t3": -1, "t4": -1, "t5": 1, "t6": 1, "t7": -1, "t8": 1}
{"id": 3, "j1": "fera", "v": 0, "j2": "fera", "n": 9, "winner": "draw", "t0": 1, "t1": 1, "t2": -1, "t3": -1, "t4": -1, "t5": 1, "t6": 1, "t7": -1, "t8": 1}
{"id": 4, "j1": "fera", "v": 0, "j2": "fera", "n": 9, "winner": "draw", "t0": 1, "t1": 1, "t2": -1, "t3": -1, "t4": -1, "t5": 1, "t6": 1, "t7": -1, "t8": 1}
{"id": 5, "j1": "fera", "v": 0, "j2": "fera", "n": 9, "winner": "draw", "t0": 1, "t1": 1, "t2": -1, "t3": -1, "t4": -1, "t5": 1, "t6": 1, "t7": -1, "t8": 1}
```
