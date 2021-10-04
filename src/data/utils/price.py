from datetime import datetime

from binance import Client

from data.settings import TokenPriceRange


def get_token_price_range(client: Client, token: str, start_time: float, end_time: float, interval: str) -> TokenPriceRange:
    raw_price_klines = client.get_klines(
        symbol=token,
        interval=interval,
        startTime=start_time,
        endTime=end_time
    )
    closing_prices = [data[4] for data in raw_price_klines]
    return TokenPriceRange(min(closing_prices), max(closing_prices))
