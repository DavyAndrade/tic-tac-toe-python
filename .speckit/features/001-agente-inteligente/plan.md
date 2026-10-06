# Plano técnico — Agente Inteligente (001)

Brownfield: integração com código existente. O algoritmo fica em `algorithms/`; os runners apenas executam partidas e produzem evidências.

## 1. Algoritmo

### Núcleo — `algorithms/learning.py`

Manter `fera_aprendizado` existente. Adicionar `aprendiz` como estratégia online separada, sem treino automático no import.

Estado interno do novo agente:

```python
_Q[(board, player)][cell] = (value, visits)
_history[X] = [(state, action), ...]
_history[O] = [(state, action), ...]
_epsilon = 0.0  # decisão: exploração só pelo desempate aleatório (EC-003)
```

Responsabilidades do módulo:

- escolher ação ε-greedy;
- registrar estado e ação;
- calcular +2, +1 ou -5 do ponto de vista do agente;
- atualizar média incremental após a partida;
- persistir episódios em JSONL;
- salvar e carregar snapshot Q em JSON;
- resetar estado entre experimentos.

Atualização:

```text
novo_valor = valor_antigo + (recompensa - valor_antigo) / visitas
```

O agente aprende após cada partida. Todas as decisões que ele tomou naquela partida recebem a recompensa terminal.

API prevista:

```python
def aprendiz(board: Tab, player: str, rng: random.Random) -> Tab: ...
```

`aprendiz` terá callback interno de fim de partida com contrato:

```python
aprendiz.on_game_end(player, winner)
```

O callback continua pertencendo ao módulo `algorithms/learning.py`; `main.py` apenas o dispara.

## 2. Integração do motor

O contrato normal continua sendo `fn(board, player, rng) -> Tab`. Como o agente não recebe o lance final do oponente, o motor precisa informar o resultado depois que a partida acaba.

Helper em `main.py`:

```python
def notify_game_end(players, winner):
    for player, strategy in players:
        hook = getattr(strategy, "on_game_end", None)
        if hook:
            hook(player, winner)
```

Usar o helper em:

- `main.play_game`;
- `main.play_with_view`;
- `run_torneio.py`;
- `run_progressivo.py`.

O helper não calcula recompensa nem conhece Q. Estratégias antigas não possuem callback e continuam iguais.

## 3. Persistência

Cada experimento possui diretório próprio:

```text
experiments/learning/
└── aprendiz_vs_ingenuo/
    ├── episodes.jsonl
    ├── progress.jsonl
    ├── q_table.json
    └── progress.svg
```

`episodes.jsonl` é fonte histórica. Uma linha contém decisões do agente, estados, ações, jogador, resultado e recompensa:

```json
{"schema_version":1,"partida":1,"player":"X","moves":[{"state":".........|X","action":4}],"winner":"X","reward":2}
```

`q_table.json` é snapshot derivado e versionado:

```json
{"schema_version":1,"algorithm":"monte_carlo_q_table","epsilon":0.0,"episodes":1,"states":{}}
```

Carga será explícita. Sem `carregar_q`, agente começa zerado. Escrita será opcional para testes e partidas normais, evitando artefatos inesperados.

## 4. Experimentos no escopo

### Confrontos diretos

Quatro experimentos independentes, cada um começando com Q vazio:

```text
aprendiz vs ingenuo
ingenuo  vs aprendiz
aprendiz vs fera
fera     vs aprendiz
```

Currículos de treinamento ficam para fase futura.

`fera` é o nome canônico do minimax (`fera_minimax`). `fera_aprendizado` é a estratégia Q pré-treinada existente e fica fora deste escopo; não representa o agente novo zerado. `fera_basica`, outros algoritmos e `humano` ficam para fase posterior.

Cada execução produz seu próprio diretório, dataset, snapshot Q, estatísticas e gráfico. Nenhuma execução compartilha Q com outra.

## 5. Progresso cumulativo

