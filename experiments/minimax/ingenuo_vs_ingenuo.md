# Experimento: ingenuo vs ingenuo

**Algoritmos:**
- `ingenuo` — Jogador 1 (X, primeiro)
- `ingenuo` — Jogador 2 (O, segundo)

**Configuracao:**
- Sem alternancia (J1 = X sempre)
- Semente: 42

## Resultados progressivos

| Rodadas | V (vitorias) | D (derrotas) | E (empates) | Tempo |
|---------|-------------|-------------|-------------|-------|
| 100,000 | 87,146 | 87,146 | 25,708 | 1.74s |
| 200,000 | 174,565 | 174,565 | 50,870 | 3.55s |
| 300,000 | 261,953 | 261,953 | 76,094 | 5.29s |
| 400,000 | 349,500 | 349,500 | 101,000 | 7.15s |
| 500,000 | 436,892 | 436,892 | 126,216 | 9.19s |
| 600,000 | 524,113 | 524,113 | 151,774 | 10.84s |
| 700,000 | 611,558 | 611,558 | 176,884 | 13.14s |
| 800,000 | 698,843 | 698,843 | 202,314 | 14.49s |
| 900,000 | 786,136 | 786,136 | 227,728 | 16.10s |
| 1,000,000 | 873,413 | 873,413 | 253,174 | 18.24s |

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
{"id": 1, "j1": 1, "v": 0, "j2": 0, "n": 7, "winner": 1, "j1_name": "ingenuo", "j2_name": "ingenuo", "t0": -1, "t1": 0, "t2": -1, "t3": 1, "t4": 1, "t5": 1, "t6": 0, "t7": 1, "t8": -1}
{"id": 2, "j1": 1, "v": 0, "j2": 0, "n": 9, "winner": 1, "j1_name": "ingenuo", "j2_name": "ingenuo", "t0": 1, "t1": 1, "t2": 1, "t3": 1, "t4": -1, "t5": -1, "t6": -1, "t7": -1, "t8": 1}
{"id": 3, "j1": 0, "v": 1, "j2": 0, "n": 9, "winner": 0, "j1_name": "ingenuo", "j2_name": "ingenuo", "t0": 1, "t1": 1, "t2": -1, "t3": -1, "t4": 1, "t5": 1, "t6": 1, "t7": -1, "t8": -1}
{"id": 4, "j1": 1, "v": 0, "j2": 0, "n": 9, "winner": 1, "j1_name": "ingenuo", "j2_name": "ingenuo", "t0": 1, "t1": -1, "t2": -1, "t3": 1, "t4": 1, "t5": 1, "t6": -1, "t7": 1, "t8": -1}
{"id": 5, "j1": 1, "v": 0, "j2": 0, "n": 9, "winner": 1, "j1_name": "ingenuo", "j2_name": "ingenuo", "t0": -1, "t1": -1, "t2": 1, "t3": 1, "t4": -1, "t5": 1, "t6": -1, "t7": 1, "t8": 1}
```
