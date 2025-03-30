from abc import ABC, abstractmethod

class CurrencyConverter(ABC):
    """
    Абстрактный базовый класс для конвертеров валют.
    Определяет интерфейс для всех конвертеров.
    """
    @abstractmethod
    def convert_usd(self, amount, to_currency) -> float:
        """
        Абстрактный метод для конвертации USD в другую валюту.

        Args:
            amount (float): Сумма в USD для конвертации.
            to_currency (str): Код валюты, в которую нужно конвертировать (например, 'EUR', 'RUB').

        Returns:
            float: Конвертированная сумма в указанной валюте или None в случае ошибки.
        """
        pass