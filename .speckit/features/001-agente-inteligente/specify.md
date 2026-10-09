# Especificação — Agente Inteligente (001)

Feature: estratégia que começa com zero conhecimento, aprende entre partidas e persiste evidências do aprendizado.

## Visão

Código "zerado": tabela de valores vazia. A cada partida em que joga, registra suas jogadas `(estado, célula)` e ao fim aplica recompensa terminal — **+10 venceu, +1 empatou, −3 perdeu** (peso vigente — `eps0_pes1013`, variante de persistência em árvore: vitória forte, derrota suavizada; baseline +2/+1/−5 (`eps0_pes215`) segue campeã, com `eps0_pes311`, `eps0_pes424` e `eps0_pes1011` descartadas) — a todas as jogadas daquela partida, influenciando escolhas futuras.

O foco inicial será `aprendiz` vs `ingenuo` e `ingenuo` vs `aprendiz`. Em v1 executam-se os quatro confrontos diretos (`ingenuo` e `fera_basica` como oponentes, em ambos os lados); currículos ficam para fase futura. Cada experimento terá dataset, tabela, estatísticas e gráfico próprios; cada experimento começa com agente zerado.

## Requisitos funcionais

- **FR-001** — Tabela de valores `(tabuleiro, jogador) -> {célula: (soma, n)}` inicia vazia. Zero conhecimento.
- **FR-002** — Durante a partida, registra cada jogada feita: par `(estado, célula)`.
- **FR-003** — Ao fim de cada partida em que participou, aplica a recompensa terminal a **todas** as jogadas registradas daquela partida: +10 (agente venceu), +1 (empate), −3 (agente perdeu); pesos em `_RECOMPENSAS_APRENDIZ`.
- **FR-004** — Escolha ε-greedy: com probabilidade ε joga aleatoriamente (usa o `rng` fornecido); caso contrário, maior valor, desempate aleatório via `rng`.
- **FR-005** — Atualização por média incremental: `Q ← Q + (recompensa − Q) / N`, com `N` por par (estado, célula).
- **FR-006** — `resetar_aprendizado()` esvazia a tabela e os históricos.
- **FR-007** — Registrada como `aprendiz` em `STRATEGIES` e exportada de `algorithms/`.
- **FR-008** — Ao fim de cada partida, persistir em JSONL as decisões do agente, estado, ação, jogador, resultado e recompensa.
- **FR-009** — Persistir tabela aprendida em JSON versionado, com valores, quantidade de visitas, algoritmo e número de episódios.
- **FR-010** — Permitir carregar tabela persistida explicitamente para continuar treinamento; execução sem carga começa zerada.
- **FR-011** — Executar os quatro confrontos diretos do escopo: `aprendiz` vs `ingenuo`, `ingenuo` vs `aprendiz`, `aprendiz` vs `fera_basica` e `fera_basica` vs `aprendiz`.
- **FR-012** — Persistir uma linha inicial da partida `0` com `J1=0`, `V=0`, `J2=0`, seguida de uma linha após cada partida com contagens cumulativas e vencedor da partida.
- **FR-013** — Gerar **um gráfico SVG por confronto ordenado**, a partir das linhas persistidas, com eixo X = número da partida e séries cumulativas `J1`, `V` e `J2`.
- **FR-014** — Permitir consultar estatísticas exatas de qualquer partida persistida, incluindo a partida 100, sem reexecutar o experimento.
- **FR-015** — Usar nomes canônicos de estratégias na matriz; `fera` e `fera_minimax` não devem gerar gráficos duplicados quando apontam para o mesmo algoritmo.

## Histórias de usuário

1. **Como** jogo, **quero** que o agente comece sem saber nada, **para** observar o aprendizado a partir do zero.
2. **Como** torneio, **quero** que o agente melhore entre partidas sem re-treino explícito, **para** rodar `run_torneio` e ver a curva.
3. **Como** teste, **quero** `resetar_aprendizado()` entre casos, **para** estado global não vazar.
4. **Como** observador do experimento, **quero** um gráfico separado para cada confronto ordenado, **para** comparar posições e adversários sem misturar resultados.
5. **Como** pesquisador, **quero** recuperar a partida 100 pelo número em qualquer confronto, **para** conferir o vencedor e os totais naquele ponto.
6. **Como** pesquisador, **quero** continuar a mesma tabela após trocar `ingenuo` por `fera`, **para** observar transferência de aprendizado.

