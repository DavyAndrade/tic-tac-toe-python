# Constituição — TicTacToe

Princípios extraídos do código existente. Vale para toda feature nova.

## Princípios arquiteturonómicos

- Contrato de estratégia: `fn(board, player, rng) -> Tab`. Retorno sempre tupla imutável nova.
- Regras de tabuleiro só em `core/board.py`. Estratégias só em `algorithms/`.
- `main.py` guarda cópias de compatibilidade e rebinda nomes públicos. Não "consertar" duplicatas lá; preservar exports.
- Importar `main` dispara treino Q de 10.000 episódios. Tooling leve não importa `main`.
- `fera_basica` é rules-only. Sem fallback minimax.

## Padrões

- Nomeação em português (`ingenuo`, `fera_*`, `tab_vazio`).
- Imutabilidade: estado do jogo = tupla; `board[:i] + (player,) + board[i+1:]`.
- Estratégias registráveis externamente via `python main.py register NOME arq.py:funcao` (`strategies.json` é ignorado pelo git).
- Algoritmos ficam em `algorithms/`; `main.py` apenas coordena partidas e preserva a API pública.
- Dados brutos de aprendizado são eventos versionados em JSONL; tabela aprendida é snapshot JSON derivado.
- Gráficos são gerados a partir dos dados persistidos, nunca de valores inventados ou embutidos no código.

## Porta de verificação

- `python -m unittest test_main -v` — obrigatório, verde, antes de commit.
- `python main.py test` é smoke de 60 jogas. Nunca substitui a suíte.
- `run_torneio.py` com contagem pequena para checagens. `run_progressivo.py` (1M partidas) só sob pedido explícito.
- Experimentos de aprendizado devem registrar progresso cumulativo por partida e permitir consulta por número da partida.

## Versionamento

- v1.0 — inicial, derivada do estado atual do repositório (set/2026).
