"""Интеграционный тест: поиск VIN на реальной странице absolutins.ru."""

import pytest
import requests

from vin import find_vins_in_text, is_valid_format

URL = "https://www.absolutins.ru/blog/rasshifrovka-vin-koda-avtomobilya/"
EXPECTED_VINS = [
    "JHMCM56557C404453",
    "WBA7E0C59GGM56193",
]

@pytest.fixture(scope="module")
def html():
    response = requests.get(URL, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    return response.text


@pytest.mark.integration
class TestAbsolutinsPage:
    def test_finds_all_expected_vins(self, html):
        found = set(find_vins_in_text(html))
        for vin in EXPECTED_VINS:
            assert vin in found, f"VIN {vin} не найден. Найдено: {found}"

    def test_finds_at_least_two_unique_vins(self, html):
        found = set(find_vins_in_text(html))
        assert len(found) >= 2, f"Ожидалось >=2 уникальных VIN, найдено {len(found)}: {found}"

    def test_all_found_are_structurally_valid(self, html):
        for vin in set(find_vins_in_text(html)):
            assert is_valid_format(vin), f"{vin} не проходит is_valid_format"
