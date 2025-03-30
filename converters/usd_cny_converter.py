import json
import time
import os
from typing import Any

from converters.usd_converter import UsdConverter
from converters.rate_fetcher import RateFetcher

class UsdCnyConverter(UsdConverter):
    """
    Конвертер USD в CNY (китайский юань).

    Использует RateFetcher для получения обменных курсов и кэширования.
    """
    def __init__(self, rate_fetcher=None, cache_file="exchange_rates.json", cache_expiry=3600) -> None:
        """
        Инициализация UsdCnyConverter.

        Args:
            rate_fetcher (RateFetcher, optional): Экземпляр RateFetcher.
                                                 Если None, создается новый экземпляр.
            cache_file (str, optional): Путь к файлу кэша.
            cache_expiry (int, optional): Время жизни кэша в секундах.
        """
        super().__init__(rate_fetcher or RateFetcher())
        self.cache_file = cache_file
        self.cache_expiry = cache_expiry

    def get_exchange_rate(self) -> Any | None:
        """
        Получение обменного курса USD к CNY.

        Возвращает обменный курс или None в случае ошибки.
        """
        rates = self._load_from_cache()
        if rates:
            return rates.get('CNY')

        rates_data = self.rate_fetcher.fetch_rates()
        if rates_data and 'rates' in rates_data:
            rates = rates_data['rates']
            self._save_to_cache(rates)
            return rates.get('CNY')
        return None

    def _load_from_cache(self) -> Any | None:
        """Загрузка курсов из кэша."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    data = json.load(f)
                    if time.time() - data['timestamp'] < self.cache_expiry:
                        return data['rates']
            except (json.JSONDecodeError, KeyError):
                print("Invalid cache file. Fetching from API.") # Можно заменить на logging.warning
                return None
        return None

    def _save_to_cache(self, rates) -> None:
        """Сохранение курсов в кэш."""
        try:
            data = {'timestamp': time.time(), 'rates': rates}
            with open(self.cache_file, 'w') as f:
                json.dump(data, f)
        except IOError as e:
            print(f"Error saving to cache: {e}") # Можно заменить на logging.error

    def convert_usd_to_cny(self, amount) -> float | None:
        """
        Конвертация USD в CNY.

        Args:
            amount (float): Сумма в USD.

        Returns:
            float: Сумма в CNY или None в случае ошибки получения курса.
        """
        rate = self.get_exchange_rate()
        if rate is not None:
            return amount * rate
        return None

    def convert_usd(self, amount, to_currency) -> float | None:
        """
        Конвертация USD в указанную валюту (поддерживается только CNY).

        Args:
            amount (float): Сумма в USD.
            to_currency (str): Код валюты назначения.

        Returns:
            float: Сумма в указанной валюте или None, если валюта не поддерживается
                   или произошла ошибка при получении курса.
        """
        if to_currency == 'CNY':
            return self.convert_usd_to_cny(amount)
        else:
            print(f"UsdCnyConverter не поддерживает конвертацию в {to_currency}. "
                  f"Поддерживается только конвертация в CNY.") # Более информативное сообщение
            return None