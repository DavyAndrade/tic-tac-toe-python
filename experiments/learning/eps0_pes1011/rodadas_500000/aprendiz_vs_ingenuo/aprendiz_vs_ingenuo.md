# Experimento: aprendiz vs ingenuo (500.000 rodadas)

**Configuracao:**
- X (J1): `aprendiz`
- O (J2): `ingenuo`
- Semente: 42
- Rodadas: 500.000
- Recompensa: vitoria +10, empate +1, derrota -1
- epsilon: 0.0 (exploracao apenas pelo desempate aleatorio de estados zerados)

Dados: `experiments/learning/eps0_pes1011/rodadas_500000/aprendiz_vs_ingenuo/`
(episodes/progress jsonl locais — regeneraveis por seed 42; versionados:
q_table.json, progress.svg, este relatorio)

## Resultado acumulado

| Partida | J1 | V | J2 |
|---------|----|---|----|
| 1.000 | 710 | 140 | 150 |
| 100.000 | 73.234 | 14.078 | 12.688 |
| 500.000 | 368.694 | 69.192 | 62.114 |

Os 100.000 primeiros sao byte a byte identicos ao `rodadas_100000` do mesmo
config (execucao deterministica seed 42).

## Evolucao por janela de 50.000 partidas (aprendiz = J1)

| Janela | V | E | D | Aproveitamento (V+E) |
|--------|---|---|---|----------------------|
| 1-50.000 | 36.660 | 7.044 | 6.296 | 87.4% |
| 50.001-100.000 | 36.574 | 7.034 | 6.392 | 87.2% |
| 100.001-150.000 | 36.687 | 6.937 | 6.376 | 87.2% |
| 150.001-200.000 | 36.877 | 6.910 | 6.213 | 87.6% |
| 200.001-250.000 | 36.858 | 6.972 | 6.170 | 87.7% |
| 250.001-300.000 | 37.292 | 6.639 | 6.069 | 87.9% |
| 300.001-350.000 | 36.906 | 6.898 | 6.196 | 87.6% |
| 350.001-400.000 | 36.890 | 6.918 | 6.192 | 87.6% |
| 400.001-450.000 | 36.931 | 6.975 | 6.094 | 87.8% |
| 450.001-500.000 | 37.019 | 6.865 | 6.116 | 87.8% |

Leitura: perfeitamente plano (87,2–87,9%). 5x partidas nao moveu nada —
confirmacao em escala do que o 100k ja mostrava.

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 220 | 2.024.424 |

**Mesmos 220 estados do 100k** — zero crescimento da tabela em 400k partidas
extras. Abertura 100% `canto0`, 0 migracoes; nenhum estado novo descoberto apos
a janela 0.

## Grafico

`progress.svg` — series `J1 (Aprendiz)` / `V` / `J2 (Ingenuo)` por partida.

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Nada: 73,7% de vitorias e 87,6% sem derrota no acumulado de 500k, contra 73,2%
e 87,3% nos primeiros 100k. Janela a janela oscila 0,7pp.

**Em que trecho do grafico ocorreu a mudanca mais importante?**
Em nenhum — e o proprio resultado: com epsilon 0 a politica congela antes da
partida 10.000; as 500k linhas sao a mesma jogada repetida.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Nao. Ultima derrota na partida 499.998, ~6.200 derrotas por janela de 50 mil
ate o fim.

**Depois de observar este resultado, o que voces decidiram testar ou alterar na proxima execucao?**
500k com pesos 10/1/−1 e informativo e encerra a questao "mais partidas
melhora?": nao. O gap para o baseline 2/1/−5 (82,5% de vitorias, 98,5% sem
derrota em 100k; 98,7% em 1M) e estrutural na recompensa, nao de amostragem.
