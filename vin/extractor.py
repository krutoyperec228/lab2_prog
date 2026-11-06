"""Логика поиска VIN в произвольном тексте.
Задача: извлечь все потенциальные VIN из текста.
"""

from vin.constants import VIN_SEARCH_PATTERN


def find_vins_in_text(text: str) -> list[str]:
    """Находит все потенциальные VIN в тексте (по структуре).
    Контрольная цифра не проверяется
    """
    return VIN_SEARCH_PATTERN.findall(text.upper())