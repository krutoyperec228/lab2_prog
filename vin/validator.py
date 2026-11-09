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

    Алгоритм (ISO 3779)
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