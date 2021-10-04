from dataclasses import dataclass
from typing import NamedTuple

from data.token import TokenBalance

TokenBalances = dict[str, TokenBalance]

@dataclass
class TokenPriceRange(NamedTuple):
    low: float
    high: float

    def price_in_range(self, price: float):
        return self.high >= price >= self.low