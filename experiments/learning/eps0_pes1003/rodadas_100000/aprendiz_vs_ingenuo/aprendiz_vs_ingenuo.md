# Experimento: aprendiz vs ingenuo (100.000 rodadas)

**Configuracao:**
- X (J1): `aprendiz`
- O (J2): `ingenuo`
- Semente: 42
- Rodadas: 100.000
- Recompensa: vitoria +10, empate +0, derrota -3
- epsilon: 0.0 (exploracao apenas pelo desempate aleatorio de estados zerados)

Dados: `experiments/learning/eps0_pes1003/rodadas_100000/aprendiz_vs_ingenuo/`

## Resultado acumulado

| Partida | J1 | V | J2 |
|---------|----|---|----|
| 1.000 | 763 | 91 | 146 |
| 10.000 | 7.958 | 820 | 1.222 |
| 50.000 | 39.925 | 4.071 | 6.004 |
| 100.000 | 79.809 | 8.135 | 12.056 |

## Evolucao por janela de 10,000 partidas (aprendiz = J1)

| Janela | V | E | D | Aproveitamento (V+E) |
|--------|---|---|---|----------------------|
| 1-10.000 | 7.958 | 820 | 1.222 | 87.8% |
| 10.001-20.000 | 7.973 | 809 | 1.218 | 87.8% |
| 20.001-30.000 | 7.995 | 828 | 1.177 | 88.2% |
| 30.001-40.000 | 7.971 | 809 | 1.220 | 87.8% |
| 40.001-50.000 | 8.028 | 805 | 1.167 | 88.3% |
| 50.001-60.000 | 8.024 | 793 | 1.183 | 88.2% |
| 60.001-70.000 | 7.979 | 807 | 1.214 | 87.9% |
| 70.001-80.000 | 7.960 | 815 | 1.225 | 87.8% |
| 80.001-90.000 | 7.960 | 824 | 1.216 | 87.8% |
| 90.001-100.000 | 7.961 | 825 | 1.214 | 87.9% |

Leitura: plano do fim ao fim (87,8–88,3%). Empates caem para ~813/janela
(vs ~1.350 com empate +1) e derrotas ficam ~1.200/janela.

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 235 | 398.244 |

Abertura 100% `canto0`, 0 migracoes; 2a jogada do X equilibrada
({2:25.220, 4:24.812, 6:25.182, 8:24.786}); todos os estados descobertos na
janela 0, +0 depois.

## Grafico

`progress.svg` — series `J1 (Aprendiz)` / `V` / `J2 (Ingenuo)` por partida.

## Arquivos

```
experiments/learning/eps0_pes1003/rodadas_100000/aprendiz_vs_ingenuo/
├── episodes.jsonl    # cada decisao (estado, acao), resultado, recompensa
├── progress.jsonl    # linha 0 + 1 linha por partida (100.001 linhas)
├── q_table.json      # snapshot da tabela Q (schema_version 1)
├── progress.svg      # grafico acumulado
└── aprendiz_vs_ingenuo.md    # este relatorio
```

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --rounds 100000 \
  --scenario aprendiz_vs_ingenuo --root experiments/learning/eps0_pes1003
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/eps0_pes1003/rodadas_100000/aprendiz_vs_ingenuo/progress.jsonl \
  --partida 100000
```

## Analise — perguntas do experimento

**O que aconteceu com o desempenho do Inteligente conforme aumentou o numero de partidas?**
Plano: 87,8% de aproveitamento (V+E) na primeira janela, 87,9% na última.
Total 79.809V / 8.135E / 12.056D (79,8% de vitorias; 87,9% sem derrota).

**Em que trecho do grafico ocorreu a mudanca mais importante?**
Nenhuma — variação entre janelas abaixo de 0,5pp; epsilon 0 converge antes da
partida 10.000 e o restante e repeticao deterministica.

**O Inteligente chegou a parar de perder? Se sim, aproximadamente depois de quantas partidas?**
Nao. Ultima derrota na partida 99.997, com ~1.200 derrotas por janela de 10
mil ate o fim.

**Depois de observar este resultado, o que voces decidiram testar ou alterar na proxima execucao?**
Ver `relatorio_100k_comparativo.md` na raiz do config — serie completa de
pesos 10x fechada; baseline 2/1/−5 segue campea.
