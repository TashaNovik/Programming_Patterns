import requests
import json
import time
import os
import logging

class RateFetcher:
    _instance = None

    def __new__(cls, api_url="https://api.exchangerate-api.com/v4/latest/USD",
                cache_file="exchange_rates.json", cache_expiry=3600, max_retries=3, retry_delay=2):
        if not cls._instance:
            cls._instance = super(RateFetcher, cls).__new__(cls)
            cls._instance.api_url = api_url
            cls._instance.cache_file = cache_file
            cls._instance.cache_expiry = cache_expiry
            cls._instance.max_retries = max_retries
            cls._instance.retry_delay = retry_delay
            cls._instance.logger = cls._instance._setup_logger()
        return cls._instance

    def __init__(self, api_url="https://api.exchangerate-api.com/v4/latest/USD",
                 cache_file="exchange_rates.json", cache_expiry=3600, max_retries=3, retry_delay=2):
        if not hasattr(self, 'logger'):
            self.api_url = api_url
            self.cache_file = cache_file
            self.cache_expiry = cache_expiry
            self.max_retries = max_retries
            self.retry_delay = retry_delay
            self.logger = self._setup_logger()


    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def fetch_rates(self):
        rates = self._load_from_cache()
        if rates:
            return rates

        for attempt in range(self.max_retries):
            try:
                response = requests.get(self.api_url, timeout=10)
                response.raise_for_status()
                data = response.json()
                if 'rates' in data:
                    rates = data
                    self._save_to_cache(rates)
                    return rates
                else:
                    self.logger.error("Response JSON missing 'rates' key.")
                    return None


            except requests.exceptions.RequestException as e:
                self.logger.error(f"API request failed (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    self.logger.error("Max retries reached. Unable to fetch rates from API.")
                    return None
            except json.JSONDecodeError as e:
                self.logger.error(f"Error decoding JSON response: {e}")
                return None


    def _load_from_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    data = json.load(f)
                    if 'timestamp' in data and 'rates' in data and time.time() - data['timestamp'] < self.cache_expiry:
                        self.logger.info("Rates loaded from cache.")
                        return data
            except (json.JSONDecodeError, KeyError):
                self.logger.warning("Invalid cache file or format. Fetching from API.")
                return None
        return None

    def _save_to_cache(self, rates):
        try:
            rates['timestamp'] = time.time() # Add timestamp when saving
            with open(self.cache_file, 'w') as f:
                json.dump(rates, f)
            self.logger.info("Rates saved to cache.")
        except IOError as e:
            self.logger.error(f"Error saving rates to cache file: {e}")
        except TypeError as e:
            self.logger.error(f"Error serializing rates to JSON: {e}")