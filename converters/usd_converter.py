from abc import ABC
from converters.currency_converter import CurrencyConverter


class UsdConverter(CurrencyConverter, ABC):
    def __init__(self, rate_fetcher):
        self.rate_fetcher = rate_fetcher

    def get_exchange_rate(self):
        raise NotImplementedError("Subclasses must implement "
                                  "get_exchange_rate to fetch specific currency rate.")

    def convert_usd(self, amount, to_currency):
        raise NotImplementedError("Subclasses must implement convert_usd method.")