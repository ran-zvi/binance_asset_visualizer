from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

import pandas as pd
from binance import Client

from data.sources.settings import DataField
from data.constants import FieldNames


class TokenDataSource(ABC):

    NAME: Optional[str] = None
    DATA_FIELDS: Optional[list[DataField]] = None
    DATA_INTERVAL: Optional[int] = None

    def __new__(cls, *args, **kwargs):
        class_attrs = ["NAME", "DATA_FIELDS", "DATA_INTERVAL"]
        for attr in class_attrs:
            if not getattr(cls, attr, None):
                raise ValueError(f"class: {cls.__name__} missing attribute: {attr}")
        return super().__new__(cls, *args, **kwargs)

    @classmethod
    @abstractmethod
    def get_data(
        cls,
        binance_client: Client,
        start_timestamp: Optional[int] = None,
        end_timestamp: Optional[int] = None,
    ):
        pass

    @classmethod
    @abstractmethod
    def _normalize_data(cls, data):
        pass


@dataclass
class TokenBalance:
    free: float = 0.0
    locked: float = 0.0

    @classmethod
    def create_from_series(cls, data: pd.Series) -> "TokenBalance":
        return cls(
            data[FieldNames.free], data[FieldNames.locked]
        )

    def balance(self) -> float:
        return self.free + self.locked

    def flipped(self) -> 'TokenBalance':
        return TokenBalance(
            self.locked,
            self.free
        )

    def __eq__(self, other: 'TokenBalance') -> bool:
        return (self.free == other.free) and (self.locked == other.locked)

    def __sub__(self, other: 'TokenBalance') -> 'TokenBalance':
        return TokenBalance(
            self.free - other.free,
            self.locked - other.locked
        )

    def __add__(self, other: 'TokenBalance') -> 'TokenBalance':
        return TokenBalance(
            self.free + other.free,
            self.locked + other.locked
        )
