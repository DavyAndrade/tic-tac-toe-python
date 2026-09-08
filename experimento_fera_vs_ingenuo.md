# Experimento: fera vs ingenuo

**Rodadas:** 100,000
**Ordem:** alternada (J1 e J2 trocam posicao)
**Semente:** 42
**Tempo:** 1.51s

## Resultado

| Algoritmo | V (vitorias) | D (derrotas) | E (empates) |
|-----------|-------------|-------------|-------------|
| fera | 90020 | 0 | 9980 |
| ingenuo | 0 | 90020 | 9980 |

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

## Amostra (primeiras 5 partidas)

```json
{"id": 1, "j1": "fera", "v": 1, "j2": "ingenuo", "n": 5, "winner": "fera", "t0": 1, "t1": 1, "t2": 1, "t3": -1, "t4": 0, "t5": 0, "t6": 0, "t7": 0, "t8": -1}
{"id": 2, "j1": "ingenuo", "v": 0, "j2": "fera", "n": 6, "winner": "fera", "t0": -1, "t1": -1, "t2": -1, "t3": 1, "t4": 0, "t5": 0, "t6": 0, "t7": 1, "t8": 1}
{"id": 3, "j1": "fera", "v": 1, "j2": "ingenuo", "n": 5, "winner": "fera", "t0": 1, "t1": 1, "t2": 1, "t3": 0, "t4": 0, "t5": -1, "t6": -1, "t7": 0, "t8": 0}
{"id": 4, "j1": "ingenuo", "v": 0, "j2": "fera", "n": 6, "winner": "fera", "t0": -1, "t1": 0, "t2": 1, "t3": 1, "t4": -1, "t5": 0, "t6": 0, "t7": 1, "t8": -1}
{"id": 5, "j1": "fera", "v": 1, "j2": "ingenuo", "n": 5, "winner": "fera", "t0": 1, "t1": 1, "t2": 1, "t3": 0, "t4": -1, "t5": -1, "t6": 0, "t7": 0, "t8": 0}
```
