"""Testes unitários para main.py (paradigma funcional) - usa unittest."""
import io
import json
import os
import tempfile
import unittest

import main


class TestBoard(unittest.TestCase):
    def test_empty_board_nove_posicoes(self):
        b = main.empty_board()
        self.assertEqual(len(b), 9)
        self.assertTrue(all(c == main.EMPTY for c in b))
        self.assertIsInstance(b, tuple)  # imutável

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
        self.assertFalse(main.is_full(main.empty_board()))

    def test_empty_cells(self):
        b = (main.X, main.EMPTY, main.O,
             main.EMPTY, main.X, main.EMPTY,
             main.O, main.EMPTY, main.X)
        self.assertEqual(main.get_empty_cells(b), (1, 3, 5, 7))

    def test_score_for(self):
        self.assertEqual(main.score_for(main.X), 1)
        self.assertEqual(main.score_for(main.O), -1)
        self.assertEqual(main.score_for(None), 0)


class TestMovimentos(unittest.TestCase):
    def test_naive_cria_novo_board_imutavel(self):
        import random
        b = main.empty_board()
        b2 = main.naive(b, main.X, random.Random(0))
        self.assertEqual(b, main.empty_board())
        self.assertNotEqual(b, b2)
        self.assertEqual(sum(1 for c in b2 if c != main.EMPTY), 1)

    def test_bee_joga_em_celula_vazia(self):
        import random
        b = main.empty_board()
        b2 = main.bee(b, main.X, random.Random(0))
        self.assertEqual(sum(1 for c in b2 if c != main.EMPTY), 1)
        self.assertIn(main.X, b2)

    def test_bee_primeiro_turno_joga_otimo(self):
        """Centro ou canto são ótimos primeiros lances."""
        import random
        b2 = main.bee(main.empty_board(), main.X, random.Random(0))
        cell = next(i for i, c in enumerate(b2) if c != main.EMPTY)
        self.assertIn(cell, (0, 2, 4, 6, 8))  # cantos e centro são ótimos


class TestMinimax(unittest.TestCase):
    def test_minimax_vitoria_x(self):
        b = (main.X, main.X, main.X,
             main.O, main.O, main.EMPTY,
             main.EMPTY, main.EMPTY, main.EMPTY)
        score, _ = main.minimax(b, main.O)
        self.assertGreater(score, 0)  # X venceu, score positivo

    def test_minimax_bloqueio_critical(self):
        # O tem ameaça própria em 5 (ganha); X deve bloquear ou ganhar
        b = (main.X, main.X, main.EMPTY,
             main.O, main.O, main.EMPTY,
             main.EMPTY, main.EMPTY, main.EMPTY)
        score, cell = main.minimax(b, main.O)
        self.assertEqual(cell, 5)  # O joga 5 e vence (linha 1 completa)


class TestPartida(unittest.TestCase):
    def test_play_game_formato(self):
        g = main.play_game(main.bee, main.naive, seed=5)
        for key in ("J1", "V", "J2", "N", "board", "rounds"):
            self.assertIn(key, g)
        self.assertIn(g["V"], (-1, 0, 1))
        self.assertEqual(len(g["board"]), 9)

    def test_bee_nunca_perde_vs_naive(self):
        for seed in range(3):
            results = main.compete("naive", "bee", rounds=20,
                                   start_player=1, seed=100 + seed)
            for g in results:
                # V=1 → J1(X) venceu; se J2=bee então bee perdeu
                if g["J2"] == "bee" and g["V"] == 1:
                    self.fail(f"bee perdeu (J2) seed={seed}")
                # V=-1 → J2(O) venceu; se J1=bee então bee perdeu
                if g["J1"] == "bee" and g["V"] == -1:
                    self.fail(f"bee perdeu (J1) seed={seed}")

    def test_bee_vs_bee_sempre_empata(self):
        results = main.compete("bee", "bee", rounds=15,
                               start_player=1, seed=42)
        for g in results:
            self.assertEqual(g["V"], 0, "dois bees devem empatar")

    def test_compete_conta_rndos(self):
        results = main.compete("naive", "bee", rounds=10,
                               start_player=1, seed=0)
        self.assertEqual(len(results), 10)

    def test_summarize_conta_total_jogadores(self):
        results = main.compete("naive", "bee", rounds=10,
                               start_player=1, seed=3)
        s = main.summarize(results)
        self.assertIn("naive", s)
        self.assertIn("bee", s)
        total = sum(v["W"] + v["D"] + v["L"] for v in s.values())
        self.assertEqual(total, 20)  # 10 games * 2 players

    def test_save_json_e_txt(self):
        results = main.compete("naive", "bee", rounds=5,
                               start_player=1, seed=0)
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
            self.assertIn("SUMÁRIO", txt)
            self.assertIn("J1", txt)

    def test_bee_dominna_naive_estatistica(self):
        results = main.compete("naive", "bee", rounds=20,
                               start_player=1, seed=11)
        s = main.summarize(results)
        self.assertEqual(s["bee"]["L"], 0)
        self.assertGreaterEqual(s["bee"]["W"], 15)


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
        self.assertIn("-", out)  # separadores


if __name__ == "__main__":
    unittest.main(verbosity=2)
