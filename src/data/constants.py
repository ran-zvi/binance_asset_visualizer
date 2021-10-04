from .sources.utils import convert_timestamp_to_date
from enum import Enum

YEAR_IN_DAYS = 365


class FiatTransactionType(Enum):
    Deposit = 0
    Withdrawal = 1


class TransactionType(Enum):
    Buy = 0
    Sell = 1


class AccountType(Enum):
    Margin = "MARGIN"
    Spot = "SPOT"
    Futures = "FUTURES"


class TransactionStatus:
    completed = "completed"


class TypeConverter:
    timestamp = convert_timestamp_to_date


class FieldNames:
    update_time = "updateTime"
    date = "date"
    transaction_time = "transaction_time"
    asset = "asset"
    name = "name"
    free = "free"
    locked = "locked"
    obtain_amount = "obtainAmount"
    crypto_currency = "cryptoCurrency"
    quantity = "quantity"
    status = "status"


class ComparisonResult(Enum):
    Equal = 1
    Greater = 2
    Smaller = 3


class TimeIntervals:
    class Minutes:
        one = '1m'
        five = '5m'
        thirty = '30m'

    class Hours:
        one = '1h'
        four = '4h'
