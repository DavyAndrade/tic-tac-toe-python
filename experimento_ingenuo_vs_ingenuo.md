# Experimento: ingenuo vs ingenuo

**Rodadas:** 100,000
**Ordem:** alternada (J1 e J2 trocam posicao)
**Semente:** 42
**Tempo:** 1.76s

## Resultado

| Algoritmo | V (vitorias) | D (derrotas) | E (empates) |
|-----------|-------------|-------------|-------------|
| ingenuo | 87146 | 87146 | 25708 |
| ingenuo | 87146 | 87146 | 25708 |

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
{"id": 1, "j1": "ingenuo", "v": 1, "j2": "ingenuo", "n": 7, "winner": "ingenuo", "t0": -1, "t1": 0, "t2": -1, "t3": 1, "t4": 1, "t5": 1, "t6": 0, "t7": 1, "t8": -1}
{"id": 2, "j1": "ingenuo", "v": 1, "j2": "ingenuo", "n": 9, "winner": "ingenuo", "t0": 1, "t1": 1, "t2": 1, "t3": 1, "t4": -1, "t5": -1, "t6": -1, "t7": -1, "t8": 1}
{"id": 3, "j1": "ingenuo", "v": 0, "j2": "ingenuo", "n": 9, "winner": "draw", "t0": 1, "t1": 1, "t2": -1, "t3": -1, "t4": 1, "t5": 1, "t6": 1, "t7": -1, "t8": -1}
{"id": 4, "j1": "ingenuo", "v": 1, "j2": "ingenuo", "n": 9, "winner": "ingenuo", "t0": 1, "t1": -1, "t2": -1, "t3": 1, "t4": 1, "t5": 1, "t6": -1, "t7": 1, "t8": -1}
{"id": 5, "j1": "ingenuo", "v": 1, "j2": "ingenuo", "n": 9, "winner": "ingenuo", "t0": -1, "t1": -1, "t2": 1, "t3": 1, "t4": -1, "t5": 1, "t6": -1, "t7": 1, "t8": 1}
```
