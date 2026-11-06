"""Логика проверки одного VIN."""

from vin.constants import TRANSLITERATION, VIN_PATTERN, WEIGHTS


def _normalize(vin: str) -> str:
    """Приводит VIN к верхнему регистру и убирает пробелы по краям."""
    return vin.strip().upper()


def is_valid_format(vin: str) -> bool:
    """Проверка структуры VIN.
    Не проверяет контрольную цифру.
    """
    return VIN_PATTERN.fullmatch(_normalize(vin)) is not None


def is_valid_with_checksum(vin: str) -> bool:
    """Полная проверка: формат + контрольная цифра на позиции 9.

    Алгоритм (ISO 3779):
      1. Каждый символ, кроме контрольного, переводится в число
         по TRANSLITERATION.
      2. Умножается на вес своей позиции из WEIGHTS.
      3. Сумма делится на 11; остаток 10 → 'X', иначе — цифра.
      4. Сравнивается с символом на позиции 9 (индекс 8).
    """
    normalized = _normalize(vin)
    if not VIN_PATTERN.fullmatch(normalized):
        return False

    total = 0
    for i, char in enumerate(normalized):
        if i == 8:# индекс 8 == позиция 9 (контрольный символ)
            continue
        total += TRANSLITERATION[char] * WEIGHTS[i]

    remainder = total % 11
    expected = 'X' if remainder == 10 else str(remainder)
    return normalized[8] == expected