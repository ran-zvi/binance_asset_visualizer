from datetime import datetime, timedelta
from typing import Generator, Tuple
import pandas as pd


def convert_timestamp_to_date(timestamp: int) -> datetime:
    return pd.Timestamp(timestamp, unit="ms").date()


def generate_batched_timestamps(start: float, end: float, time_interval: int) -> Generator[Tuple[float, float], None, None]:
    start_date = datetime.fromtimestamp(start)
    end_date = datetime.fromtimestamp(end)
    
    delta = (end_date - start_date).days
    interval = timedelta(days=time_interval)

    for _ in range(0, delta, time_interval):
        start_timestamp = start_date.timestamp()
        end_timestamp = (start_date + interval).timestamp()
        if end_timestamp >= end:
            yield (start_timestamp, end)
        else:
            yield (start_timestamp, end_timestamp)
        start_date += interval
