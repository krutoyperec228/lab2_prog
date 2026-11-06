"""Тесты согласованности констант."""

from vin.constants import TRANSLITERATION, VIN_PATTERN, WEIGHTS


def test_transliteration_covers_all_pattern_chars():
    allowed = set("ABCDEFGHJKLMNPRSTUVWXYZ0123456789")
    assert set(TRANSLITERATION.keys()) == allowed


def test_forbidden_letters_absent():
    for letter in "IOQ":
        assert letter not in TRANSLITERATION


def test_weights_length():
    assert len(WEIGHTS) == 17


def test_control_position_weight_is_zero():
    # Позиция 9 не должна влиять на сумму
    assert WEIGHTS[8] == 0


def test_pattern_rejects_forbidden_letters():
    assert VIN_PATTERN.fullmatch("1HGCI82633A004352") is None
    assert VIN_PATTERN.fullmatch("1HGCO82633A004352") is None
    assert VIN_PATTERN.fullmatch("1HGCQ82633A004352") is None