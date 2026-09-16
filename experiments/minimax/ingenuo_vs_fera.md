# Experimento: ingenuo vs fera

**Algoritmos:**
- `ingenuo` — Jogador 1 (X, primeiro)
- `fera` — Jogador 2 (O, segundo)

**Configuracao:**
- Sem alternancia (J1 = X sempre)
- Semente: 42

## Resultados progressivos

| Rodadas | V (vitorias) | D (derrotas) | E (empates) | Tempo |
|---------|-------------|-------------|-------------|-------|
| 100,000 | 0 | 80,559 | 19,441 | 1.49s |
| 200,000 | 0 | 161,281 | 38,719 | 3.05s |
| 300,000 | 0 | 241,827 | 58,173 | 4.66s |
| 400,000 | 0 | 322,586 | 77,414 | 6.17s |
| 500,000 | 0 | 403,447 | 96,553 | 7.88s |
| 600,000 | 0 | 484,152 | 115,848 | 9.48s |
| 700,000 | 0 | 564,962 | 135,038 | 10.82s |
| 800,000 | 0 | 645,604 | 154,396 | 12.70s |
| 900,000 | 0 | 726,308 | 173,692 | 13.94s |
| 1,000,000 | 0 | 807,087 | 192,913 | 15.85s |

## Formato de cada partida

```json
{
  "id": "inteiro sequencial",
  "j1": "0 ou 1 (1 = J1 venceu)",
  "v": "0 ou 1 (1 = empate/velha)",
  "j2": "0 ou 1 (1 = J2 venceu)",
  "winner": "1 = J1, -1 = J2, 0 = empate",
  "n": "numero de jogadas",
  "j1_name": "nome da estrategia J1",
  "j2_name": "nome da estrategia J2",
  "t0".."t8": "1 = marca J1, 0 = vazio, -1 = marca J2"
}
```

## Amostra (ultima rodada - 5 partidas)

```json
{"id": 1, "j1": 0, "v": 1, "j2": 0, "n": 9, "winner": 0, "j1_name": "ingenuo", "j2_name": "fera", "t0": 1, "t1": -1, "t2": 1, "t3": -1, "t4": 1, "t5": 1, "t6": -1, "t7": 1, "t8": -1}
{"id": 2, "j1": 0, "v": 0, "j2": 1, "n": 6, "winner": -1, "j1_name": "ingenuo", "j2_name": "fera", "t0": -1, "t1": -1, "t2": -1, "t3": 1, "t4": 0, "t5": 0, "t6": 0, "t7": 1, "t8": 1}
{"id": 3, "j1": 0, "v": 1, "j2": 0, "n": 9, "winner": 0, "j1_name": "ingenuo", "j2_name": "fera", "t0": 1, "t1": 1, "t2": -1, "t3": -1, "t4": 1, "t5": 1, "t6": 1, "t7": -1, "t8": -1}
{"id": 4, "j1": 0, "v": 0, "j2": 1, "n": 6, "winner": -1, "j1_name": "ingenuo", "j2_name": "fera", "t0": -1, "t1": 0, "t2": 1, "t3": 1, "t4": -1, "t5": 0, "t6": 0, "t7": 1, "t8": -1}
{"id": 5, "j1": 0, "v": 1, "j2": 0, "n": 9, "winner": 0, "j1_name": "ingenuo", "j2_name": "fera", "t0": -1, "t1": -1, "t2": 1, "t3": 1, "t4": 1, "t5": -1, "t6": -1, "t7": 1, "t8": 1}
```
