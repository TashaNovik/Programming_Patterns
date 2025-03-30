from converters.usd_converter import UsdConverter
from converters.rate_fetcher import RateFetcher


class UsdRubConverter(UsdConverter):
    def __init__(self, rate_fetcher=None):
        super().__init__(rate_fetcher or RateFetcher())
        self.rates = self.get_exchange_rate()


    def get_exchange_rate(self):
        rates_data = self.rate_fetcher.fetch_rates()
        if rates_data and 'rates' in rates_data:
            return rates_data['rates'].get('RUB')
        return None

    def convert_usd_to_rub(self, amount):
        if self.rates is not None:
            return amount * self.rates
        return None

    def convert_usd(self, amount, to_currency):
        if to_currency == 'RUB':
            return self.convert_usd_to_rub(amount)
        else:
            print(f"UsdRubConverter не поддерживает конвертацию в {to_currency}")