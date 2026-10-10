# Experimento: aprendiz vs ingenuo (500.000 rodadas)

**Configuracao:**
- X (J1): `aprendiz`
- O (J2): `ingenuo`
- Semente: 42
- Rodadas: 500.000
- Recompensa: vitoria +10, empate +1, derrota -3
- epsilon: 0.0 (exploracao apenas pelo desempate aleatorio de estados zerados)

Dados: `experiments/learning/eps0_pes1013/rodadas_500000/aprendiz_vs_ingenuo/`
(episodes/progress jsonl locais — regeneraveis por seed 42; versionados:
q_table.json, progress.svg, este relatorio)

## Resultado acumulado

| Partida | J1 | V | J2 |
|---------|----|---|----|
| 100.000 | 75.348 | 13.545 | 11.107 |
| 500.000 | 377.529 | 67.469 | 55.002 |

75,5% de vitorias, 89,0% sem derrota — mesmas taxas do 100k (75,3% / 88,9%);
os primeiros 100k sao identicos ao `rodadas_100000` (seed 42 deterministica).

## Evolucao por janela de 50.000 partidas (aprendiz = J1)

| Janela | V | E | D | Aproveitamento (V+E) |
|--------|---|---|---|----------------------|
| 1-50.000 | 37.736 | 6.755 | 5.509 | 89.0% |
| 50.001-100.000 | 37.612 | 6.790 | 5.598 | 88.8% |
| 100.001-150.000 | 37.700 | 6.702 | 5.598 | 88.8% |
| 150.001-200.000 | 37.872 | 6.714 | 5.414 | 89.2% |
| 200.001-250.000 | 37.720 | 6.838 | 5.442 | 89.1% |
| 250.001-300.000 | 38.041 | 6.555 | 5.404 | 89.2% |
| 300.001-350.000 | 37.677 | 6.779 | 5.544 | 88.9% |
| 350.001-400.000 | 37.700 | 6.760 | 5.540 | 88.9% |
| 400.001-450.000 | 37.690 | 6.847 | 5.463 | 89.1% |
| 450.001-500.000 | 37.781 | 6.729 | 5.490 | 89.0% |

## Para de perder? (criterio principal)

| Metrica | Valor |
|---------|-------|
| Janelas de 1.000 jogos com ZERO derrotas | **0 de 500** |
| Derrotas por janela de 1.000 — 5 primeiras | 136, 141, 110, 105, 108 |
| Derrotas por janela de 1.000 — 5 ultimas | 114, 107, 116, 109, 103 |
| Maior sequencia sem derrota | 96 jogos (termina p143.588) |
| Ultima derrota | **p499.998** |

**Nao para.** Taxa estavel em ~110 derrotas por mil do primeiro ao ultimo
jogo — nenhuma tendencia de queda entre o inicio e o fim das 500k. Mesmo
veredito de todas as execucoes de pesos puros; so o curriculo epsilon
(0,25→0) zerou derrotas, na virada p499.989.

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 224 | 2.014.947 |

Mesmos 224 estados do 100k (zero crescimento em 400k partidas extras);
abertura 100% `canto0`; 0 migracoes.

## Grafico

`progress.svg` — series `J1 (Aprendiz)` / `V` / `J2 (Ingenuo)` por partida.

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Nada: 89,0% sem derrota em todas as janelas de 50k (88,8–89,2%).

**Em que trecho do grafico ocorreu a mudanca mais importante?**
Nenhuma — politica congelada antes da partida 10.000.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Nao. Ultima derrota p499.998; 0 janelas de 1.000 sem derrota em 500k.

**Depois de observar este resultado, o que voces decidiram testar ou alterar na proxima execucao?**
500k fecha a pergunta para 10/1/−3: escala de partidas nao produz o ponto de
"para de perder" — o que produziu (nao demonstrado) foi so o curriculo
epsilon. Ver `relatorio_100k_comparativo.md` para o comparativo de pesos.
