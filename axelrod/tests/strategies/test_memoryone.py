"""Tests for the Memoryone strategies."""

import unittest

import axelrod
from axelrod import Game
from axelrod.strategies.memoryone import MemoryOnePlayer, LRPlayer
from .test_player import TestPlayer, test_four_vector

C, D = axelrod.Actions.C, axelrod.Actions.D


class TestGenericPlayerOne(unittest.TestCase):
    """A class to test the naming and classification of generic memory one
    players."""
    p1 = axelrod.MemoryOnePlayer(four_vector=(0, 0, 0, 0))
    p2 = axelrod.MemoryOnePlayer(four_vector=(1, 0, 1, 0))
    p3 = axelrod.MemoryOnePlayer(four_vector=(1, 0.5, 1, 0.5))

    def test_name(self):
        self.assertEqual(self.p1.name,
                         "Generic Memory One Player: (0, 0, 0, 0)")
        self.assertEqual(self.p2.name,
                         "Generic Memory One Player: (1, 0, 1, 0)")
        self.assertEqual(self.p3.name,
                         "Generic Memory One Player: (1, 0.5, 1, 0.5)")

    def test_stochastic_classification(self):
        self.assertFalse(self.p1.classifier['stochastic'])
        self.assertFalse(self.p2.classifier['stochastic'])
        self.assertTrue(self.p3.classifier['stochastic'])


class TestWinStayLoseShift(TestPlayer):

    name = "Win-Stay Lose-Shift: C"
    player = axelrod.WinStayLoseShift
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_class_classification(self):
        self.assertEqual(self.player.classifier,
                         self.expected_classifier)

    def test_strategy(self):
        # Check that switches if does not get best payoff.
        actions = [(C, C), (C, D), (D, C), (D, D), (C, C)]
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions)


class TestWinShiftLoseStayTestPlayer(TestPlayer):

    name = "Win-Shift Lose-Stay: D"
    player = axelrod.WinShiftLoseStay
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        # Check that switches if does not get best payoff.
        actions = [(D, C), (C, D), (C, C), (D, D), (D, C)]
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions)


class TestGTFT(TestPlayer):

    name = "GTFT: 0.33"
    player = axelrod.GTFT
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions, seed=0)

        actions = [(C, C), (C, D), (C, C), (C, D), (D, C)]
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions, seed=1)

    def test_four_vector(self):
        (R, P, S, T) = Game().RPST()
        p = min(1 - (T - R) / (R - S), (R - P) / (T - P))
        expected_dictionary = {(C, C): 1., (C, D): p, (D, C): 1., (D, D): p}
        test_four_vector(self, expected_dictionary)

    def test_allow_for_zero_probability(self):
        player = self.player(p=0)
        expected = {(C, C): 1., (C, D): 0, (D, C): 1., (D, D): 0}
        self.assertAlmostEqual(player._four_vector, expected)


class TestFirmButFair(TestPlayer):

    name = "Firm But Fair"
    player = axelrod.FirmButFair
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 1, (C, D): 0, (D, C): 1, (D, D): 2/3}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):

        actions = [(C, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions)

        actions = [(C, D), (D, D), (D, D), (D, D), (C, D)]
        self.versus_test(opponent=axelrod.Defector(),
                         expected_actions=actions, seed=0)

        actions = [(C, D), (D, D), (C, D), (D, D), (D, D)]
        self.versus_test(opponent=axelrod.Defector(),
                         expected_actions=actions, seed=1)


class TestStochasticCooperator(TestPlayer):

    name = "Stochastic Cooperator"
    player = axelrod.StochasticCooperator
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 0.935, (C, D): 0.229, (D, C): 0.266,
                               (D, D): 0.42}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        actions = [(C, C), (D, D), (C, C), (C, D), (C, C), (D, D)]
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions, seed=15)

        actions = [(C, C), (C, D), (D, C), (D, D), (C, C), (C, D)]
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions, seed=1)

        actions = [(C, C), (C, D), (D, C), (D, D), (D, C), (D, D)]
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions, seed=3)

        actions = [(C, C), (C, D), (D, C), (D, D), (D, C), (C, D)]
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions, seed=13)


class TestStochasticWSLS(TestPlayer):

    name = "Stochastic WSLS: 0.05"
    player = axelrod.StochasticWSLS
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        actions = [(C, C), (D, D), (C, C), (C, D), (D, C), (D, D)]
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions, seed=2)

        actions = [(C, C), (C, D), (D, C), (D, D), (C, C), (C, D)]
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions, seed=31)

        actions = [(C, D), (D, C), (D, D), (C, C), (C, D), (D, C)]
        self.versus_test(opponent=axelrod.CyclerDC(),
                         expected_actions=actions, seed=2)

        actions = [(C, D), (C, C), (C, D), (D, C), (D, D), (C, C)]
        self.versus_test(opponent=axelrod.CyclerDC(),
                         expected_actions=actions, seed=31)

    def test_four_vector(self):
        player = self.player()
        ep = player.ep
        expected_dictionary = {(C, C): 1. - ep, (C, D): ep, (D, C): ep,
                               (D, D): 1. - ep}
        test_four_vector(self, expected_dictionary)


class TestMemoryOnePlayer(unittest.TestCase):

    def test_exception_if_four_vector_not_set(self):
        player = MemoryOnePlayer()
        opponent = axelrod.Player()
        with self.assertRaises(ValueError):
            player.strategy(opponent)

    def test_exception_if_probability_vector_outside_valid_values(self):
        player = MemoryOnePlayer()
        x = 2.
        with self.assertRaises(ValueError):
            player.set_four_vector([0.1, x, 0.5, 0.1])


