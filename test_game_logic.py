import pytest
from game_logic import isWinning, evaluate, next_State

def test_isWinning_true():
    board = ['BDPC'] * 4 + [None] * 12
    assert isWinning(board) is True

def test_isWinning_false():
    board = ['BDPC', 'SDPC', None, 'LDPC'] + [None] * 12
    assert isWinning(board) is False

def test_next_state():
    state = {
        "board": [None] * 16,
        "piece": "BDPC",
        "current": 0
    }
    move = {"pos": 0, "piece": "SDPC"}
    new_state = next_State(state, move)

    assert new_state["board"][0] == "BDPC"
    assert new_state["piece"] == "SDPC"
    assert new_state["current"] == 1

def test_evaluate_returns_int():
    state = {
        "board": [None] * 16,
        "piece": None,
        "current": 0
    }
    score = evaluate(state, 0)
    assert isinstance(score, int)