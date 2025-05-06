import unittest
from Quarto_KD import isWinning, evaluate, next_State

class TestGameLogic(unittest.TestCase):

    def test_isWinning(self):
        board = ['BDPC'] * 4 + [None] * 12
        self.assertTrue(isWinning(board))

    def test_next_state(self):
        state = {"board": [None] * 16, "piece": "BDPC", "current": 0}
        move = {"pos": 0, "piece": "SDPC"}
        new_state = next_State(state, move)
        self.assertEqual(new_state["board"][0], "BDPC")
        self.assertEqual(new_state["piece"], "SDPC")
        self.assertEqual(new_state["current"], 1)

    def test_evaluate(self):
        state = {"board": [None] * 16, "piece": None, "current": 0}
        self.assertIsInstance(evaluate(state, 0), int)

if __name__ == "__main__":
    unittest.main()