class TestLRPlayer(unittest.TestCase):

    def test_exception(self):
        player = LRPlayer()
        with self.assertRaises(ValueError):
            player.receive_match_attributes(0, 0, -float("inf"))


class TestZDExtort2(TestPlayer):

    name = "ZD-Extort-2: 0.1111111111111111, 0.5"
    player = axelrod.ZDExtort2
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 8/9, (C, D): 0.5, (D, C): 1/3,
                               (D, D): 0.}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        actions = [(C, C), (D, D), (D, C), (D, D), (D, C), (C, D)]
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions, seed=2)

        actions = [(C, C), (C, D), (C, C), (C, D), (D, C), (C, D)]
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions, seed=31)

        actions = [(C, D), (D, C), (D, D), (D, C), (C, D), (C, C)]
        self.versus_test(opponent=axelrod.CyclerDC(),
                         expected_actions=actions, seed=2)

        actions = [(C, D), (C, C), (C, D), (C, C), (C, D), (C, C)]
        self.versus_test(opponent=axelrod.CyclerDC(),
                         expected_actions=actions, seed=31)


class TestZDExtort2v2(TestPlayer):

    name = "ZD-Extort-2 v2: 0.125, 0.5, 1"
    player = axelrod.ZDExtort2v2
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 7/8, (C, D): 7/16, (D, C): 3/8,
                               (D, D): 0.}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        actions = [(C, C), (D, D), (D, C), (D, D), (D, C), (C, D)]
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions, seed=2)

        actions = [(C, D), (D, C), (D, D), (D, C), (D, D), (D, C)]
        self.versus_test(opponent=axelrod.CyclerDC(),
                         expected_actions=actions, seed=5)


class TestZDExtort4(TestPlayer):

    name = "ZD-Extort-4: 0.23529411764705882, 0.25, 1"
    player = axelrod.ZDExtort4
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 11/17, (C, D): 0, (D, C): 8/17,
                               (D, D): 0.}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        actions = [(C, C), (D, D), (D, C), (D, D), (D, C), (C, D)]
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions, seed=2)

        actions = [(C, D), (D, C), (D, D), (D, C), (D, D), (D, C)]
        self.versus_test(opponent=axelrod.CyclerDC(),
                         expected_actions=actions, seed=5)


class TestZDGen2(TestPlayer):

    name = "ZD-GEN-2: 0.125, 0.5, 3"
    player = axelrod.ZDGen2
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 1, (C, D): 9/16, (D, C): 1/2,
                               (D, D): 1/8}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):

        actions = [(C, C), (C, D), (D, C), (D, D), (C, C), (C, D)]
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions, seed=2)

        actions = [(C, C), (C, D), (C, C), (C, D), (C, C), (C, D)]
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions, seed=31)

        actions = [(C, D), (D, C), (D, D), (C, C), (C, D), (C, C)]
        self.versus_test(opponent=axelrod.CyclerDC(),
                         expected_actions=actions, seed=2)

        actions = [(C, D), (C, C), (C, D), (C, C), (C, D), (C, C)]
        self.versus_test(opponent=axelrod.CyclerDC(),
                         expected_actions=actions, seed=31)


class TestZDGTFT2(TestPlayer):

    name = "ZD-GTFT-2: 0.25, 0.5"
    player = axelrod.ZDGTFT2
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 1., (C, D): 1/8, (D, C): 1.,
                               (D, D): 0.25}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C), (C, D)]
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions, seed=2)

        actions = [(C, C), (C, D), (C, C), (C, D), (C, C), (C, D)]
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions, seed=31)

        actions = [(C, D), (D, C), (C, D), (D, C), (C, D), (C, C)]
        self.versus_test(opponent=axelrod.CyclerDC(),
                         expected_actions=actions, seed=2)

        actions = [(C, D), (C, C), (C, D), (C, C), (C, D), (D, C)]
        self.versus_test(opponent=axelrod.CyclerDC(),
                         expected_actions=actions, seed=31)


class TestZDSet2(TestPlayer):

    name = "ZD-SET-2: 0.25, 0.0, 2"
    player = axelrod.ZDSet2
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 3/4, (C, D): 1/4, (D, C): 1/2,
                               (D, D): 1/4}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        actions = [(C, C), (D, D), (D, C), (C, D), (C, C), (D, D)]
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions, seed=2)

        actions = [(C, D), (D, C), (D, D), (D, C), (D, D), (D, C)]
        self.versus_test(opponent=axelrod.CyclerDC(),
                         expected_actions=actions, seed=5)


class TestSoftJoss(TestPlayer):

    name = "Soft Joss: 0.9"
    player = axelrod.SoftJoss
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_four_vector(self):
        expected_dictionary = {(C, C): 1, (C, D): 0.1, (D, C): 1., (D, D): 0.1}
        test_four_vector(self, expected_dictionary)

    def test_strategy(self):
        actions = [(C, C), (C, D), (D, C), (C, D), (D, C), (C, D)]
        self.versus_test(opponent=axelrod.Alternator(),
                         expected_actions=actions, seed=2)

        actions = [(C, D), (D, C), (C, D), (D, C), (C, D), (D, C)]
        self.versus_test(opponent=axelrod.CyclerDC(),
                         expected_actions=actions, seed=5)


class TestALLCorALLD(TestPlayer):

    name = "ALLCorALLD"
    player = axelrod.ALLCorALLD
    expected_classifier = {
        'memory_depth': 1,
        'stochastic': True,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def test_strategy(self):
        actions = [(D, C)] * 10
        self.versus_test(opponent=axelrod.Cooperator(),
                         expected_actions=actions, seed=0)
        actions = [(C, C)] * 10
        self.versus_test(opponent=axelrod.Cooperator(),
                         expected_actions=actions, seed=1)
