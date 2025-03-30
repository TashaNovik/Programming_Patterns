from converters import *

def main():
    try:
        amount_str = input('Введите значение в USD: \n')
        amount = int(amount_str)
        if amount < 0:
            print("Значение USD не может быть отрицательным.")
            return
    except ValueError:
        print("Пожалуйста, введите целое число.")
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