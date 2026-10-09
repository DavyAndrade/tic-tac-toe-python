# Tasks — Agente Inteligente (001)

Ordem TDD (skill `tdd`): teste primeiro, assistir falhar, implementação mínima, suíte verde. Porta: `python -m unittest test_main -v`.

## Fase 1 — núcleo em `algorithms/learning.py`

- [x] **T1** — Teste: tabela e históricos começam vazios; `resetar_aprendizado()` limpa tudo (FR-001, FR-006, EC-004). → Implementar estado.
- [x] **T2** — Teste: estado zerado produz jogada válida; ε-greedy explora e escolhe maior valor quando aplicável (FR-004, EC-003, SC-005). → Implementar escolha e registro.
- [x] **T3** — Teste: callback aplica +2, +0 e −5 ao agente como X e como O; média incremental funciona (FR-002, FR-003, FR-005, EC-002, SC-002). → Implementar atualização.
- [x] **T4** — Teste: histórico separado por jogador permite agente como X e O, inclusive em partidas consecutivas (EC-002). → Corrigir isolamento de histórico.

## Fase 2 — persistência do agente

- [x] **T5** — Teste: episódio concluído gera uma linha JSONL com schema, decisões, resultado e recompensa (FR-008, EC-008). → Implementar serialização.
- [x] **T6** — Teste: tabela salva em JSON e carregada reproduz valores e visitas; execução sem carga continua zerada (FR-009, FR-010, SC-009). → Implementar snapshot Q.
- [x] **T7** — Teste: escrita opcional não cria arquivos em testes que não configuram persistência. → Implementar configuração explícita.

## Fase 3 — integração brownfield

- [x] **T8** — Teste: helper de fim de partida notifica `play_game` e `play_with_view`; histórico recebe resultado mesmo quando o oponente faz o último lance (EC-001, EC-005). → Integrar em `main.py`.
- [x] **T9** — Teste: `run_torneio.py` e `run_progressivo.py` notificam o agente; partida seguinte não herda histórico pendente (FR-003). → Integrar runners.
- [x] **T10** — Exportar `aprendiz` em `algorithms/__init__.py` e registrar em `main.STRATEGIES`; testar `resolve_strategy("aprendiz")` (FR-007).

## Fase 4 — experimentos diretos

- [x] **T11** — Teste: runner reseta agente e cria diretório separado para `aprendiz/ingenuo` e `ingenuo/aprendiz` (FR-011, SC-007).
- [x] **T12** — Teste: cada progresso inicia em `partida=0` com `J1=0,V=0,J2=0` e acrescenta uma linha cumulativa por partida, incluindo `vencedor` (FR-012, SC-006).
- [x] **T13** — Teste: consulta retorna estatísticas da partida solicitada e falha claramente para partida inexistente (FR-014, EC-006, EC-007).
- [x] **T14** — Implementar somente os dois confrontos diretos do escopo inicial; `humano` e demais oponentes ficam fora (FR-011).
- [ ] **T15** — Teste: currículo `ingenuo -> fera` mantém Q e histórico de aprendizado entre fases, mas novo currículo começa zerado (FR-016, FR-018, EC-010, EC-011). — adiado, fase futura.
- [ ] **T16** — Teste: currículo `fera -> ingenuo` funciona com agente como J1 e como J2, registrando o ponto de transição e contagens por fase (FR-017, FR-019, SC-008, SC-010). — adiado, fase futura.

## Fase 5 — gráficos

- [x] **T17** — Teste: gerador lê somente `progress.jsonl` e cria um SVG para cada um dos dois confrontos diretos, com linhas `J1`, `V` e `J2` (FR-013, SC-009).
- [x] **T18** — Gerar gráficos em `experiments/learning/<experimento>/progress.svg`, com marcador de transição quando houver (caminho mantido para o currículo futuro), usando biblioteca padrão.
- [x] **T19** — Smoke com 5 partidas nos dois confrontos diretos; arquivos JSONL, Q e SVG existem; partida 5 é consultável.

## Fase 6 — verificação e entrega

- [x] **T20** — Suíte completa: `python -m unittest test_main -v` (SC-001).
- [x] **T21** — Executar 100 partidas por confronto; conferir linha 100 e gráficos sem inventar dados (SC-004, SC-006, SC-009).
- [x] **T22** — Versionar saídas de `experiments/learning/` por enquanto; revisar `.gitignore` antes de rodadas de 1M partidas (decisão do usuário).
- [ ] **T23** — Commit + push (preferência registrada).
- [x] **T24** — Atualizar `AGENTS.md` com setup de `matplotlib` via `.venv`.