## Critérios de sucesso

- **SC-001** — `python -m unittest test_main -v` verde (suíte existente + novos).
- **SC-002** — Teste prova propagação: partida perdida ⇒ Q negativo nos pares da partida; vencida ⇒ positivo; empate ⇒ +1.
- **SC-003** — Teste de aprendizado: em cada confronto configurado, comparar janelas inicial e final sem exigir melhora estocástica rígida como teste unitário.
- **SC-004** — Cada confronto configurado executa 100 partidas sem exceção, com agente em J1 e J2 quando aplicável.
- **SC-005** — Estado zerado produz jogada válida sempre (nunca célula ocupada, nunca trava).
- **SC-006** — JSONL contém exatamente uma linha de progresso para a partida 0 e uma linha para cada partida executada; linha 100 é recuperável quando 100 partidas existem.
- **SC-007** — Os confrontos diretos produzem arquivos distintos e não compartilham Q.
- **SC-009** — Cada experimento produz exatamente um gráfico SVG derivado do seu próprio progresso persistido, contendo séries J1, V e J2 e marcador de transição quando aplicável.
- **SC-011** — Tabela JSON carregada reproduz decisões aprendidas sem executar novo treinamento.

## Edge cases

- **EC-001** — Fim no lance do **oponente**: agente não é chamado de novo naquele jogo → precisa de notificação externa (`on_game_end`).
- **EC-002** — Recompensa é do agente (venceu/perdeu/empatou), independente de ser X ou O.
- **EC-003** — Tabela zerada: todos Q = 0 ⇒ desempate aleatório obrigatório (senão partida sempre idêntica).
- **EC-004** — Estado global entre testes ⇒ `resetar_aprendizado()` obrigatório em setup.
- **EC-005** — Dois loops de jogo (`play_game`, `play_with_view`) ⇒ notificação nos dois.
- **EC-006** — Experimento com zero partidas ⇒ apenas linha-base e gráfico vazio válido.
- **EC-007** — Consulta de partida inexistente ⇒ erro explícito, sem retornar estatística de outra partida.
- **EC-008** — Dataset parcialmente gravado ⇒ validação de `schema_version` e mensagem clara; não aceitar estado silenciosamente corrompido.
- **EC-009** — J1/J2 no gráfico são posições da partida; métricas do agente devem indicar sua posição para não inverter vitória e derrota.

## Fora de escopo (v1)

- ε decrescente / hiperparâmetros configuráveis.
- Treino em lote por autojogo (já coberto por `fera_aprendizado`).
- Mudar contrato das 4 estratégias existentes.
- Jogo generalizado (n×n).
- Banco de dados ou dashboard web interativo; v1 usa JSONL, JSON e SVG.
- Matriz completa de adversários; em v1 os oponentes são `ingenuo` e `fera_basica`, e currículos ficam na fase futura.
- `fera_aprendizado` como adversário; ele é a estratégia Q pré-treinada existente, não o agente novo zerado.

### Fase futura — currículos

Requisitos, critérios e edge cases adiados para a fase seguinte; ids preservados, sem renumeração.

Requisitos funcionais:

- **FR-016** — Executar currículo `ingenuo -> fera` mantendo a mesma tabela Q entre fases e registrando o ponto de transição.
- **FR-017** — Executar currículo `fera -> ingenuo` mantendo a mesma tabela Q entre fases e registrando o ponto de transição.
- **FR-018** — Executar cada currículo com `aprendiz` como J1 e como J2, sem misturar Q entre experimentos.
- **FR-019** — Registrar fase, oponente e contagens cumulativas por fase nos dados de progresso.

Critérios de sucesso:

- **SC-008** — As quatro sequências curriculares produzem arquivos distintos e preservam Q somente entre suas duas fases.
- **SC-010** — Dados de progresso identificam o oponente e a fase de cada partida; a transição é consultável sem reexecutar o experimento.

Edge cases:

- **EC-010** — Troca de `ingenuo` para `fera` não pode resetar Q dentro do mesmo currículo.
- **EC-011** — Novo currículo começa com Q vazio, mesmo que outro currículo tenha terminado com conhecimento.
