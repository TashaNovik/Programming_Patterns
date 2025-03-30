from converters import *

def main() -> None:
    """
    Основная функция для запуска конвертера валют.

    Запрашивает у пользователя сумму в USD, конвертирует ее в RUB, EUR, GBP, CNY
    и выводит результаты на экран.
    """
    try:
        amount_str = input('Введите значение в USD: \n')
        amount = int(amount_str)
        if amount < 0:
            print("Значение USD не может быть отрицательным.")
            return
    except ValueError:
        print("Некорректный ввод. Пожалуйста, введите целое число, представляющее сумму в USD.") # Более понятное сообщение
        return

    converters = {
        "RUB": UsdRubConverter(),
        "EUR": UsdEurConverter(),
        "GBP": UsdGbpConverter(),
        "CNY": UsdCnyConverter(),
    }

    for currency, converter in converters.items():
        converted_amount = converter.convert_usd(amount, currency)
        if converted_amount is not None:
            print(f"{amount} USD to {currency}: {converted_amount}")
        else:
            print(f"Не удалось конвертировать {amount} USD в {currency}.")


if __name__ == "__main__":
    main()