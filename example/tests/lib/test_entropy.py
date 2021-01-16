from src.lib import entropy


def test_binary():
    assert entropy.binary(0.5) == 1