`progress.jsonl` terá uma linha inicial e uma linha por partida. Em v1 todos os experimentos são diretos: `fase` é `direto`. Os campos `fase`, `oponente`, `fase_partida` e os contadores de fase seguem no schema para suportar o marcador de transição quando currículos entrarem na fase futura:

```json
{"partida":0,"fase":"direto","oponente":"ingenuo","fase_partida":0,"J1":0,"V":0,"J2":0,"vencedor":null}
{"partida":1,"fase":"direto","oponente":"ingenuo","fase_partida":1,"J1":1,"V":0,"J2":0,"vencedor":"J1"}
{"partida":2,"fase":"direto","oponente":"ingenuo","fase_partida":2,"J1":1,"V":1,"J2":0,"vencedor":"V"}
{"partida":3,"fase":"direto","oponente":"ingenuo","fase_partida":3,"J1":1,"V":1,"J2":1,"vencedor":"J2"}
```

`J1` e `J2` são vitórias cumulativas das posições. `V` é empate cumulativo. `vencedor` identifica o resultado exato daquela partida.
`fase_J1`, `fase_V` e `fase_J2` reiniciam apenas na troca de oponente (caminho mantido para o currículo futuro). O gráfico usa as séries globais e marca a transição quando houver.

Assim, a partida 100 pode ser consultada sem reexecutar nada:

```text
progress[100] -> vencedor + totais J1/V/J2 até partida 100
```

## 6. Gráficos

Gerar SVG com `matplotlib` usando backend `Agg`, sem abrir janela. A dependência
fica registrada em `requirements.txt` e permite evoluir depois para PNG,
subplots e análises estatísticas sem manter desenho manual de SVG.

Cada `progress.svg` terá:

- eixo X: número da partida;
- eixo Y: contagem cumulativa;
- linha azul: vitórias J1;
- linha cinza: empates V;
- linha vermelha: vitórias J2;
- título com o experimento (`Aprendiz vs Ingenuo`);
- legenda e total de partidas.
- marcador vertical no ponto de troca de oponente, quando houver (caminho mantido para o currículo futuro).

O gráfico será sempre construído lendo `progress.jsonl`; nenhum ponto será codificado manualmente.

## 7. Runner de experimentos

Criar `run_aprendizado.py` como orquestrador, sem algoritmo de jogo:

```text
1. recebe quantidade de partidas e o confronto (`aprendiz_vs_ingenuo` ou `ingenuo_vs_aprendiz`);
2. cria diretório do confronto;
3. reseta agente;
4. grava linha 0;
5. executa as partidas;
6. grava resultado e contagens;
7. atualiza JSONL/Q;
8. gera SVG no final;
9. permite consultar `--partida 100`.
```

Execução inicial recomendada: 100 partidas por confronto. Execuções maiores devem oferecer modo compacto; registrar decisões completas de 1M partidas pode gerar arquivo desnecessariamente grande.

## 8. Arquivos envolvidos

| Arquivo | Mudança |
|---|---|
| `algorithms/learning.py` | agente, histórico, persistência Q/JSONL |
| `algorithms/__init__.py` | exportar `aprendiz` |
| `main.py` | importar, registrar em `STRATEGIES`, notificar fim |
| `run_torneio.py` | notificar fim para não perder aprendizado |
| `run_progressivo.py` | notificar fim quando usado com agente |
| `run_aprendizado.py` | executar confrontos e gerar dados/gráficos |
| `test_main.py` | testes do agente e integração |
| `requirements.txt` | dependência de gráficos |
| `.gitignore` | ignorar datasets completos gerados |

## 9. Verificação

- partida 0 existe em todo `progress.jsonl`;
- partida N existe após N jogos;
- partida 100 retorna exatamente seus totais;
- cada confronto direto gera um único `progress.svg` próprio;
- carga de `q_table.json` reproduz valores aprendidos;
- os experimentos diretos não compartilham Q;
- `python -m unittest test_main -v` continua verde;
- nenhum dado de gráfico é inventado.
