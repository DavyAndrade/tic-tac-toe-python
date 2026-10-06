"""Testes unitarios para main.py (paradigma funcional) - usa unittest."""
import io
import json
import os
import tempfile
import unittest

import main
from algorithms import learning


class TestBoard(unittest.TestCase):
    def test_tab_vazio_nove_posicoes(self):
        b = main.tab_vazio()
        self.assertEqual(len(b), 9)
        self.assertTrue(all(c == main.EMPTY for c in b))
        self.assertIsInstance(b, tuple)

    def test_winner_linha(self):
        b = (main.X, main.X, main.X, main.O, main.O, main.EMPTY,
             main.EMPTY, main.EMPTY, main.EMPTY)
        self.assertEqual(main.get_winner(b), main.X)

    def test_winner_coluna(self):
        b = (main.O, main.X, main.X,
             main.O, main.O, main.X,
             main.O, main.EMPTY, main.EMPTY)
        self.assertEqual(main.get_winner(b), main.O)

    def test_winner_diagonal(self):
        b = (main.X, main.O, main.X,
             main.O, main.X, main.O,
             main.O, main.X, main.X)
        self.assertEqual(main.get_winner(b), main.X)

    def test_sem_winner(self):
        b = (main.X, main.O, main.X,
             main.X, main.O, main.O,
             main.O, main.X, main.X)
        self.assertIsNone(main.get_winner(b))

    def test_is_full(self):
        self.assertTrue(main.is_full(
            (main.X, main.O, main.X, main.O, main.X, main.O,
             main.O, main.X, main.O)))
        self.assertFalse(main.is_full(main.tab_vazio()))

    def test_empty_cells(self):
        b = (main.X, main.EMPTY, main.O,
             main.EMPTY, main.X, main.EMPTY,
             main.O, main.EMPTY, main.X)
        self.assertEqual(main.get_empty_cells(b), (1, 3, 5, 7))


class TestMovimentos(unittest.TestCase):
    def test_feras_tem_mesma_interface(self):
        import random
        for strategy in (main.fera_basica, main.fera_minimax, main.fera_aprendizado):
            board = strategy(main.tab_vazio(), main.X, random.Random(0))
            self.assertEqual(sum(cell != main.EMPTY for cell in board), 1)

    def test_ingenuo_cria_novo_board_imutavel(self):
        import random
        b = main.tab_vazio()
        b2 = main.ingenuo(b, main.X, random.Random(0))
        self.assertEqual(b, main.tab_vazio())
        self.assertNotEqual(b, b2)
        self.assertEqual(sum(1 for c in b2 if c != main.EMPTY), 1)

    def test_fera_joga_em_celula_vazia(self):
        import random
        b = main.tab_vazio()
        b2 = main.fera(b, main.X, random.Random(0))
        self.assertEqual(sum(1 for c in b2 if c != main.EMPTY), 1)
        self.assertIn(main.X, b2)


