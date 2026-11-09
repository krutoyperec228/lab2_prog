"""Тесты поиска VIN в файле через parametrize."""

from pathlib import Path

import pytest

from vin import find_vins_in_text, is_valid_format, is_valid_with_checksum

DATA = Path(__file__).parent.parent / "data"


@pytest.fixture(scope="module")
def text():
    return (DATA / "vins.txt").read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def found(text):
    return set(find_vins_in_text(text))


# VIN, которые должны находиться

@pytest.mark.parametrize("vin", [
    "1HGCM82633A004352",
    "1M8GDM9AXKP042788",
    "JH4KA8260MC000000",
    "WBA3A5C50DF123456",
    "5YJ3E1EA7KF317000",
])
def test_expected_vin_is_found(found, vin):
    assert vin in found, f"{vin} не найден. Найдено: {found}"


# VIN, которые проходят полную проверку

@pytest.mark.parametrize("vin", [
    "1HGCM82633A004352",
    "1M8GDM9AXKP042788",
    "WBA3A5C50DF123456",
])
def test_vin_passes_checksum(found, vin):
    assert vin in found
    assert is_valid_with_checksum(vin), f"{vin} не проходит checksum"


# VIN, которые структурно валидны, но checksum не сходится

@pytest.mark.parametrize("vin", [
    "JH4KA8260MC000000",
    "5YJ3E1EA7KF317000",
])
def test_vin_structurally_valid_only(found, vin):
    assert vin in found
    assert is_valid_format(vin)
    assert not is_valid_with_checksum(vin)


# Мусор, который НЕ должен находиться

@pytest.mark.parametrize("garbage, reason", [
    ("A1HGCM82633A004352B", "VIN внутри токена — lookaround блокирует"),
    ("X1HGCM82633A004352",  "VIN внутри токена — lookaround блокирует"),
    ("1HGCM82633A004352X",  "VIN внутри токена — lookaround блокирует"),
    ("XW8ZZZ61ZLG028617",   "позиция 9 = Z, не VIN по ISO 3779"),
    ("WVWZZZ1JZXW000001",   "позиция 9 = Z, не VIN по ISO 3779"),
    ("1HGCM8263IA004352",   "запрещённая I на позиции 9"),
    ("1HGCM8263OA004352",   "запрещённая O на позиции 9"),
    ("1HGCM8263QA004352",   "запрещённая Q на позиции 9"),
    ("1HGCM82633A00435",    "16 символов — слишком коротко"),
    ("1HGCM82633A0043521",  "18 символов — слишком длинно"),
])
def test_garbage_not_found(found, garbage, reason):
    assert garbage not in found, f"{garbage} ошибочно найден ({reason})"


# Разделители не мешают поиску

@pytest.mark.parametrize("vin, separator", [
    ("1HGCM82633A004352", "подчёркивание (VIN_...)"),
    ("WBA3A5C50DF123456", "кириллица (ВИН...)"),
    ("JH4KA8260MC000000", "двоеточие (Код: ...)"),
    ("1M8GDM9AXKP042788", "квадратные скобки ([...])"),
    ("5YJ3E1EA7KF317000", "кавычки (\"...\")"),
])
def test_separator_does_not_block_search(found, vin, separator):
    assert vin in found, f"{vin} не найден рядом с разделителем: {separator}"