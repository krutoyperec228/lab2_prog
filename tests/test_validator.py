"""Тесты логики проверки одного VIN."""

import pytest

from vin import is_valid_format, is_valid_with_checksum

VALID_VIN = "1HGCM82633A004352"
VALID_VIN_X = "1M8GDM9AXKP042788"


class TestFormat:
    @pytest.mark.parametrize("vin", [
        VALID_VIN, "JH4KA8260MC000000", "WBA3A5C50DF123456", VALID_VIN_X,
    ])
    def test_valid(self, vin):
        assert is_valid_format(vin) is True

    @pytest.mark.parametrize("vin, reason", [
        ("1HGCM82633A00435",   "16 символов"),
        ("1HGCM82633A0043521", "18 символов"),
        ("1HGCM8263IA004352",  "запрещённая I на позиции 9 (индекс 8)"),
        ("1HGCM8263OA004352",  "запрещённая O на позиции 9 (индекс 8)"),
        ("1HGCM8263QA004352",  "запрещённая Q на позиции 9 (индекс 8)"),
        ("1HGCM8263!A004352",  "спецсимвол на позиции 9 (индекс 8)"),
        ("",                   "пустая строка"),
    ])
    def test_invalid(self, vin, reason):
        assert is_valid_format(vin) is False, reason

    def test_y_on_position_10_is_valid(self):
        # 'Y' на позиции 10 разрешена
        assert is_valid_format("1HGCM8263YA004352") is True

    def test_y_on_position_9_is_invalid(self):
        # 'Y' на позиции 9 — недопустимый контрольный символ
        assert is_valid_format("1HGCM826YA004352") is False


class TestChecksum:
    def test_valid(self):
        assert is_valid_with_checksum(VALID_VIN) is True

    def test_valid_with_x(self):
        assert is_valid_with_checksum(VALID_VIN_X) is True

    def test_invalid_last_digit(self):
        assert is_valid_with_checksum("1HGCM82633A004353") is False

    def test_invalid_control_position(self):
        # Меняем контрольный символ (позиция 9, индекс 8) с '3' на '1'
        assert is_valid_with_checksum("1HGCM82613A004352") is False

    def test_short_circuits_on_bad_format(self):
        assert is_valid_with_checksum("SHORT") is False