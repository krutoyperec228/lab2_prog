"""Тесты логики поиска VIN в тексте."""

import pytest

from vin import find_vins_in_text

VALID_VIN = "1HGCM82633A004352"


class TestExtraction:
    def test_find_two(self):
        text = f"VIN: {VALID_VIN}, старый: WBA3A5C50DF123456."
        found = find_vins_in_text(text)
        assert len(found) == 2
        assert VALID_VIN in found

    def test_find_none(self):
        assert find_vins_in_text("нет VIN, только 12345") == []

    def test_lowercase_normalized(self):
        assert find_vins_in_text(f"vin: {VALID_VIN.lower()}") == [VALID_VIN]

    def test_forbidden_char_inside_window(self):
        # 'I' на позиции 5 внутри 17-символьного окна
        assert find_vins_in_text("1HGCI82633A004352") == []

    def test_no_partial_match_inside_alnum_token(self):
        # Латиница/цифры вокруг — часть более длинного токена
        assert find_vins_in_text("A" + VALID_VIN) == []
        assert find_vins_in_text(VALID_VIN + "B") == []

    @pytest.mark.parametrize("template", [
        "VIN_{}", "{}_old", "_x_{}_y_", "ВИН{}", "VIN: {}",
    ])
    def test_separators_allowed(self, template):
        # '_', кириллица, двоеточие — разделители, VIN извлекается
        assert find_vins_in_text(template.format(VALID_VIN)) == [VALID_VIN]

    def test_empty_text(self):
        assert find_vins_in_text("") == []