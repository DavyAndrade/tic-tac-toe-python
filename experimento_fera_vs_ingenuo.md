# Experimento: fera vs ingenuo

**Algoritmos:**
- `fera` — Jogador 1 (X, primeiro)
- `ingenuo` — Jogador 2 (O, segundo)

**Configuracao:**
- Sem alternancia (J1 = X sempre)
- Semente: 42

## Resultados progressivos

| Rodadas | V (vitorias) | D (derrotas) | E (empates) | Tempo |
|---------|-------------|-------------|-------------|-------|
| 100,000 | 99,474 | 0 | 526 | 1.26s |
| 200,000 | 198,934 | 0 | 1,066 | 2.52s |
| 300,000 | 298,444 | 0 | 1,556 | 3.78s |
| 400,000 | 397,925 | 0 | 2,075 | 4.98s |
| 500,000 | 497,419 | 0 | 2,581 | 6.42s |
| 600,000 | 596,926 | 0 | 3,074 | 7.83s |
| 700,000 | 696,409 | 0 | 3,591 | 9.12s |
| 800,000 | 795,875 | 0 | 4,125 | 10.45s |
| 900,000 | 895,349 | 0 | 4,651 | 11.62s |
| 1,000,000 | 994,852 | 0 | 5,148 | 12.85s |

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
{"id": 1, "j1": 1, "v": 0, "j2": 0, "n": 5, "winner": 1, "j1_name": "fera", "j2_name": "ingenuo", "t0": 1, "t1": 1, "t2": 1, "t3": -1, "t4": 0, "t5": 0, "t6": 0, "t7": 0, "t8": -1}
{"id": 2, "j1": 1, "v": 0, "j2": 0, "n": 5, "winner": 1, "j1_name": "fera", "j2_name": "ingenuo", "t0": 1, "t1": 1, "t2": 1, "t3": 0, "t4": -1, "t5": 0, "t6": 0, "t7": 0, "t8": -1}
{"id": 3, "j1": 1, "v": 0, "j2": 0, "n": 5, "winner": 1, "j1_name": "fera", "j2_name": "ingenuo", "t0": 1, "t1": 1, "t2": 1, "t3": 0, "t4": 0, "t5": -1, "t6": -1, "t7": 0, "t8": 0}
{"id": 4, "j1": 1, "v": 0, "j2": 0, "n": 5, "winner": 1, "j1_name": "fera", "j2_name": "ingenuo", "t0": 1, "t1": 1, "t2": 1, "t3": -1, "t4": -1, "t5": 0, "t6": 0, "t7": 0, "t8": 0}
{"id": 5, "j1": 1, "v": 0, "j2": 0, "n": 5, "winner": 1, "j1_name": "fera", "j2_name": "ingenuo", "t0": 1, "t1": 1, "t2": 1, "t3": 0, "t4": -1, "t5": -1, "t6": 0, "t7": 0, "t8": 0}
```
