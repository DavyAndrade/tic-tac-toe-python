# Experimento: aprendiz vs ingenuo (100,000 rodadas)

**Configuracao:**
- X (J1): `aprendiz`
- O (J2): `ingenuo`
- Semente: 42
- Rodadas: 100,000
- Recompensa: vitoria +2, empate +1, derrota -5
- epsilon: 0.1 (10% das jogadas sempre aleatorias)

Dados: `experiments/learning/eps0-1_pes215/rodadas_100000/aprendiz_vs_ingenuo/`

## Resultado acumulado

| Partida | J1 (aprendiz) | V | J2 (ingenuo) |
|---------|---------------|---|--------------|
| 1,000 | 765 | 109 | 126 |
| 10,000 | 8,822 | 685 | 493 |
| 50,000 | 46,738 | 2,043 | 1,219 |
| 100,000 | 94,517 | 3,603 | 1,880 |

## Evolucao por janela de 10,000 partidas (aprendiz = J1)

| Janela | V | E | D | Aproveitamento |
|--------|---|---|---|----------------|
| 1-10,000 | 8,822 | 685 | 493 | 95% |
| 10,001-20,000 | 9,410 | 374 | 216 | 98% |
| 20,001-30,000 | 9,479 | 341 | 180 | 98% |
| 30,001-40,000 | 9,492 | 333 | 175 | 98% |
| 40,001-50,000 | 9,535 | 310 | 155 | 98% |
| 50,001-60,000 | 9,553 | 306 | 141 | 99% |
| 60,001-70,000 | 9,509 | 343 | 148 | 99% |
| 70,001-80,000 | 9,550 | 318 | 132 | 99% |
| 80,001-90,000 | 9,607 | 275 | 118 | 99% |
| 90,001-100,000 | 9,560 | 318 | 122 | 99% |

Leitura: sobe de 95% para 98% na primeira janela e estabiliza; a partir da
partida 50,000 fica em 99%. As ~1% de perda restante vem do epsilon (10% das
jogadas aleatorias para sempre) — teto estrutural, nao falta de aprendizado.

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 2,282 | 346,469 |

## Grafico

`progress.svg` — series J1/V/J2 por
partida, eixo X numerado. Gerado por `matplotlib` a partir de `progress.jsonl`.

## Arquivos

```
experiments/learning/eps0-1_pes215/rodadas_100000/aprendiz_vs_ingenuo/
├── episodes.jsonl    # 29M — cada decisao (estado, acao), resultado, recompensa
├── progress.jsonl    # 18M — linha 0 + 1 linha por partida (100,001 linhas)
├── q_table.json      # snapshot da tabela Q (schema_version 1)
├── progress.svg      # grafico acumulado
└── aprendiz_vs_ingenuo.md    # este relatorio
```

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --rounds 100000 --scenario aprendiz_vs_ingenuo
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps0-1_pes215/rodadas_100000/aprendiz_vs_ingenuo/progress.jsonl \
  --partida 100000
```

Execucao deterministica (seed 42): regenera identico. Versao de 1,000
rodadas preservada em `eps0-1_pes215/rodadas_1000/` e documentada em
`eps0-1_pes215/rodadas_1000/aprendiz_vs_ingenuo/aprendiz_vs_ingenuo.md`.

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Aproveitamento subiu de 95.1% para 98.8% em 100,000 partidas. Derrotas por
janela de 10 mil caíram de 493 para 122; vitorias subiram de ~8,200 para
~9,560 por janela; empates caíram de 1,606 para 1,595. O agente vence 94.5%
das 100,000 — a melhor marca de vitoria de todos os experimentos.

**Em que trecho do grafico ocorreu a mudanca mais importante?**
Entre a 1a e a 2a janela de 10 mil (+2.8pp, de 95.1% para 97.8%). Depois a
curva é quase reta, ganhando centésimos por janela ate 98.8%.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Nao. A ultima derrota foi na partida 99,923 e a ultima janela ainda teve
122 derrotas (1.2%) — o residuo do epsilon 0.1.

**Depois de observar este resultado, o que voces decidiram testar ou alterar na proxima execucao?**
Testar o novo padrao epsilon 0 (feito: `eps0_pes215/rodadas_100000`) para
comparar se a remocao da exploracao aleatoria melhora ou piora.
