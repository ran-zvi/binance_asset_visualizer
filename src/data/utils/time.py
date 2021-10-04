from datetime import datetime, timedelta

def get_timestamp_30_days_ago() -> int:
    return get_past_timestamp(30)

def get_timestamp_today() -> int:
    return get_past_timestamp(0)

def get_past_timestamp(interval_days: int = 0) -> int:
    date_in_past = datetime.utcnow() - timedelta(days=interval_days)
    return get_timestamp_from_datetime(date_in_past)

def get_timestamp_from_datetime(t: datetime) -> int:
    return int(t.timestamp()) * 1000