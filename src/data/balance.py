from data.constants import FieldNames
from data.utils.time import get_timestamp_from_datetime
from datetime import datetime
from typing import Optional, Type

from binance.client import Client
from data.token import TokenBalance, TokenDataSource
from data.sources.fiat import Fiat
import pandas as pd

DATA_SOURCES: list[Type[TokenDataSource]] = [
    Fiat
]


def get_all_transactions_data(binance_client: Client, start_time: datetime,
                              end_time: Optional[datetime]) -> pd.DataFrame:
    start_timestamp = get_timestamp_from_datetime(start_time)
    end_timestamp = get_timestamp_from_datetime(end_time)

    all_transaction_data = [source.get_data(binance_client, start_timestamp, end_timestamp) for source in DATA_SOURCES]
    return pd.concat(all_transaction_data)


def calculate_tokens_balance(tokens_data: pd.DataFrame) -> list[TokenBalance]:
    """
    tokens_data:
    
    name: str,
    quantity': float,
    transaction_time': datetime

    """

    data_sorted_by_transaction_time = _sort_data_by_time(tokens_data)
    data_by_token = _split_data_by_token(data_sorted_by_transaction_time)
    return _get_balances_from_transactions(data_by_token)


def _split_data_by_token(tokens_data: pd.DataFrame) -> list[pd.DataFrame]:
    tokens = tokens_data.name.unique().tolist()
    return [
        tokens_data[tokens_data.name == token] for token in tokens
    ]


def _sort_data_by_time(data: pd.DataFrame) -> pd.DataFrame:
    return data.sort_values(by=[FieldNames.transaction_time])


def _get_balances_from_transactions(token_transactions: list[pd.DataFrame]) -> dict[str, TokenBalance]:
    all_balances = {}
    for transactions in token_transactions:
        name = transactions.name.iloc[0]
        free = transactions.quantity.sum()
        all_balances[name] = TokenBalance(free)
    return all_balances
