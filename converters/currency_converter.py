from abc import ABC, abstractmethod

class CurrencyConverter(ABC):
    @abstractmethod
    def convert_usd(self, amount, to_currency):
        pass