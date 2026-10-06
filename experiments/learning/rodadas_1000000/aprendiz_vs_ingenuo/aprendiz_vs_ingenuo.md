# Experimento: aprendiz vs ingenuo (1,000,000 rodadas)

**Configuracao:**
- X (J1): `aprendiz`
- O (J2): `ingenuo`
- Semente: 42
- Rodadas: 1,000,000
- Recompensa: vitoria +2, empate +1, derrota -5
- **epsilon: 0.0** — padrao congelado para todos os experimentos a partir
  desta rodada (exploracao so pelo desempate aleatorio de estados zerados,
  EC-003)

Dados: `experiments/learning/rodadas_1000000/aprendiz_vs_ingenuo/`

## Resultado acumulado

| Partida | J1 (aprendiz) | V | J2 (ingenuo) |
|---------|---------------|---|--------------|
| 1,000 | 764 | 156 | 80 |
| 100,000 | 82,513 | 16,018 | 1,469 |
| 500,000 | 412,814 | 80,512 | 6,674 |
| 1,000,000 | 825,711 | 161,082 | 13,207 |

## Evolucao por janela de 100,000 partidas (aprendiz = J1)

| Janela | V | E | D | Aproveitamento |
|--------|---|---|---|----------------|
| 1-100,000 | 82,513 | 16,018 | 1,469 | 98.5% |
| 100,001-200,000 | 82,721 | 16,002 | 1,277 | 98.7% |
| 200,001-300,000 | 82,656 | 16,066 | 1,278 | 98.7% |
| 300,001-400,000 | 82,377 | 16,309 | 1,314 | 98.7% |
| 400,001-500,000 | 82,547 | 16,117 | 1,336 | 98.7% |
| 500,001-600,000 | 82,564 | 16,130 | 1,306 | 98.7% |
| 600,001-700,000 | 82,516 | 16,183 | 1,301 | 98.7% |
| 700,001-800,000 | 82,486 | 16,145 | 1,369 | 98.6% |
| 800,001-900,000 | 82,559 | 16,164 | 1,277 | 98.7% |
| 900,001-1,000,000 | 82,772 | 15,948 | 1,280 | 98.7% |

Leitura: **platol**. As janelas ficam em 98.6-98.7% do primeiro ao ultimo
bloco — 10x mais partidas nao mudam nada. O primeiro bloco de 100,000 e
prefixo identico ao de `experiments/learning/rodadas_100000_eps0/` (mesma
cadeia de seeds), confirmando determinismo.

Causa do platol: a tabela Q tem **300 estados** — exatamente os mesmos 300 do
experimento de 100,000. Com epsilon 0 o agente nao visita nada fora das linhas
que ja conhece; mais rodadas apenas repetem a politica. Comparar com o baseline
epsilon 0.1 (100k, historico do Git): 2,282 estados e 94.5% de vitorias — a
exploracao aleatoria cobria muito mais do espaco.

## Tabela Q final

| Estados | Visitas |
|---------|---------|
| 300 | 4,028,016 |

## Grafico

`progress.svg` — series `J1 (Aprendiz)` / `V` / `J2 (Ingenuo)` por partida.
Gerado por `matplotlib` a partir de `progress.jsonl`.

## Arquivos

```
experiments/learning/rodadas_1000000/aprendiz_vs_ingenuo/
├── episodes.jsonl    # 316M — LOCAL, fora do Git (limite 100MB do GitHub)
├── progress.jsonl    # 185M — LOCAL, fora do Git
├── q_table.json      # versionado
├── progress.svg      # versionado
└── aprendiz_vs_ingenuo.md    # este relatorio (versionado)
```

Os JSONLs grandes ficam locais e sao regeneraveis identicos (seed 42).

## Reproduzir e consultar

```bash
.venv/bin/python run_aprendizado.py --rounds 1000000 --scenario aprendiz_vs_ingenuo
.venv/bin/python run_aprendizado.py \
  --progress experiments/learning/rodadas_1000000/aprendiz_vs_ingenuo/progress.jsonl \
  --partida 1000000
```
