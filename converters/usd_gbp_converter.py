import logging
from converters.usd_converter import UsdConverter
from converters.rate_fetcher import RateFetcher


class UsdGbpConverter(UsdConverter):
    def __init__(self, rate_fetcher=None):
        super().__init__(rate_fetcher or RateFetcher())
        self.logger = self._setup_logger()
        self.rates = self.get_exchange_rate()


    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def get_exchange_rate(self):
        rates_data = self.rate_fetcher.fetch_rates()
        if rates_data and 'rates' in rates_data:
            return rates_data['rates'].get('GBP')
        return None


    def convert_usd_to_gbp(self, amount): #
        if self.rates is not None:
            return amount * self.rates
        return None

    def convert_usd(self, amount, to_currency):
        if to_currency == 'GBP':
            return self.convert_usd_to_gbp(amount)
        else:
            print(f"UsdGbpConverter не поддерживает конвертацию в {to_currency}")
            return None
