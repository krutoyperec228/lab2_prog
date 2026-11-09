"""CLI для проверки и поиска VIN."""

from pathlib import Path
import requests

from vin import find_vins_in_text, is_valid_format, is_valid_with_checksum


def print_results(found: list[str]) -> None:
    if not found:
        print("VIN не найдены.")
        return
    print(f"Найдено VIN: {len(found)}")
    for vin in found:
        if is_valid_with_checksum(vin):
            print(f"  {vin}")
        else:
            print(f"  {vin} (формат верный, контрольная цифра не совпадает)")


def run_interactive() -> None:
    print("VIN Validator")
    vin = input("Введите VIN для проверки: ").strip()
    if is_valid_with_checksum(vin):
        print("VIN корректен.")
    elif is_valid_format(vin):
        print("Формат верный, контрольная цифра не совпадает.")
    else:
        print("Неверный формат VIN.")


def run_from_url() -> None:
    url = input("Введите URL страницы для поиска VIN: ").strip()
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # выбросит исключение при статусах 4xx/5xx
        html = response.text
    except requests.RequestException as e:
        print(f"Ошибка загрузки URL: {e}")
        return

    print_results(find_vins_in_text(html))


def run_from_file() -> None:
    path = Path(input("Введите путь к файлу: ").strip())
    if not path.is_file():
        print("Файл не найден.")
        return
    text = path.read_text(encoding='utf-8', errors='ignore')
    print_results(find_vins_in_text(text))


def main() -> None:
    print("Выберите режим:")
    print("1 - Проверить один VIN")
    print("2 - Найти VIN на веб-странице")
    print("3 - Найти VIN в файле")
    choice = input("> ").strip()

    if choice == "1":
        run_interactive()
    elif choice == "2":
        run_from_url()
    elif choice == "3":
        run_from_file()
    else:
        print("Неверный выбор.")


if __name__ == "__main__":
    main()