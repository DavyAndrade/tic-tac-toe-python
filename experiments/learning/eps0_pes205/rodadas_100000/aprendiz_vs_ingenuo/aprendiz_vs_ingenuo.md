# Experimento: aprendiz vs ingenuo (100.000 rodadas)

**Configuracao:**
- X (J1): `aprendiz`
- O (J2): `ingenuo`
- Semente: 42
- Rodadas: 100.000
- Recompensa: vitoria +2, empate +0, derrota -5
- epsilon: 0.0 (exploracao apenas pelo desempate aleatorio de estados zerados)

Dados: `experiments/learning/eps0_pes205/rodadas_100000/aprendiz_vs_ingenuo/`

## Resultado acumulado

| Partida | J1 | V | J2 |
|---------|----|---|----|
| 1.000 | 775 | 121 | 104 |
| 10.000 | 8.654 | 1.074 | 272 |
| 50.000 | 43.952 | 5.105 | 943 |
| 100.000 | 88.066 | 10.150 | 1.784 |

## Evolucao por janela de 10,000 partidas (aprendiz = J1)

| Janela | V | E | D | Aproveitamento (V+E) |
|--------|---|---|---|----------------------|
| 1-10.000 | 8.654 | 1.074 | 272 | 97.3% |
| 10.001-20.000 | 8.812 | 1.031 | 157 | 98.4% |
| 20.001-30.000 | 8.832 | 1.009 | 159 | 98.4% |
| 30.001-40.000 | 8.838 | 974 | 188 | 98.1% |
| 40.001-50.000 | 8.816 | 1.017 | 167 | 98.3% |
| 50.001-60.000 | 8.783 | 1.041 | 176 | 98.2% |
| 60.001-70.000 | 8.847 | 975 | 178 | 98.2% |
| 70.001-80.000 | 8.847 | 999 | 154 | 98.5% |
| 80.001-90.000 | 8.864 | 968 | 168 | 98.3% |
| 90.001-100.000 | 8.773 | 1.062 | 165 | 98.3% |

Leitura: primeira janela ja em 97,3% (janela fria de exploracao com272
derrotas), estavel em 98,1–98,5% depois. Empates ~1.000/janela (vs ~1.600 do
baseline com empate +1); derrotas ~170/janela (vs ~147 do baseline).

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 347 | 385.139 |

Abertura 100% `canto0`, 0 migracoes; 2a jogada do X em 5 celulas principais
({2:25.244, 4:24.820, 6:25.111, 7:12.403, 8:12.384}); todos os estados
descobertos na janela 0, +0 depois. Maior tabela Q de todos os pesos testados
(347 vs 300 do baseline).

## Grafico

`progress.svg` — series `J1 (Aprendiz)` / `V` / `J2 (Ingenuo)` por partida.

## Arquivos

```
experiments/learning/eps0_pes205/rodadas_100000/aprendiz_vs_ingenuo/
├── episodes.jsonl    # cada decisao (estado, acao), resultado, recompensa
├── progress.jsonl    # linha 0 + 1 linha por partida (100.001 linhas)
├── q_table.json      # snapshot da tabela Q (schema_version 1)
├── progress.svg      # grafico acumulado
└── aprendiz_vs_ingenuo.md    # este relatorio
```

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --rounds 100000 \
  --scenario aprendiz_vs_ingenuo --root experiments/learning/eps0_pes205
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps0_pes205/rodadas_100000/aprendiz_vs_ingenuo/progress.jsonl \
  --partida 100000
```

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Melhor de toda a serie: 86,5% de vitorias na primeira janela, 87,7% na ultima;
aproveitamento (V+E) de 97,3% a 98,3%. Total 88.066V / 10.150E / 1.784D
(88,1% de vitorias; 98,2% sem derrota).

**Em que trecho do grafico ocorreu a mudanca mais importante?**
A primeira janela (272 derrotas — mais que o dobro das demais ~170): e a fase
em que o greedy ainda fecha as contas. Depois disso o ritmo e constante.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Nao. Ultima derrota na partida 99.975; ~170 derrotas por janela ate o fim.
Nenhum arranjo de pesos puros zerou derrotas em 100k — apenas o curriculo
epsilon (`eps025_0_pes215`) chegou a 0D, e so na fase 2.

**Depois de observar este resultado, o que voces decidiram testar ou alterar na proxima execucao?**
Ver `relatorio_100k_comparativo.md` — empate 0 no baseline deu o maior salto
de vitorias da serie (+5,6pp) praticamente empatando o aproveitamento.
