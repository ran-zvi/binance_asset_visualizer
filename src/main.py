from data.utils.time import get_past_timestamp, get_timestamp_from_datetime
from data.balance import calculate_tokens_balance, get_all_transactions_data
from data.sources.fiat import Fiat
from data.sources.account_snapshot import AccountSnapshot, get_balances_from_data
from datetime import datetime, timedelta
from data.constants import YEAR_IN_DAYS, FiatTransactionType
from typing import Union
from config import Config
from binance import Client
import pandas as pd


def get_binance_client() -> Client:
    config = Config.create_from_env_vars()
    return Client(api_key=config.binance_api_key, api_secret=config.binance_secret_key)


def get_existing_balances(client: Client) -> list[dict[str, Union[str, float]]]:
    account = client.get_account()
    balances = account["balances"]
    return [
        balance
        for balance in balances
        if float(balance["free"]) or float(balance["locked"])
    ]


def main():
    binance_client = get_binance_client()
    
    # data = get_all_transactions_data(binance_client, datetime.utcnow() - timedelta(days=YEAR_IN_DAYS*5), datetime.utcnow())
    # five_years_ago = get_past_timestamp(YEAR_IN_DAYS * 5)
    binance_client._request_margin_api('get', 'api/v3/allOrders', signed=True, data=dict(
        startTime=five_years_ago
    ))
    a = binance_client.get_c2c_trade_history(startTimestamp=five_years_ago)
    token_balances = calculate_tokens_balance(data)
    print("bob")


if __name__ == "__main__":
    main()
