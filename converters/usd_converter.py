from abc import ABC
from converters.currency_converter import CurrencyConverter

class UsdConverter(CurrencyConverter, ABC):
    """
    Абстрактный класс, представляющий конвертер из USD в другие валюты.

    Предоставляет базовую структуру и требует реализации методов
    для получения обменного курса и выполнения конвертации в конкретную валюту.
    """
    def __init__(self, rate_fetcher) -> None:
        """
        Инициализация UsdConverter.

        Args:
            rate_fetcher (RateFetcher): Экземпляр RateFetcher для получения обменных курсов.
        """
        self.rate_fetcher = rate_fetcher

    def get_exchange_rate(self) -> float:
        """
        Абстрактный метод для получения обменного курса для конкретной валюты.
        Должен быть реализован в подклассах.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError(f"{self.__class__.__name__} должен реализовать метод "
                                  "get_exchange_rate для получения курса конкретной валюты.")

    def convert_usd(self, amount, to_currency) -> float:
        """
        Абстрактный метод для конвертации USD в конкретную валюту.
        Должен быть реализован в подклассах.

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError(f"{self.__class__.__name__} должен реализовать метод "
                                  "convert_usd для конвертации в конкретную валюту.")