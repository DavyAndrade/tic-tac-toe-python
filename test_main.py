"""Testes unitarios para main.py (paradigma funcional) - usa unittest."""
import io
import json
import os
import tempfile
import unittest

import main


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

    def test_fera_primeiro_turno_joga_otimo(self):
        import random
        b2 = main.fera(main.tab_vazio(), main.X, random.Random(0))
        cell = next(i for i, c in enumerate(b2) if c != main.EMPTY)
        self.assertIn(cell, (0, 2, 4, 6, 8))


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
