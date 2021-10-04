from typing import Any, Optional

import pandas as pd
from binance.client import Client

from ..constants import FiatTransactionType, FieldNames, TransactionStatus, TypeConverter
from ..token import TokenDataSource
from ..utils.data import convert_to_df
from .settings import DataField


class Fiat(TokenDataSource):
    NAME = "fiat"
    DATA_FIELDS = [
        DataField(FieldNames.obtain_amount, float),
        DataField(FieldNames.crypto_currency, str),
        DataField(FieldNames.status, str),
        DataField(FieldNames.update_time, TypeConverter.timestamp),
    ]
    DATA_INTERVAL = 0

    @classmethod
    def get_data(
        cls,
        binance_client: Client,
        start_timestamp: Optional[int] = None,
        end_timestamp: Optional[int] = None,
    ):
        purchase_data = cls.get_data_by_transaction(
            binance_client, start_timestamp, end_timestamp, FiatTransactionType.Deposit
        )
        withdrawal_data = cls.get_data_by_transaction(
            binance_client,
            start_timestamp,
            end_timestamp,
            FiatTransactionType.Withdrawal,
        )

        return cls._normalize_data([*purchase_data, *withdrawal_data])

    @classmethod
    def get_data_by_transaction(
        cls,
        binance_client: Client,
        start_timestamp,
        end_timestamp,
        transaction_type: FiatTransactionType,
    ) -> list[dict[str, Any]]:
        return binance_client.get_fiat_payments_history(
            transactionType=transaction_type.value,
            beginTime=start_timestamp,
            endTime=end_timestamp,
        )["data"]

    @classmethod
    def _normalize_data(cls, data: list[dict[str, Any]]) -> pd.DataFrame:
        dataframe = convert_to_df(data, cls.DATA_FIELDS)
        dataframe.rename(
            columns={
                FieldNames.crypto_currency: FieldNames.name,
                FieldNames.obtain_amount: FieldNames.quantity,
                FieldNames.update_time: FieldNames.transaction_time,
            },
            inplace=True,
        )
        return dataframe[
            dataframe.status.str.lower() == TransactionStatus.completed
        ].drop(columns=[FieldNames.status])

