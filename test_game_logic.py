import pytest
from game_logic import isWinning, evaluate, next_State, get_available_pieces, get_available_positions

def test_isWinning_true():
    board = ['BDFP'] * 4 + [None] * 12
    assert isWinning(board) is True

def test_isWinning_false():
    board = ['BDFP', 'SDEP', None, 'SDEC'] + [None] * 12
    assert isWinning(board) is False

def test_next_state():
    state = {
        "board": [None] * 16,
        "piece": "BDFP",
        "current": 0
    }
    move = {"pos": 0, "piece": "SDEC"}
    new_state = next_State(state, move)

    assert new_state["board"][0] == "BDFP"
    assert new_state["piece"] == "SDEC"
    assert new_state["current"] == 1

def test_evaluate_returns_int():
    state = {
        "board": [None] * 16,
        "piece": None,
        "current": 0
    }
    score = evaluate(state, 0)
    assert isinstance(score, int)

def test_get_available_pieces():
    state={
        "board": [None] * 16,
        "piece": "BDFP",
        "current": 0
    }
    pieces = get_available_pieces(state)
    assert len(pieces)==15

def test_get_available_positions():
    state={
        "board": [None] * 16,
        "piece": "BDFP",
        "current": 0
    }
    positions=get_available_positions(state)
    assert len(positions)==16
