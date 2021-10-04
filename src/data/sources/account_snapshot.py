from data.constants import TypeConverter, AccountType, FieldNames
from data.token import TokenBalance
from data.sources.settings import DataField
from data.utils.data import convert_to_df
from datetime import datetime
from typing import Any, Optional
from binance.client import Client
import pandas as pd
from data.token import TokenDataSource


class AccountSnapshot(TokenDataSource):
    NAME = "account_snapshot"
    DATA_FIELDS = [
        DataField(FieldNames.update_time, TypeConverter.timestamp),
        DataField(FieldNames.asset, str),
        DataField(FieldNames.free, float),
        DataField(FieldNames.locked, float),
    ]

    @classmethod
    def get_data(
            cls,
            binance_client: Client,
            start_timestamp: Optional[int] = None,
            end_timestamp: Optional[int] = None,
            account_type: AccountType = AccountType.Spot,
    ):
        raw_snapshots = binance_client.get_account_snapshot(
            type=account_type.value, startTime=start_timestamp, endTime=end_timestamp
        )["snapshotVos"]

        return cls._normalize_data(raw_snapshots)

    @classmethod
    def _normalize_data(cls, data: list[dict[str, Any]]) -> pd.DataFrame:
        account_data_per_day = cls._flatten_and_clean_balance_data(data)

        dataframe = convert_to_df(account_data_per_day, cls.DATA_FIELDS)
        dataframe.rename(
            columns={
                FieldNames.update_time: FieldNames.date,
                FieldNames.asset: FieldNames.name,
            },
            inplace=True,
        )

        return dataframe

    @classmethod
    def _flatten_and_clean_balance_data(
            cls, data: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        all_balances = []
        for snapshot in data:
            balances = snapshot["data"]["balances"]
            update_time = snapshot[FieldNames.update_time]
            cls._add_update_time_to_balances(balances, update_time)
            all_balances.extend(balances)
        return all_balances

    @staticmethod
    def _add_update_time_to_balances(
            balances: list[dict[str, Any]], update_time: float
    ) -> None:
        for balance in balances:
            balance[FieldNames.update_time] = update_time


def get_balances_from_data(
        balance_data: pd.DataFrame,
) -> dict[datetime, dict[str, TokenBalance]]:
    balance_data = _filter_balance_data(balance_data)
    balances_by_date = {}
    dates: list[pd.Timestamp] = balance_data.date.sort_values().unique().tolist()

    for date in dates:
        data_by_date = balance_data[balance_data[FieldNames.date] == date]
        token_balances = {
            row.name: TokenBalance(row.free, row.locked)
            for row in data_by_date.itertuples()
        }

        balances_by_date[date] = token_balances

    return balances_by_date


def _filter_balance_data(data: pd.DataFrame) -> pd.DataFrame:
    return data[(data.free > 0) | (data.locked > 0)]