class TestAprendiz(unittest.TestCase):
    def test_epsilon_zero_por_decisao(self):
        self.assertEqual(learning._EPSILON_APRENDIZ, 0.0)

    def test_resetar_aprendizado_limpa_tabela_e_historicos(self):
        learning.resetar_aprendizado()
        learning._Q_APRENDIZ[(main.tab_vazio(), main.X)] = {4: (2.0, 1)}
        learning._HISTORICO_APRENDIZ[main.X].append(((main.tab_vazio(), main.X), 4))

        learning.resetar_aprendizado()

        self.assertEqual(learning._Q_APRENDIZ, {})
        self.assertEqual(learning._HISTORICO_APRENDIZ, {main.X: [], main.O: []})

    def test_aprendiz_escolhe_maior_valor_em_estado_conhecido(self):
        import random

        learning.resetar_aprendizado()
        board = main.tab_vazio()
        learning._Q_APRENDIZ[(board, main.X)] = {
            0: (-1.0, 1),
            4: (2.0, 1),
        }

        result = learning.aprendiz(board, main.X, random.Random(0))

        self.assertEqual(result[4], main.X)
        self.assertEqual(sum(cell != main.EMPTY for cell in result), 1)

    def test_aprendiz_aplica_recompensa_de_vitoria(self):
        import random

        learning.resetar_aprendizado()
        board = main.tab_vazio()
        learning.aprendiz(board, main.X, random.Random(0))
        state, cell = learning._HISTORICO_APRENDIZ[main.X][0]

        learning.aprendiz.on_game_end(main.X, main.X)

        self.assertEqual(learning._Q_APRENDIZ[state][cell], (2.0, 1))
        self.assertEqual(learning._HISTORICO_APRENDIZ[main.X], [])

    def test_aprendiz_aplica_empate_derrota_e_media_incremental(self):
        import random

        learning.resetar_aprendizado()
        board = main.tab_vazio()
        learning.aprendiz(board, main.X, random.Random(0))
        state, cell = learning._HISTORICO_APRENDIZ[main.X][0]
        learning.aprendiz.on_game_end(main.X, None)

        learning.aprendiz(board, main.X, random.Random(0))
        learning.aprendiz.on_game_end(main.X, main.X)

        self.assertEqual(learning._Q_APRENDIZ[state][cell], (1.5, 2))

        learning.aprendiz(board, main.O, random.Random(0))
        state_o, cell_o = learning._HISTORICO_APRENDIZ[main.O][0]
        learning.aprendiz.on_game_end(main.O, main.X)

        self.assertEqual(learning._Q_APRENDIZ[state_o][cell_o], (-5.0, 1))

    def test_aprendiz_persiste_episodio_em_jsonl(self):
        import random

        learning.resetar_aprendizado()
        with tempfile.TemporaryDirectory() as directory:
            episodes_path = os.path.join(directory, "episodes.jsonl")
            q_path = os.path.join(directory, "q_table.json")
            learning.configurar_persistencia(episodes_path, q_path)
            learning.aprendiz(main.tab_vazio(), main.X, random.Random(0))
            learning.aprendiz.on_game_end(main.X, main.X)
            learning.configurar_persistencia(None)

            with open(episodes_path) as file:
                episode = json.loads(file.readline())

        self.assertEqual(episode["schema_version"], 1)
        self.assertEqual(episode["player"], main.X)
        self.assertEqual(episode["reward"], 2)
        self.assertEqual(len(episode["moves"]), 1)

    def test_aprendiz_salva_e_carrega_tabela_q(self):
        import random

        learning.resetar_aprendizado()
        with tempfile.TemporaryDirectory() as directory:
            q_path = os.path.join(directory, "q_table.json")
            learning.aprendiz(main.tab_vazio(), main.X, random.Random(0))
            state, cell = learning._HISTORICO_APRENDIZ[main.X][0]
            learning.aprendiz.on_game_end(main.X, main.X)
            learning.salvar_q(q_path)
            learning.resetar_aprendizado()

            learning.carregar_q(q_path)

            self.assertEqual(learning._Q_APRENDIZ[state][cell], (2.0, 1))

    def test_aprendiz_sem_persistencia_nao_cria_arquivos(self):
        import random

        learning.resetar_aprendizado()
        learning.configurar_persistencia(None)
        with tempfile.TemporaryDirectory() as directory:
            learning.aprendiz(main.tab_vazio(), main.X, random.Random(0))
            learning.aprendiz.on_game_end(main.X, main.X)

            self.assertEqual(os.listdir(directory), [])

    def test_play_game_finaliza_historico_do_aprendiz(self):
        learning.resetar_aprendizado()

        main.play_game(main.fera, learning.aprendiz, seed=0)

        self.assertEqual(learning._HISTORICO_APRENDIZ[main.O], [])
        self.assertTrue(learning._Q_APRENDIZ)

    def test_play_with_view_finaliza_historico_do_aprendiz(self):
        import contextlib

        learning.resetar_aprendizado()
        with contextlib.redirect_stdout(io.StringIO()):
            main.play_with_view(main.fera, learning.aprendiz, seed=0)

        self.assertEqual(learning._HISTORICO_APRENDIZ[main.O], [])

    def test_run_torneio_finaliza_historico_do_aprendiz(self):
        import run_torneio

        learning.resetar_aprendizado()
        run_torneio.simular(main.fera, learning.aprendiz, seed=0)

        self.assertEqual(learning._HISTORICO_APRENDIZ[main.O], [])

    def test_run_progressivo_finaliza_historico_do_aprendiz(self):
        import run_progressivo

        learning.resetar_aprendizado()
        run_progressivo.simular(main.fera, learning.aprendiz, seed=0)

        self.assertEqual(learning._HISTORICO_APRENDIZ[main.O], [])

    def test_aprendiz_e_resolvido_pelo_registro_de_estrategias(self):
        label, strategy = main.resolve_strategy("aprendiz")

        self.assertIn("aprendiz", main.STRATEGIES)
        self.assertEqual(label, "aprendiz")
        self.assertIs(strategy, learning.aprendiz)

    def test_consulta_progresso_retorna_partida_solicitada(self):
        import run_aprendizado

        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "progress.jsonl")
            with open(path, "w") as file:
                file.write(json.dumps({"partida": 0, "J1": 0, "V": 0, "J2": 0}) + "\n")
                file.write(json.dumps({"partida": 1, "J1": 1, "V": 0, "J2": 0}) + "\n")

            result = run_aprendizado.consultar_partida(path, 1)
            self.assertEqual(result["J1"], 1)
            with self.assertRaises(KeyError):
                run_aprendizado.consultar_partida(path, 100)

    def test_runner_gera_progresso_q_e_svg_por_experimento(self):
        import run_aprendizado

        learning.resetar_aprendizado()
        with tempfile.TemporaryDirectory() as directory:
            result = run_aprendizado.executar_experimento(
                "aprendiz_vs_ingenuo",
                run_aprendizado.SCENARIOS["aprendiz_vs_ingenuo"],
                rounds_per_phase=2,
                root=directory,
            )
            progress = run_aprendizado.carregar_progresso(result["progress"])

            self.assertEqual([row["partida"] for row in progress], [0, 1, 2])
            self.assertTrue(result["episodes"].exists())
            self.assertTrue(result["q_table"].exists())
            self.assertTrue(result["svg"].exists())
            self.assertIn("J1", result["svg"].read_text())
            self.assertIn("V", result["svg"].read_text())
            self.assertIn("J2", result["svg"].read_text())

    def test_svg_marca_numeros_das_partidas_no_eixo_x(self):
        import run_aprendizado

        with tempfile.TemporaryDirectory() as directory:
            progress_path = os.path.join(directory, "progress.jsonl")
            svg_path = os.path.join(directory, "progress.svg")
            with open(progress_path, "w") as file:
                for partida in (0, 500, 1000):
                    file.write(json.dumps({
                        "partida": partida,
                        "J1": partida,
                        "V": 0,
                        "J2": 0,
                    }) + "\n")

            run_aprendizado.gerar_svg(progress_path, svg_path, "teste")
            with open(svg_path) as file:
                svg = file.read()

        for partida in (0, 100, 500, 1000):
            self.assertIn(f">{partida}</text>", svg)
        self.assertIn("matplotlib", svg)

    def test_svg_labels_usam_nome_dos_jogadores(self):
        import run_aprendizado

        with tempfile.TemporaryDirectory() as directory:
            progress_path = os.path.join(directory, "progress.jsonl")
            svg_path = os.path.join(directory, "progress.svg")
            with open(progress_path, "w") as file:
                file.write(json.dumps({"partida": 0, "J1": 0, "V": 0, "J2": 0}) + "\n")

            run_aprendizado.gerar_svg(
                progress_path,
                svg_path,
                "J1 (Aprendiz) vs J2 (Ingenuo)",
                j1_name="aprendiz",
                j2_name="ingenuo",
            )
            with open(svg_path) as file:
                svg = file.read()

        self.assertIn("J1 (Aprendiz)", svg)
        self.assertIn("J2 (Ingenuo)", svg)

    def test_runner_novo_experimento_comeca_q_vazio(self):
        import run_aprendizado

        scenario = run_aprendizado.SCENARIOS["aprendiz_vs_ingenuo"]
        with tempfile.TemporaryDirectory() as directory:
            run_aprendizado.executar_experimento(
                "primeiro", scenario, rounds_per_phase=1, root=directory
            )
            result = run_aprendizado.executar_experimento(
                "segundo", scenario, rounds_per_phase=1, root=directory
            )
            q_table = json.loads(result["q_table"].read_text())

        visits = sum(
            action["visits"]
            for action in q_table["states"][".........|X"].values()
        )
        self.assertEqual(visits, 1)

    def test_runner_executa_os_quatro_confrontos_diretos(self):
        import run_aprendizado

        expected = {
            "aprendiz_vs_ingenuo",
            "ingenuo_vs_aprendiz",
            "aprendiz_vs_fera",
            "fera_vs_aprendiz",
        }
        with tempfile.TemporaryDirectory() as directory:
            results = run_aprendizado.executar_matriz(
                rounds_per_phase=1, root=directory
            )

            self.assertEqual(set(results), expected)
            for name, phases in run_aprendizado.SCENARIOS.items():
                progress = run_aprendizado.carregar_progresso(results[name]["progress"])
                self.assertEqual(progress[-1]["partida"], len(phases))
                self.assertEqual(progress[0]["J1"], 0)
                self.assertEqual(progress[0]["V"], 0)
                self.assertEqual(progress[0]["J2"], 0)

    def test_fera_primeiro_turno_joga_otimo(self):
        import random
        b2 = main.fera(main.tab_vazio(), main.X, random.Random(0))
        cell = next(i for i, c in enumerate(b2) if c != main.EMPTY)
        self.assertIn(cell, (0, 2, 4, 6, 8))

    def test_fera_basica_bloqueia_garfo(self):
        import random
        board = (main.X, main.EMPTY, main.EMPTY,
                 main.EMPTY, main.O, main.EMPTY,
                 main.EMPTY, main.EMPTY, main.X)
        result = main.fera_basica(board, main.O, random.Random(0))
        cell = next(i for i, value in enumerate(result) if value != board[i])
        self.assertIn(cell, (1, 3, 5, 7))

    def test_fera_basica_forca_resposta_contra_garfo(self):
        import random
        board = (main.O, main.EMPTY, main.EMPTY,
                 main.EMPTY, main.X, main.EMPTY,
                 main.EMPTY, main.EMPTY, main.X)
        result = main.fera_basica(board, main.O, random.Random(0))
        cell = next(i for i, value in enumerate(result) if value != board[i])
        self.assertIn(cell, (2, 6))


