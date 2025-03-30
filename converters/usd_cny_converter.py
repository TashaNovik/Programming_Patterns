import json
import time
import os
from converters.usd_converter import UsdConverter # Import UsdConverter
from converters.rate_fetcher import RateFetcher


class UsdCnyConverter(UsdConverter):
    def __init__(self, rate_fetcher=None, cache_file="exchange_rates.json", cache_expiry=3600):
        super().__init__(rate_fetcher or RateFetcher())
        self.cache_file = cache_file
        self.cache_expiry = cache_expiry

    def get_exchange_rate(self):
        rates = self._load_from_cache()
        if rates:
            return rates.get('CNY')

        rates_data = self.rate_fetcher.fetch_rates()
        if rates_data and 'rates' in rates_data:
            rates = rates_data['rates']
            self._save_to_cache(rates)
            return rates.get('CNY')
        return None

    def _load_from_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    data = json.load(f)
                    if time.time() - data['timestamp'] < self.cache_expiry:
                        return data['rates']
            except (json.JSONDecodeError, KeyError):
                print("Invalid cache file. Fetching from API.")
                return None
        return None

    def _save_to_cache(self, rates):
        try:
            data = {'timestamp': time.time(), 'rates': rates}
            with open(self.cache_file, 'w') as f:
                json.dump(data, f)
        except IOError as e:
            print(f"Error saving to cache: {e}")

    def convert_usd_to_cny(self, amount):
        rate = self.get_exchange_rate()
        if rate is not None:
            return amount * rate
        return None

    def convert_usd(self, amount, to_currency):
        if to_currency == 'CNY':
            return self.convert_usd_to_cny(amount)
        else:
            print(f"UsdCnyConverter не поддерживает конвертацию в {to_currency}")
            return None