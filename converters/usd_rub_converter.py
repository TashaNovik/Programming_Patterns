from converters.usd_converter import UsdConverter
from converters.rate_fetcher import RateFetcher

class UsdRubConverter(UsdConverter):
    """
    Конвертер USD в RUB (российский рубль).
    Использует RateFetcher для получения обменных курсов.
    """
    def __init__(self, rate_fetcher=None) -> None:
        """
        Инициализация UsdRubConverter.

        Args:
            rate_fetcher (RateFetcher, optional): Экземпляр RateFetcher.
                                                 Если None, создается новый экземпляр.
        """
        super().__init__(rate_fetcher or RateFetcher())
        self.rates = self.get_exchange_rate()


    def get_exchange_rate(self) -> float | None:
        """
        Получение обменного курса USD к RUB.

        Возвращает обменный курс или None в случае ошибки.
        """
        rates_data = self.rate_fetcher.fetch_rates()
        if rates_data and 'rates' in rates_data:
            return rates_data['rates'].get('RUB')
        return None

    def convert_usd_to_rub(self, amount) -> float | None:
        """
        Конвертация USD в RUB.

        Args:
            amount (float): Сумма в USD.

        Returns:
            float: Сумма в RUB или None в случае ошибки получения курса.
        """
        if self.rates is not None:
            return amount * self.rates
        return None

    def convert_usd(self, amount, to_currency) -> float | None:
        """
        Конвертация USD в указанную валюту (поддерживается только RUB).

        Args:
            amount (float): Сумма в USD.
            to_currency (str): Код валюты назначения.

        Returns:
            float: Сумма в RUB или None, если валюта не поддерживается
                   или произошла ошибка при получении курса.
        """
        if to_currency == 'RUB':
            return self.convert_usd_to_rub(amount)
        else:
            print(f"UsdRubConverter не поддерживает конвертацию в {to_currency}. "
                  f"Поддерживается только конвертация в RUB.")
            return None