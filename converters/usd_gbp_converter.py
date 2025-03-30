import logging
from typing import Any

from converters.usd_converter import UsdConverter
from converters.rate_fetcher import RateFetcher

class UsdGbpConverter(UsdConverter):
    """
    Конвертер USD в GBP (британский фунт стерлингов).
    Использует RateFetcher для получения обменных курсов.
    """
    def __init__(self, rate_fetcher=None) -> None:
        """
        Инициализация UsdGbpConverter.

        Args:
            rate_fetcher (RateFetcher, optional): Экземпляр RateFetcher.
                                                 Если None, создается новый экземпляр.
        """
        super().__init__(rate_fetcher or RateFetcher())
        self.logger = self._setup_logger()
        self.rates = self.get_exchange_rate()


    def _setup_logger(self) -> logging.Logger:
        """Настройка логгера."""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def get_exchange_rate(self) -> Any | None:
        """
        Получение обменного курса USD к GBP.

        Возвращает обменный курс или None в случае ошибки.
        """
        rates_data = self.rate_fetcher.fetch_rates()
        if rates_data and 'rates' in rates_data:
            return rates_data['rates'].get('GBP')
        return None


    def convert_usd_to_gbp(self, amount) -> float | None:
        """
        Конвертация USD в GBP.

        Args:
            amount (float): Сумма в USD.

        Returns:
            float: Сумма в GBP или None в случае ошибки получения курса.
        """
        if self.rates is not None:
            return amount * self.rates
        return None

    def convert_usd(self, amount, to_currency) -> float | None:
        """
        Конвертация USD в указанную валюту (поддерживается только GBP).

        Args:
            amount (float): Сумма в USD.
            to_currency (str): Код валюты назначения.

        Returns:
            float: Сумма в GBP или None, если валюта не поддерживается
                   или произошла ошибка при получении курса.
        """
        if to_currency == 'GBP':
            return self.convert_usd_to_gbp(amount)
        else:
            print(f"UsdGbpConverter не поддерживает конвертацию в {to_currency}. "
                  f"Поддерживается только конвертация в GBP.")
            return None