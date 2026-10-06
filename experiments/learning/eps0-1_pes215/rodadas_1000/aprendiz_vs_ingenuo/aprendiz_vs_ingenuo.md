# Experimento: aprendiz vs ingenuo

**Configuracao:**
- X (J1): `aprendiz`
- O (J2): `ingenuo`
- Semente: 42
- Rodadas: 1,000
- Recompensa: vitoria +2, empate +1, derrota -5
- epsilon: 0.1 (10% das jogadas sempre aleatorias)

## Resultado acumulado

| Partida | J1 (aprendiz) | V | J2 (ingenuo) |
|---------|---------------|---|--------------|
| 100 | 67 | 10 | 23 |
| 500 | 367 | 57 | 76 |
| 1,000 | 765 | 109 | 126 |

## Evolucao por janela de 100 partidas (aprendiz = J1)

| Janela | V | E | D | Aproveitamento |
|--------|---|---|---|----------------|
| 1-100 | 67 | 10 | 23 | 77% |
| 101-200 | 65 | 17 | 18 | 82% |
| 201-300 | 80 | 8 | 12 | 88% |
| 301-400 | 72 | 11 | 17 | 83% |
| 401-500 | 83 | 11 | 6 | 94% |
| 501-600 | 81 | 7 | 12 | 88% |
| 601-700 | 77 | 10 | 13 | 87% |
| 701-800 | 81 | 11 | 8 | 92% |
| 801-900 | 78 | 12 | 10 | 90% |
| 901-1000 | 81 | 12 | 7 | 93% |

Leitura: aproveitamento sobe de 77% para ~93% e estabiliza por volta da
partida 400. O teto parcial vem do epsilon: 10% das jogadas sao aleatorias
para sempre, entao o agente nunca chega a 100%.

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 809 | 3,991 |

## Grafico

`progress.svg` — series J1/V/J2 por partida, eixo X numerado de 100 em 100.
Gerado por `matplotlib` a partir de `progress.jsonl`.

## Arquivos

```
experiments/learning/eps0-1_pes215/rodadas_1000/aprendiz_vs_ingenuo/
├── episodes.jsonl    # cada decisao (estado, acao), resultado, recompensa
├── progress.jsonl    # linha 0 + 1 linha por partida
├── q_table.json      # snapshot da tabela Q (schema_version 1)
├── progress.svg      # grafico acumulado
└── aprendiz_vs_ingenuo.md    # este relatorio
```

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --rounds 1000 --scenario aprendiz_vs_ingenuo
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps0-1_pes215/rodadas_1000/aprendiz_vs_ingenuo/progress.jsonl \
  --partida 1000
```

Execucao deterministica (seed 42): regenera identico.

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Aproveitamento subiu de 77% (primeiras 100) para 93% (ultimas 100), com
oscilacao: 83% na quarta janela, 94% na quinta, de novo 87% na setima.
Derrotas por janela caíram de 23 para 7; vitorias oscilaram entre 65 e 82;
empates entre 10 e 21.

**Em que trecho do grafico ocorreu a mudanca mais importante?**
Inicio rapido com oscilacoes — maior salto entre a 4a e a 5a janela
(+11pp, de 83% para 94%). Depois a curva oscila em 87-93% sem tendência
clara: o epsilon 0.1 mantem ruido em toda a execucao.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Nao. A ultima derrota foi na partida 991 e as 100 finais ainda tiveram 7
derrotas (e 4 na janela 801-900). O teto de ~7% de derrota vem do epsilon
0.1, que joga 10% das jogadas ao acaso para sempre.

**Depois de observar este resultado, o que voces decidiram testar ou alterar na proxima execucao?**
Escalar o treino para 100,000 partidas (feito: `eps0-1_pes215/rodadas_100000`)
para ver se a oscilacao estabiliza.