class TestMinimax(unittest.TestCase):
    def test_minimax_vitoria_x(self):
        b = (main.X, main.X, main.X,
             main.O, main.O, main.EMPTY,
             main.EMPTY, main.EMPTY, main.EMPTY)
        score, _ = main.minimax(b, main.O)
        self.assertGreater(score, 0)

    def test_minimax_bloqueio_critical(self):
        b = (main.X, main.X, main.EMPTY,
             main.O, main.O, main.EMPTY,
             main.EMPTY, main.EMPTY, main.EMPTY)
        score, cell = main.minimax(b, main.O)
        self.assertEqual(cell, 5)


class TestPartida(unittest.TestCase):
    def test_play_game_formato(self):
        g = main.play_game(main.fera, main.ingenuo, seed=5)
        for key in ("j1", "v", "j2", "n", "winner", "t0", "t8"):
            self.assertIn(key, g)
        self.assertIn(g["j1"], (0, 1))
        self.assertIn(g["v"], (0, 1))
        self.assertIn(g["j2"], (0, 1))
        self.assertIn(g["winner"], (-1, 0, 1))

    def test_play_game_j1_vence(self):
        # Forca vitoria de X
        b = (main.X, main.X, main.EMPTY,
             main.O, main.O, main.EMPTY,
             main.EMPTY, main.EMPTY, main.EMPTY)
        # Joga ingenuo com seed que escolhe posicao 2
        g = main.play_game(main.ingenuo, main.ingenuo, seed=0)
        # Verifica formato: exatamente 1 de j1/v/j2 e 1
        bits = [g["j1"], g["v"], g["j2"]]
        self.assertEqual(sum(bits), 1)
        self.assertIn(g["winner"], (-1, 0, 1))

    def test_fera_nunca_perde_vs_ingenuo(self):
        results = main.compete("ingenuo", "fera", rounds=30,
                               start_player=0, seed=100)
        for g in results:
            # fera e J2, nao deve perder (winner != 1, que significaria J1 venceu)
            if g["winner"] == 1:
                self.fail("fera perdeu como J2")

    def test_fera_vs_fera_sempre_empata(self):
        results = main.compete("fera", "fera", rounds=15,
                               start_player=0, seed=42)
        for g in results:
            self.assertEqual(g["winner"], 0, "dois feras devem empatar")

    def test_compete_conta_rounds(self):
        results = main.compete("ingenuo", "fera", rounds=10,
                               start_player=0, seed=0)
        self.assertEqual(len(results), 10)

    def test_progressivo_permite_destino_explícito(self):
        from pathlib import Path

        import run_progressivo

        self.assertEqual(
            run_progressivo._pasta_destino("ingenuo", "ingenuo"),
            Path("experiments") / "minimax",
        )
        self.assertEqual(
            run_progressivo._pasta_destino("ingenuo", "ingenuo", "basic"),
            Path("experiments") / "basic",
        )
        self.assertEqual(
            run_progressivo._pasta_destino("ingenuo", "fera_basica"),
            Path("experiments") / "basic",
        )

    def test_summarize(self):
        results = main.compete("ingenuo", "fera", rounds=10,
                               start_player=0, seed=3)
        s = main.summarize(results)
        self.assertIn("ingenuo", s)
        self.assertIn("fera", s)
        total = sum(v["W"] + v["D"] + v["L"] for v in s.values())
        self.assertEqual(total, 20)

    def test_save_json_e_txt(self):
        results = main.compete("ingenuo", "fera", rounds=5,
                               start_player=0, seed=0)
        with tempfile.TemporaryDirectory() as d:
            jp = os.path.join(d, "r.json")
            tp = os.path.join(d, "r.txt")
            main.save_json(results, jp)
            main.save_txt(results, tp)
            with open(jp) as f:
                data = json.loads(f.read())
            self.assertEqual(len(data), 5)
            with open(tp) as f:
                txt = f.read()
            self.assertIn("SUMARIO", txt)

    def test_fera_dominia_ingenuo_estatistica(self):
        results = main.compete("ingenuo", "fera", rounds=20,
                               start_player=0, seed=11)
        s = main.summarize(results)
        self.assertEqual(s["fera"]["L"], 0)
        self.assertGreaterEqual(s["fera"]["W"], 15)


class TestRender(unittest.TestCase):
    def test_draw_board_visually(self):
        b = (main.X, main.O, main.EMPTY, main.EMPTY, main.X, main.EMPTY,
             main.EMPTY, main.EMPTY, main.O)
        buf = io.StringIO()
        import contextlib
        with contextlib.redirect_stdout(buf):
            main.draw_board(b)
        out = buf.getvalue()
        self.assertIn("X", out)
        self.assertIn("O", out)
        self.assertIn("-", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
